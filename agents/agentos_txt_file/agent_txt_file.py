import asyncio
from typing import Any, Annotated
from genai_session.session import GenAISession
 
AGENT_JWT = "" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="agent_txt_file",
    description="Read text files"
)

async def read_text_file(
        agent_context,
        file_id: Annotated[str, "ID of the file to read"]
) -> dict[str, Any]:
    file = await agent_context.files.get_by_id(file_id)
    file_content = file.read().decode("utf-8")
    return file_content



async def main():
    print(f"Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
