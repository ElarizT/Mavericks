from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
import asyncio


session = GenAISession(jwt_token="d13c7f06-819e-403a-ae69-5d71ef929ac8")


@session.bind(name="I/O agent", description="Agent to test I/O")
async def message_handler(agent_context: GenAIContext, input: str) -> dict:
    
    agent_uuid = agent_context.agent_uuid

    print(f"\nAgent {agent_uuid} is up")
    
    type_name = type(input).__name__
    
    print(f"Received '{type_name}': {input}\n")
    
    return input


async def main():

    await session.process_events()


if __name__ == "__main__":

    asyncio.run(main())
