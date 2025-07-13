from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
import aiofiles
import asyncio
import os


genai_session = GenAISession(jwt_token="720344df-033c-4700-9b79-832917f86895")


@genai_session.bind(name="Saver", description="Saves file")
async def save_handler(agent_context: GenAIContext, filename: str) -> dict:

    print(os.path.exists(filename))

    print(os.path.isfile(filename))

    async with aiofiles.open(filename, mode="rb") as file:

        content = await file.read()

    print(type(content))

    print(content)

    print(f"Saving file with new name: {filename}")

    file_id = await agent_context.files.save(content=content, filename=filename)

    print(file_id)

    file_metadata_from_agent = await genai_session.send(
        message={"file_id": file_id}, client_id="d13c7f06-819e-403a-ae69-5d71ef929ac8"
    )

    agent_context.logger.info(f"File was saved: {file_id}")

    agent_context.logger.info(f"File metadata: {file_metadata_from_agent.response}")

    return {"file_id": file_id, "file_metadata_from_agent": file_metadata_from_agent.response}


async def main():

    await genai_session.process_events()


if __name__ == "__main__":

    asyncio.run(main())
