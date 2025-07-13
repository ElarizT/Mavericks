import json
from typing import Awaitable, Callable
import asyncio
import requests
import websockets
import pytest

from loguru import logger
from datetime import datetime
from genai_session.session import GenAISession

from tests.constants import URI, ACTIVE_AGENTS, WS_HEADERS
from tests.conftest import DummyAgent


@pytest.mark.asyncio
async def test_agent_call_to_another_agent(
    user_jwt_token: str,
    agent_jwt_factory: Callable[[str], Awaitable[str]],
    agent_factory: Callable[[], DummyAgent],
):
    """Tests if one agent can successfully call another and if their metadata is correct."""

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

    async def process_events():
        """Processes events for both GenAISession instances concurrently."""
        await asyncio.gather(session_1.process_events(), session_2.process_events())
        # Start background processing

    event_task = asyncio.create_task(process_events())

    # Allow agents a brief period to initialize
    await asyncio.sleep(0.1)  # Adjust as needed

    invoke_data = {
        "message_type": "agent_invoke",
        "agent_uuid": session_2.agent_id,
        "request_payload": {},
    }

    expected_agent_1_input_schema = {
        "agent_id": session_2.agent_id,
        "agent_name": dummy_agent_2.name,
        "agent_description": dummy_agent_2.description,
        "agent_input_schema": {
            "type": "function",
            "function": {
                "name": session_2.agent_id,
                "description": dummy_agent_2.description,
                "parameters": {"type": "object", "properties": {}, "required": []},
            },
        },
    }

    expected_agent_2_input_schema = {
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

            logger.info(f"Response from invoking agent: {response_data}")

            expected_date_str = datetime.now().strftime("%Y-%m-%d")
            expected_response = (
                f"Response is successful: True. Current date is {expected_date_str}."
            )
            assert response_data.get("response") == expected_response
            assert response_data.get("message_type") == "agent_response"

            active_agents_response = requests.get(
                ACTIVE_AGENTS,
                headers={"Authorization": f"Bearer {user_jwt_token}"},
            )
            active_agents_response.raise_for_status()
            active_agents_data = active_agents_response.json()

            logger.info(f"Active agents data: {active_agents_data}")

            assert active_agents_data.get("count_active_connections") == 2
            assert len(active_agents_data.get("active_connections")) == 2

            active_connections = active_agents_data.get("active_connections")
            agents_by_id = {agent["agent_id"]: agent for agent in active_connections}

            assert agents_by_id[session_2.agent_id] == expected_agent_1_input_schema
            assert agents_by_id[session_1.agent_id] == expected_agent_2_input_schema

            logger.info("Test successful!")

    finally:
        # Cancel background event loop
        event_task.cancel()
        try:
            await event_task
        except asyncio.CancelledError:
            logger.info("Background task has been properly cancelled.")
