import json
from typing import Awaitable, Callable
import asyncio
import requests
import websockets
import pytest

from loguru import logger
from datetime import datetime
from genai_session.session import GenAISession
from tests.conftest import DummyAgent
from tests.constants import URI, ACTIVE_AGENTS, AGENT_INPUT_SCHEMA, WS_HEADERS


@pytest.mark.asyncio
async def test_agent_with_required_params(
    user_jwt_token: str,
    agent_jwt_factory: Callable[[str], Awaitable[str]],
    agent_factory: Callable[[], DummyAgent],
):
    """Tests if the agent correctly handles and registers with multiple required parameters of different types."""
    dummy_agent_1 = agent_factory()

    JWT_TOKEN_1 = await agent_jwt_factory(user_jwt_token)
    session = GenAISession(jwt_token=JWT_TOKEN_1)

    @session.bind(name=dummy_agent_1.name, description=dummy_agent_1.description)
    async def get_current_date(
        param_1: str,
        param_2: list[str],
        param_3: dict[str, str],
        agent_context="",
    ):
        """Returns the current date concatenated with the provided parameters."""
        date = datetime.now().strftime("%Y-%m-%d")
        return (
            f"{param_1} _ {param_2[0]} _ {param_2[1]} _ {str(param_3.items())} _ {date}"
        )

    async def process_events():
        """Processes events for the GenAISession."""
        await session.process_events()

    # Start agent's background event processing
    event_task = asyncio.create_task(process_events())
    await asyncio.sleep(0.1)  # Reduced sleep for faster initialization

    invoke_data = {
        "message_type": "agent_invoke",
        "agent_uuid": session.agent_id,
        "request_payload": {
            "param_1": "Param_1",
            "param_2": ["0", "1"],
            "param_3": {"key": "val"},
        },
    }

    expected_agent_input_schema = AGENT_INPUT_SCHEMA.copy()
    expected_agent_input_schema["function"]["name"] = session.agent_id
    expected_agent_input_schema["function"]["description"] = dummy_agent_1.description
    expected_agent_input_schema["function"]["parameters"] = {
        "type": "object",
        "properties": {
            "param_1": {"type": "string"},
            "param_2": {"type": "array", "items": {"type": "string"}},
            "param_3": {"type": "object", "additionalProperties": {"type": "string"}},
        },
        "required": ["param_1", "param_2", "param_3"],
    }

    try:
        async with websockets.connect(URI, additional_headers=WS_HEADERS) as websocket:
            await websocket.send(json.dumps(invoke_data))
            response = await websocket.recv()
            response_data = json.loads(response)
            logger.info(f"Response: {response_data}")

            expected_response = f"Param_1 _ 0 _ 1 _ dict_items([('key', 'val')]) _ {datetime.now().strftime('%Y-%m-%d')}"  # noqa: E501
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
            logger.info("Background task cancelled cleanly.")
