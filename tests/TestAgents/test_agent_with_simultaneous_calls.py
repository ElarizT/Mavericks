import json
from typing import Awaitable, Callable
import uuid
import pytest
import websockets
import asyncio

from loguru import logger
from time import time
from genai_session.session import GenAISession
from tests.conftest import DummyAgent
from tests.constants import URI

TIMEOUT = 3


async def send_message(uri: str, message: str):
    """Connects to a WebSocket server and sends a message."""

    headers = {"x-custom-authorization": str(uuid.uuid4())}

    try:
        async with websockets.connect(uri, additional_headers=headers) as websocket:
            json_message = json.dumps(message)

            await asyncio.sleep(0.1)

            await websocket.send(json_message)

            logger.info(f"Sent: {json_message}")

            await asyncio.sleep(0.1)

            response = await websocket.recv()

            logger.info(f"Received: {response}")

            return response

    except websockets.exceptions.ConnectionClosedError as e:
        logger.info(f"Connection closed unexpectedly: {e}")

    except ConnectionRefusedError:
        logger.info(f"Connection refused at {uri}")


@pytest.mark.asyncio
async def test_agent_for_doc_string_description_schema(
    user_jwt_token: str,
    agent_jwt_factory: Callable[[str], Awaitable[str]],
    agent_factory: Callable[[], DummyAgent],
):
    """Tests how agent handles simultaneous calls"""
    dummy_agent_1 = agent_factory()

    JWT_TOKEN_1 = await agent_jwt_factory(user_jwt_token)
    session = GenAISession(jwt_token=JWT_TOKEN_1)

    @session.bind(name=dummy_agent_1.name, description=dummy_agent_1.description)
    async def get_current_time(agent_context=""):
        """Returns the current time"""
        started_at = time()
        await asyncio.sleep(TIMEOUT)
        return {"started_at": started_at, "ended_at": time()}

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

    try:
        messages = [invoke_data, invoke_data]
        tasks = [send_message(uri=URI, message=msg) for msg in messages]
        responses = await asyncio.gather(*tasks)

        resp_1 = json.loads(responses[0])
        resp_2 = json.loads(responses[1])

        started_at_resp_1 = resp_1.get("response").get("started_at")
        started_at_resp_2 = resp_2.get("response").get("started_at")

        ended_at_resp_1 = resp_1.get("response").get("ended_at")
        ended_at_resp_2 = resp_2.get("response").get("ended_at")

        execution_time_resp_1 = resp_1.get("execution_time")
        execution_time_resp_2 = resp_2.get("execution_time")

        assert 3 > abs(started_at_resp_1 - started_at_resp_2) > 0
        assert 3 > abs(ended_at_resp_1 - ended_at_resp_2) > 0

        assert abs(execution_time_resp_1 - execution_time_resp_2) < 3

        logger.info("Test successful!")

    finally:
        # Clean up background task
        event_task.cancel()

        try:
            await event_task

        except asyncio.CancelledError:
            logger.info("Background task has been properly cancelled.")
