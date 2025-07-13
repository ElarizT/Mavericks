import json
from typing import Awaitable, Callable
import copy
import pytest
import requests
import websockets
import asyncio

from loguru import logger
from datetime import datetime
from tests.conftest import DummyAgent
from tests.constants import ACTIVE_AGENTS, URI, AGENT_INPUT_SCHEMA, WS_HEADERS
from genai_session.session import GenAISession


@pytest.mark.asyncio
@pytest.mark.order(-1)
async def test_agent_kill_during_request(
    user_jwt_token: str,
    agent_jwt_factory: Callable[[str], Awaitable[str]],
    agent_factory: Callable[[], DummyAgent],
):
    """Tests behaviour if agent was killed during request"""
    dummy_agent_1 = agent_factory()
    dummy_agent_2 = agent_factory()

    JWT_TOKEN_1 = await agent_jwt_factory(user_jwt_token)
    JWT_TOKEN_2 = await agent_jwt_factory(user_jwt_token)
    session_1 = GenAISession(jwt_token=JWT_TOKEN_1)
    session_2 = GenAISession(jwt_token=JWT_TOKEN_2)

    @session_1.bind(name=dummy_agent_1.name, description=dummy_agent_1.description)
    async def get_current_date(agent_context=""):
        """An example agent function that takes time and can be cancelled."""
        await asyncio.sleep(10)  # Simulate a long-running task
        return datetime.now().strftime("%Y-%m-%d")

    @session_2.bind(name=dummy_agent_2.name, description=dummy_agent_2.description)
    async def get_current_time(agent_context=""):
        """Attempts to call GetCurrentDateTest (which might be inactive) and returns the response status."""
        response = await session_2.send(message={}, client_id=session_1.agent_id)
        return f"Response is successful: {response.is_success}. Current date is {response.response}."

    async def process_events_session_1():
        """Processes events only for session_1."""
        await session_1.process_events()

    async def process_events_session_2():
        """Processes events only for session_2."""
        await session_2.process_events()

    # Start processing events in background
    event_task_1 = asyncio.create_task(process_events_session_1())
    await asyncio.sleep(0.1)  # Reduced sleep for faster initialization

    event_task_2 = asyncio.create_task(process_events_session_2())
    await asyncio.sleep(0.1)  # Reduced sleep for faster initialization

    invoke_data = {
        "message_type": "agent_invoke",
        "agent_uuid": session_2.agent_id,
        "request_payload": {},
    }

    expected_agent_input_schema = copy.deepcopy(AGENT_INPUT_SCHEMA)
    expected_agent_input_schema["function"] = {
        "name": session_2.agent_id,
        "description": dummy_agent_2.description,
    }

    async with websockets.connect(URI, additional_headers=WS_HEADERS) as websocket:
        await websocket.send(json.dumps(invoke_data))

        # Wait for a short time to ensure the agent starts processing
        await asyncio.sleep(1)

        await websocket.send(json.dumps(invoke_data))

        # Simulate killing the agent
        event_task_1.cancel()

        # Validate that the agent is no longer in the active list
        await asyncio.sleep(2)  # Give some time for the active list to update

        response = await websocket.recv()
        response_data = json.loads(response)

        logger.info(f"WebSocket Response: {response_data}")

        assert (
            response_data.get("response")
            == "Response is successful: False. Current date is Agent has been unregistered."
        ), f"{response_data}"
        assert response_data.get("message_type") == "agent_response", f"{response_data}"

        rest_response = requests.get(
            ACTIVE_AGENTS,
            headers={"Authorization": f"Bearer {user_jwt_token}"},
        )
        rest_response.raise_for_status()
        active_agents_data = rest_response.json()

        logger.info(f"Active agents after potential kill: {active_agents_data}")

        assert active_agents_data.get("count_active_connections") == 1, (
            f"Agent should not be active: {active_agents_data}"
        )

        assert len(active_agents_data.get("active_connections")) == 1, (
            f"Active connections should be empty: {active_agents_data}"
        )

        logger.info("\nTest successful (agent kill simulated)!")

        event_task_2.cancel()
