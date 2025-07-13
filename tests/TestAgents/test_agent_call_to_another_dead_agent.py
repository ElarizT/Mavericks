import json
from typing import Awaitable, Callable
import pytest
import requests
import websockets
import asyncio

from loguru import logger
from datetime import datetime
from genai_session.session import GenAISession

from tests.constants import URI, ACTIVE_AGENTS, WS_HEADERS
from tests.conftest import DummyAgent


@pytest.mark.asyncio
async def test_agent_call_to_another_dead_agent(
    user_jwt_token: str,
    agent_jwt_factory: Callable[[str], Awaitable[str]],
    agent_factory: Callable[[], DummyAgent],
):
    """Tests the behavior when an agent attempts to call another agent that is not actively processing events."""
    dummy_agent_1 = agent_factory()
    dummy_agent_2 = agent_factory()

    JWT_TOKEN_1 = await agent_jwt_factory(user_jwt_token)
    JWT_TOKEN_2 = await agent_jwt_factory(user_jwt_token)
    session_1 = GenAISession(jwt_token=JWT_TOKEN_1)
    session_2 = GenAISession(jwt_token=JWT_TOKEN_2)

    @session_1.bind(name=dummy_agent_1.name, description=dummy_agent_1.description)
    async def get_current_date(agent_context=""):
        """Returns the current date in YYYY-MM-DD format."""
        return datetime.now().strftime("%Y-%m-%d")

    @session_2.bind(name=dummy_agent_2.name, description=dummy_agent_2.description)
    async def get_current_time(agent_context=""):
        """Calls the GetCurrentDateTest agent and returns its response."""
        response = await session_2.send(message={}, client_id=session_1.agent_id)
        return f"Response is successful: {response.is_success}. Current date is {response.response}."

    async def process_events_session_1():
        """Processes events only for session_1."""
        await session_1.process_events()

    # Start background task to process session_1 events
    event_task = asyncio.create_task(process_events_session_1())

    # Allow session_1 to initialize briefly
    await asyncio.sleep(0.1)  # Adjust as needed

    invoke_data = {
        "message_type": "agent_invoke",
        "agent_uuid": session_2.agent_id,
        "request_payload": {},
    }

    expected_active_agent_schema = {
        "agent_id": session_1.agent_id,
        "agent_name": dummy_agent_1.name,
        "agent_description": dummy_agent_1.description,
        "agent_input_schema": {
            "type": "function",
            "function": {
                "name": session_1.agent_id,
                "description": dummy_agent_1.description,
                "parameters": {"type": "object", "properties": {}, "required": []},
            },
        },
    }

    try:
        async with websockets.connect(URI, additional_headers=WS_HEADERS) as websocket:
            await websocket.send(json.dumps(invoke_data))
            response = await websocket.recv()
            response_data = json.loads(response)

            logger.info(f"WebSocket Response: {response_data}")

            error = response_data.get("error", {})
            assert error.get("error_message") == "Agent is NOT active", (
                f"{response_data}"
            )
            assert error.get("error_type") == "AgentNotActive", f"{response_data}"

            # Check active agents
            rest_response = requests.get(
                ACTIVE_AGENTS,
                headers={"Authorization": f"Bearer {user_jwt_token}"},
            )
            rest_response.raise_for_status()
            agent_data = rest_response.json()

            logger.info(f"Active agents: {agent_data}")

            assert agent_data.get("count_active_connections") == 1, f"{agent_data}"
            assert len(agent_data.get("active_connections")) == 1, f"{agent_data}"

            [active_connection] = agent_data.get("active_connections")
            assert active_connection == expected_active_agent_schema, f"{agent_data}"

            logger.info("Test successful!")

    finally:
        # Cancel the background task
        event_task.cancel()
        try:
            await event_task
        except asyncio.CancelledError:
            logger.info("Background task has been properly cancelled.")
