import json
from typing import Awaitable, Callable
import copy
import pytest
import requests
import websockets
import asyncio

from loguru import logger
from genai_session.session import GenAISession
from tests.conftest import DummyAgent
from tests.constants import URI, ACTIVE_AGENTS, AGENT_INPUT_SCHEMA, WS_HEADERS


@pytest.mark.asyncio
async def test_agent_for_error_handling(
    user_jwt_token: str,
    agent_jwt_factory: Callable[[str], Awaitable[str]],
    agent_factory: Callable[[], DummyAgent],
):
    """Tests if the agent correctly handles and reports a ZeroDivisionError."""
    # Start processing agent events
    dummy_agent_1 = agent_factory()

    JWT_TOKEN_1 = await agent_jwt_factory(user_jwt_token)
    session = GenAISession(jwt_token=JWT_TOKEN_1)

    @session.bind(name=dummy_agent_1.name, description=dummy_agent_1.description)
    async def zero_division(agent_context=""):
        """Deliberately raises a ZeroDivisionError for testing error handling."""
        return 1 / 0  # Deliberate error for testing

    async def process_events():
        """Processes events for the GenAISession."""
        logger.info(f"Agent with ID {JWT_TOKEN_1} started")
        await session.process_events()

    event_task = asyncio.create_task(process_events())
    await asyncio.sleep(0.1)  # Reduced sleep for faster initialization

    invoke_data = {
        "message_type": "agent_invoke",
        "agent_uuid": session.agent_id,
        "request_payload": {},
    }

    expected_agent_input_schema = copy.deepcopy(AGENT_INPUT_SCHEMA)
    expected_agent_input_schema["function"]["name"] = session.agent_id
    expected_agent_input_schema["function"]["description"] = dummy_agent_1.description

    try:
        async with websockets.connect(URI, additional_headers=WS_HEADERS) as websocket:
            await websocket.send(json.dumps(invoke_data))
            response = await websocket.recv()
            response_data = json.loads(response)

            logger.info(f"WebSocket Response: {response_data}")

            assert response_data.get("message_type") == "agent_error"
            assert (
                response_data.get("error", {}).get("error_message")
                == "division by zero"
            )
            assert (
                response_data.get("execution_time") >= 0
            )  # Execution time might not be exactly 0

            # Check agent registration via REST
            rest_response = requests.get(
                ACTIVE_AGENTS,
                headers={"Authorization": f"Bearer {user_jwt_token}"},
            )
            rest_response.raise_for_status()
            active_agents_data = rest_response.json()

            logger.info(f"Active agents: {active_agents_data}")

            assert active_agents_data.get("count_active_connections") == 1
            assert len(active_agents_data.get("active_connections")) == 1

            [active_connection] = active_agents_data.get("active_connections")
            agent_input_schema = active_connection.get("agent_input_schema")

            assert active_connection.get("agent_id") == session.agent_id
            assert active_connection.get("agent_name") == dummy_agent_1.name
            assert (
                active_connection.get("agent_description") == dummy_agent_1.description
            )
            assert agent_input_schema == expected_agent_input_schema

            logger.info("Test successful!")

    finally:
        # Cancel background task
        event_task.cancel()
        try:
            await event_task
        except asyncio.CancelledError:
            logger.info("Background task has been properly cancelled.")
