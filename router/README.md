# 🧠 Agent WebSocket API - Router

This FastAPI-based WebSocket server manages agent connections and communication between AI agents and master servers.\
It supports agent registration, invocation, logging, and graceful error handling via structured WebSocket message types.

---

## 📦 Features

- 🔌 **WebSocket Agent Management**  
  Accepts and manages WebSocket connections from AI agents and master services.

- 📬 **Message Routing**  
  Routes registration, invocation, response, and log messages between agents and master servers.

- 🚫 **Error Handling**  
  Sends structured error messages for issues like invalid JSON, inactive agents, or missing payloads.

- 🛠️ **Extensible Enum-Based Protocol**  
  Clean and centralized definition of all supported message types and errors using Python `Enum`.

---


## 📤 Message Types

Defined in `WSMessageType` enum:

| Type              | Description                          |
|-------------------|--------------------------------------|
| `agent_register`  | Agent registers itself               |
| `agent_unregister`| Agent disconnects                    |
| `agent_invoke`    | Master server sends a request to agent |
| `agent_response`  | Agent responds to a previous request |
| `agent_error`     | Agent reports an error               |
| `agent_log`       | Agent sends log/info messages        |
| `ml_invoke`       | Reserved for future ML-specific logic |

---

## ⚠️ Error Types

Defined in `ErrorType` enum:

| Error Code                    | Description                          |
|------------------------------|--------------------------------------|
| `AgentUUIDError`             | Invalid or missing agent ID          |
| `AgentGeneralError`          | Unexpected exception                 |
| `AgentNotActive`             | Invoked agent is not connected       |
| `InvalidJSONRequestFormat`   | Invalid or malformed JSON message    |
| `NoRequestPayload`           | Missing payload for agent invocation |

---

## 🧠 Master Servers

Defined in `MasterServerName` enum:

| Name                | Purpose                           |
|---------------------|-----------------------------------|
| `master_server_be`  | Backend / business logic handler  |
| `master_server_ml`  | ML agent service aka Master Agent |

These are identified via API keys set in environment variables.
