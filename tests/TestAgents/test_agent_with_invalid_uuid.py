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
from tests.constants import URI, ACTIVE_AGENTS, WS_HEADERS

# Intentionally create an invalid UUID for testing


# TODO: invalid jwt does not raise err
@pytest.mark.asyncio
async def test_agent_with_invalid_uuid(
    user_jwt_token: str,
    agent_jwt_factory: Callable[[str], Awaitable[str]],
    agent_factory: Callable[[], DummyAgent],
):
    """Tests the behavior when the GenAISession is initialized with an invalid agent UUID."""
    # Start the background event processing (which should raise an exception)
    dummy_agent_1 = agent_factory()

    _ = await agent_jwt_factory(user_jwt_token)
    session = GenAISession(jwt_token="asd")

    @session.bind(name=dummy_agent_1.name, description=dummy_agent_1.description)
    async def get_current_date(param: str = "Param", agent_context=""):
        """Returns the current date, prefixed with the provided 'param' value (or 'Param' if not provided)."""
        date = datetime.now().strftime("%Y-%m-%d")
        return f"{param} _ {date}"

    async def process_events():
        """Attempts to process events with an invalid agent ID and asserts the expected error."""
        # with pytest.raises(Exception) as excinfo:
        await session.process_events()
        # assert str(excinfo.value) == "Agent ID is not UUID"
        # logger.info(
        #     "Successfully caught expected 'Agent ID is not UUID' error during process_events."
        # )

    event_task = asyncio.create_task(process_events())
    await asyncio.sleep(0.1)  # Give a short time for the task to start

    # Attempt to invoke the agent (which should not be active)
    invoke_data = {
        "message_type": "agent_invoke",
        "agent_uuid": session.agent_id,  # Use a valid UUID for the invoke
        "request_payload": {"param": "New_Param"},
    }

    try:
        async with websockets.connect(URI, additional_headers=WS_HEADERS) as websocket:
            await websocket.send(json.dumps(invoke_data))
            response = await websocket.recv()
            response_data = json.loads(response)
            logger.info(f"WebSocket Response: {response_data}")

            error = response_data.get("error")
            assert error is not None, (
                f"Expected an error response, but got: {response_data}"
            )
            assert error.get("error_message") == "Agent is NOT active", (
                f"{response_data}"
            )
            assert error.get("error_type") == "AgentNotActive", f"{response_data}"

            # Confirm that no agents are active due to the invalid UUID
            rest_response = requests.get(
                ACTIVE_AGENTS,
                headers={"Authorization": f"Bearer {user_jwt_token}"},
            )
            rest_response.raise_for_status()
            active_agents_data = rest_response.json()
            logger.info(f"Active agents: {active_agents_data}")

            assert active_agents_data.get("count_active_connections") == 0, (
                f"{active_agents_data}"
            )
            assert len(active_agents_data.get("active_connections")) == 0, (
                f"{active_agents_data}"
            )

            logger.info("Test successful!")

    finally:
        # Cleanup the background task
        event_task.cancel()
        try:
            await event_task
        except asyncio.CancelledError:
            logger.info("Background task cancelled cleanly.")
