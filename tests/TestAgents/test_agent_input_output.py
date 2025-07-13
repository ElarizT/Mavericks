import json
from typing import Awaitable, Callable
import pytest
import asyncio
import mimetypes
import websockets

from loguru import logger
from copy import deepcopy
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
from tests.conftest import DummyAgent
from tests.http_client.AsyncHTTPClient import AsyncHTTPClient
from tests.constants import URI, WS_HEADERS, WS_MESSAGE

mimetypes.init()
http_client = AsyncHTTPClient(timeout=10)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input, output",
    [
        ("valid_string", "valid_string"),
        (12345, 12345),
        (12.34, 12.34),
        (True, True),
        (None, None),
        (["list", "of", "strings"], ["list", "of", "strings"]),
        ({"key": "value"}, {"key": "value"}),
        ((1, 2, 3), [1, 2, 3]),
    ],
    ids=[
        "how agent accepts normal string",
        "how agent accepts integer",
        "how agent accepts float",
        "how agent accepts boolean",
        "how agent accepts NoneType",
        "how agent accepts list",
        "how agent accepts dictionary",
        "how agent accepts tuple",
    ],
)
async def test_agent_input_output(
    input,
    output,
    user_jwt_token: str,
    agent_jwt_factory: Callable[[str], Awaitable[str]],
    agent_factory: Callable[[], DummyAgent],
):
    JWT_TOKEN_1 = await agent_jwt_factory(user_jwt_token)
    session_1 = GenAISession(jwt_token=JWT_TOKEN_1)

    @session_1.bind(name="Input agent", description="Verifies what input is valid")
    async def io_agent(agent_context: GenAIContext, input: str):
        agent_uuid = agent_context.agent_uuid

        logger.info(f"Agent {agent_uuid} is up")

        return input

    async def start_io_agent():
        await asyncio.gather(session_1.process_events())

    event_task_1 = asyncio.create_task(start_io_agent())

    await asyncio.sleep(0.1)

    event_tasks = [event_task_1]

    message = deepcopy(WS_MESSAGE)
    message["agent_uuid"] = session_1.agent_id
    message["request_payload"]["input"] = input

    try:
        async with websockets.connect(
            URI, additional_headers=WS_HEADERS, close_timeout=10
        ) as websocket:
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            response_data = json.loads(response)
            logger.info(f"WebSocket Response: {response_data}")
            del response_data["execution_time"]
            expected_response_data = {
                "response": output,
                "message_type": "agent_response",
            }

            assert response_data == expected_response_data

            logger.info("Test successful!")

    finally:
        for task in event_tasks:
            task.cancel()

        try:
            await task

        except asyncio.CancelledError:
            logger.info("Background task has been properly cancelled.")
