import json
from typing import Awaitable, Callable
import uuid
import pytest
import requests
import websockets
import asyncio

from loguru import logger
from genai_session.session import GenAISession
from tests.constants import URI, ACTIVE_AGENTS, AGENT_INPUT_SCHEMA, WS_HEADERS
from tests.conftest import DummyAgent


@pytest.mark.asyncio
async def test_agent_call_when_agent_is_inactive(
    user_jwt_token: str,
    agent_jwt_factory: Callable[[str], Awaitable[str]],
    agent_factory: Callable[[], DummyAgent],
):
    """Tests the behavior when attempting to call a non-existent (inactive) agent."""
    dummy_agent_1 = agent_factory()
    JWT_TOKEN_1 = await agent_jwt_factory(user_jwt_token)
    session = GenAISession(jwt_token=JWT_TOKEN_1)

    @session.bind(name=dummy_agent_1.name, description=dummy_agent_1.description)
    async def dummy_handler(agent_context=""):
        """A dummy agent handler that simply returns True."""
        return True

    async def process_events():
        """Processes events for the registered GenAISession."""
        await session.process_events()

    event_task = asyncio.create_task(process_events())
    await asyncio.sleep(0.1)  # Reduced sleep for faster initialization

    # Simulate calling a non-existing (inactive) agent
    invoke_data = {
        "message_type": "agent_invoke",
        "agent_uuid": str(uuid.uuid4())[::-1],
        "request_payload": {},
    }

    expected_active_agent_schema = AGENT_INPUT_SCHEMA.copy()
    expected_active_agent_schema["function"]["name"] = session.agent_id
    expected_active_agent_schema["function"]["description"] = dummy_agent_1.description

    try:
        async with websockets.connect(URI, additional_headers=WS_HEADERS) as websocket:
            await websocket.send(json.dumps(invoke_data))
            response = await websocket.recv()
            response_data = json.loads(response)

            logger.info(f"WebSocket response: {response_data}")

            error = response_data.get("error", {})
            assert error.get("error_message") == "Agent is NOT active"
            assert error.get("error_type") == "AgentNotActive"

            # Check that only the registered agent is active
            rest_response = requests.get(
                ACTIVE_AGENTS,
                headers={"Authorization": f"Bearer {user_jwt_token}"},
            )
            rest_response.raise_for_status()
            active_data = rest_response.json()

            logger.info(f"Active agents: {active_data}")

            assert active_data.get("count_active_connections") == 1
            assert len(active_data.get("active_connections")) == 1

            [active_connection] = active_data.get("active_connections")
            assert active_connection.get("agent_id") == session.agent_id
            assert active_connection.get("agent_name") == dummy_agent_1.name
            assert (
                active_connection.get("agent_description") == dummy_agent_1.description
            )
            assert (
                active_connection.get("agent_input_schema")
                == expected_active_agent_schema
            )

    finally:
        # Clean up the background task
        event_task.cancel()
        try:
            await event_task
        except asyncio.CancelledError:
            logger.info("Background task has been properly cancelled.")
