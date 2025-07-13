import json
import logging
import jwt

from typing import Dict

from fastapi import WebSocket
from settings import get_settings
from utils.enums import WSMessageType, MasterServerName, ErrorType

app_settings = get_settings()


class WSConnectionManager:
    """
    WebSocket Connection Manager responsible for managing active WebSocket connections,
    routing messages between agents and master servers, and handling different types
    of WebSocket messages.
    """

    MASTER_SERVERS_API_KEY_MAPPING = {
        app_settings.MASTER_BE_API_KEY: MasterServerName.MASTER_SERVER_BE.value,
        app_settings.MASTER_AGENT_API_KEY: MasterServerName.MASTER_SERVER_ML.value,
    }

    def __init__(self):
        """
        Initializes the WebSocket connection manager with an empty active connections dictionary.
        """
        self.active_connections: Dict[str, WebSocket] = {}

    async def process_message(
        self, client_id: str, message: str, agent_jwt: str
    ) -> None:
        """
        Processes incoming messages from clients and routes them based on message type.

        Args:
            client_id (str): The ID of the client sending the message.
            message (str): The message content as a JSON string.
        """
        try:
            data = json.loads(message)
            logging.debug(f"Received message: {data}")
        except json.JSONDecodeError:
            await self.send_message(
                client_id=client_id,
                message={
                    "error": {
                        "error_message": "Invalid JSON format",
                        "error_type": ErrorType.INVALID_JSON_REQUEST_FORMAT.value,
                    }
                },
            )
        else:
            message_type = data.pop("message_type", None)
            agent_uuid = data.pop("agent_uuid", None)
            payload = data.get("request_payload")

            if message_type == WSMessageType.AGENT_REGISTER.value:
                if client_id not in self.MASTER_SERVERS_API_KEY_MAPPING.values():
                    request_payload = {
                        "request_payload": {
                            **payload,
                            "agent_uuid": client_id,
                            "agent_jwt": agent_jwt,
                            "message_type": message_type,
                        }
                    }

                    # Register the agent in SQL Database
                    await self.send_message(
                        client_id=MasterServerName.MASTER_SERVER_BE.value,
                        message=request_payload,
                    )

            elif message_type in (
                WSMessageType.AGENT_RESPONSE.value,
                WSMessageType.AGENT_ERROR.value,
            ):
                invoked_by = data.pop("invoked_by", None)
                data["message_type"] = message_type
                logging.info(
                    f"Got response: {data}, from: {client_id}, invoked_by: {invoked_by}"
                )
                await self.send_message(invoked_by, data)

            elif message_type == WSMessageType.AGENT_INVOKE.value:
                if not payload and not agent_uuid:
                    await self.send_message(
                        client_id=client_id,
                        message={
                            "error": {
                                "error_message": "Missing request payload or agent UUID",
                                "error_type": ErrorType.NO_REQUEST_PAYLOAD.value,
                            }
                        },
                    )

                if agent_uuid not in self.active_connections:
                    await self.send_message(
                        client_id=client_id,
                        message={
                            "message_type": WSMessageType.AGENT_ERROR.value,
                            "error": {
                                "error_message": "Agent is NOT active",
                                "error_type": ErrorType.AGENT_NOT_ACTIVE.value,
                            },
                        },
                    )

                if (
                    agent_uuid == MasterServerName.MASTER_SERVER_ML.value
                    and not client_id.startswith(app_settings.MASTER_BE_API_KEY)
                ):
                    await self.send_message(
                        client_id=client_id,
                        message={
                            "error": {
                                "error_message": "Agent is NOT active",
                                "error_type": ErrorType.AGENT_NOT_ACTIVE.value,
                            }
                        },
                    )
                else:
                    if (
                        client_id.startswith(app_settings.MASTER_BE_API_KEY)
                        and "error_message" in payload
                    ):
                        payload["message_type"] = WSMessageType.AGENT_ERROR.value
                        payload = {"error": payload}
                        await self.send_message(agent_uuid, payload)
                    else:
                        data["invoked_by"] = client_id
                        await self.send_message(agent_uuid, data)

            elif message_type == WSMessageType.AGENT_LOG.value:
                await self.send_message(
                    client_id=MasterServerName.MASTER_SERVER_BE.value,
                    message={
                        "request_payload": {
                            "message_type": message_type,
                            "agent_uuid": client_id,
                            **data,
                        },
                    },
                )

            else:
                await self.send_message(
                    client_id=client_id,
                    message={
                        "error": {
                            "error_message": f"Unexpected exception: {message}",
                            "error_type": ErrorType.AGENT_GENERAL_ERROR.value,
                        }
                    },
                )

    async def send_message(self, client_id: str, message: str | dict):
        """
        Sends a message to the specified client if the connection exists.

        Args:
            client_id (str): The client ID to which the message should be sent.
            message (str | dict): The message content, can be a string or a dictionary.
        """
        message = json.dumps(message) if isinstance(message, dict) else message
        logging.info(f"Sending message: {message}, to: {client_id}")
        if websocket := self.active_connections.get(client_id):
            await websocket.send_text(message)

    async def connect(self, websocket: WebSocket) -> str:
        """
        Accepts a new WebSocket connection and assigns a client ID based on headers.

        Args:
            websocket (WebSocket): The WebSocket connection instance.

        Returns:
            str: The resolved client ID.
        """
        client_id = None
        agent_jwt = None

        if api_key := websocket.headers.get("api-key"):
            client_id = self.MASTER_SERVERS_API_KEY_MAPPING.get(api_key)

        elif agent_jwt := websocket.headers.get("x-custom-authorization"):
            try:
                decoded = jwt.decode(
                    agent_jwt, options={"verify_signature": False}, algorithms=["HS256"]
                )
                client_id = decoded.get("sub")
            except jwt.DecodeError:
                client_id = agent_jwt
        elif invoke_key := websocket.headers.get("x-custom-invoke-key"):
            client_id = invoke_key

        await websocket.accept()
        self.active_connections[client_id] = websocket
        return client_id, agent_jwt

    async def disconnect(self, client_id: str):
        """
        Disconnects a client and notifies relevant parties about the unregistration.

        Args:
            client_id (str): The ID of the client to disconnect.
        """
        if client_id not in self.active_connections:
            return

        del self.active_connections[client_id]

        if not client_id.startswith(
            app_settings.MASTER_BE_API_KEY
        ):  # Ignore sockets from Master BE
            await self.send_message(
                client_id=MasterServerName.MASTER_SERVER_BE.value,
                message={
                    "request_payload": {
                        "agent_uuid": client_id,
                        "message_type": WSMessageType.AGENT_UNREGISTER.value,
                    }
                },
            )

        for connection_id in (
            self.active_connections
        ):  # Clean up all connections created via session.send
            if client_id in connection_id:
                await self.send_message(
                    client_id=connection_id,
                    message={
                        "message_type": WSMessageType.AGENT_ERROR.value,
                        "error": {
                            "error_message": "Agent has been unregistered",
                            "agent_uuid": client_id,
                        },
                    },
                )
