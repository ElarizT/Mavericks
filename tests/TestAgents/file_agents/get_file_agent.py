from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
import asyncio


genai_session = GenAISession(jwt_token="d13c7f06-819e-403a-ae69-5d71ef929ac8")


@genai_session.bind(name="Getter", description="Gets file")
async def get_handler(agent_context: GenAIContext, file_id: str) -> dict:

    file = await agent_context.files.get_by_id(file_id)

    print(file)

    metadata = await agent_context.files.get_metadata_by_id(file_id)

    print(metadata)

    return metadata


async def main():

    await genai_session.process_events()


if __name__ == "__main__":

    asyncio.run(main())
