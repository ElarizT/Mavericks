import json
from typing import Awaitable, Callable
import copy
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
async def test_agent_for_doc_string_description_schema(
    user_jwt_token: str,
    agent_jwt_factory: Callable[[str], Awaitable[str]],
    agent_factory: Callable[[], DummyAgent],
):
    """Tests if the agent registers with the correct name, description (from decorator), and schema."""
    dummy_agent = agent_factory()
    JWT_TOKEN = await agent_jwt_factory(user_jwt_token)
    session = GenAISession(jwt_token=JWT_TOKEN)

    @session.bind(name=dummy_agent.name, description=dummy_agent.description)
    async def get_current_date(agent_context=""):
        """Returns the current date in YYYY-MM-DD format."""
        return datetime.now().strftime("%Y-%m-%d")

    async def process_events():
        """Processes events for the GenAISession."""
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
    expected_agent_input_schema["function"]["description"] = dummy_agent.description

    try:
        async with websockets.connect(URI, additional_headers=WS_HEADERS) as websocket:
            await websocket.send(json.dumps(invoke_data))
            response = await websocket.recv()
            response_data = json.loads(response)

            logger.info(f"WebSocket Response: {response_data}")

            assert response_data.get("response") == datetime.now().strftime("%Y-%m-%d")
            assert response_data.get("message_type") == "agent_response"

            rest_response = requests.get(
                ACTIVE_AGENTS,
                headers={"Authorization": f"Bearer {user_jwt_token}"},
            )
            rest_response.raise_for_status()
            active_agents_data = rest_response.json()

            logger.info(f"Active agents: {active_agents_data}")

            assert active_agents_data.get("count_active_connections") == 1, (
                f"{active_agents_data}"
            )
            assert len(active_agents_data.get("active_connections")) == 1, (
                f"{active_agents_data}"
            )

            [active_connection] = active_agents_data.get("active_connections")
            agent_input_schema = active_connection.get("agent_input_schema")

            assert active_connection.get("agent_id") == session.agent_id
            assert active_connection.get("agent_name") == dummy_agent.name
            assert active_connection.get("agent_description") == dummy_agent.description
            assert agent_input_schema == expected_agent_input_schema

            logger.info("Test successful!")

    finally:
        # Clean up background task
        event_task.cancel()
        try:
            await event_task
        except asyncio.CancelledError:
            logger.info("Background task has been properly cancelled.")
