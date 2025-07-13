import json
from typing import Awaitable, Callable
import pytest
import requests
import websockets
import asyncio

from loguru import logger
from datetime import datetime
from genai_session.session import GenAISession
from tests.conftest import DummyAgent
from tests.constants import URI, ACTIVE_AGENTS, AGENT_INPUT_SCHEMA, WS_HEADERS


@pytest.mark.asyncio
async def test_agent_with_default_parameters_2(
    user_jwt_token: str,
    agent_jwt_factory: Callable[[str], Awaitable[str]],
    agent_factory: Callable[[], DummyAgent],
):
    """Tests if the agent correctly uses the provided parameter value in the invoke payload, overriding the default."""
    dummy_agent_1 = agent_factory()

    JWT_TOKEN_1 = await agent_jwt_factory(user_jwt_token)
    session = GenAISession(jwt_token=JWT_TOKEN_1)

    @session.bind(name=dummy_agent_1.name, description=dummy_agent_1.description)
    async def get_current_date(param: str = "Param", agent_context=""):
        """Returns the current date, prefixed with the provided 'param' value (or 'Param' if not provided)."""
        date = datetime.now().strftime("%Y-%m-%d")
        return f"{param} _ {date}"

    async def process_events():
        """Processes events for the GenAISession."""
        await session.process_events()

    event_task = asyncio.create_task(process_events())
    await asyncio.sleep(0.1)  # Reduced sleep for faster initialization

    # Payload includes "param" to override default
    invoke_data = {
        "message_type": "agent_invoke",
        "agent_uuid": session.agent_id,
        "request_payload": {"param": "New_Param"},
    }

    expected_agent_input_schema = AGENT_INPUT_SCHEMA.copy()
    expected_agent_input_schema["function"]["name"] = session.agent_id
    expected_agent_input_schema["function"]["description"] = dummy_agent_1.description
    expected_agent_input_schema["function"]["parameters"] = {
        "type": "object",
        "properties": {"param": {"type": "string", "default": "Param"}},
        "required": [],
    }

    try:
        async with websockets.connect(URI, additional_headers=WS_HEADERS) as websocket:
            await websocket.send(json.dumps(invoke_data))
            response = await websocket.recv()
            response_data = json.loads(response)
            logger.info(f"Response: {response_data}")

            expected_response = f"New_Param _ {datetime.now().strftime('%Y-%m-%d')}"
            assert response_data.get("response") == expected_response
            assert response_data.get("message_type") == "agent_response"

            # Confirm registered agent state via REST
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
        # Cleanup
        event_task.cancel()
        try:
            await event_task
        except asyncio.CancelledError:
            logger.info("Background task has been properly cancelled.")
