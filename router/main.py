import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from connectors.ws_connector_manager import WSConnectionManager
from utils.pydantic_models import Message, MessageResponse

app = FastAPI(
    title="Agent WebSocket API",
    description="Server manages WebSocket agents' connections and message processing.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Manages WebSocket connections and routes messages
ws_connection_manager = WSConnectionManager()


@app.websocket(path="/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for agent connections.

    Handles connecting, receiving, and processing WebSocket messages from clients (agents),
    and ensures cleanup on disconnect.

    Args:
        websocket (WebSocket): The incoming WebSocket connection.
    """
    client_id, agent_jwt = await ws_connection_manager.connect(websocket)

    if not client_id:
        # Reject connection if no valid authorization header
        await websocket.close(code=4000, reason="Missing Authorization header")
    else:
        try:
            # Continuously listen for messages
            while True:
                data = await websocket.receive_text()
                await ws_connection_manager.process_message(
                    client_id, data, agent_jwt=agent_jwt
                )
        except WebSocketDisconnect:
            # Handle client disconnection
            await ws_connection_manager.disconnect(client_id)


@app.post(
    path="/invoke-agent",
    response_model=MessageResponse,
    summary="Send message to a connected agent",
)
async def invoke_agent(message: Message) -> MessageResponse:
    await ws_connection_manager.send_message(message.client_id, message.message)
    return MessageResponse(detail=f"Message sent to client {message.client_id}")


if __name__ == "__main__":
    # Run the FastAPI app using Uvicorn on port 8080 with auto-reload
    uvicorn.run("main:app", port=8080, reload=True)
