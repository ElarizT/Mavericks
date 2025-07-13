import asyncio
from typing import Any, Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
import docx2txt

AGENT_JWT = "" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)


@session.bind(
    name="agent_doc_reader",
    description="Doc file reader"
)
async def agent_doc_reader(
 agent_context, 
    file_id: Annotated[str, "ID of the file to read"],
)->dict[str, Any]:
    agent_context.logger.info("Inside agent_doc_reader")

    try:
        if not agent_context.files:
            return "No file uploaded."

        # Assuming only one file is uploaded
        file_info = await agent_context.files.get_by_id(file_id)
        file_content = docx2txt.process(file_info)

        return file_content or "No text found in the Doc file."
    except Exception as e:
        return f"Failed to read DOC: {str(e)}"

async def main():
    print(f"Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
