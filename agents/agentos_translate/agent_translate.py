import asyncio
import os
from typing import Any, Annotated

from dotenv import load_dotenv
from genai_session.session import GenAISession
from openai import OpenAI

load_dotenv()

OPENAPI_KEY = os.environ.get("OPENAPI_KEY")

openai_client = OpenAI(
    api_key=OPENAPI_KEY
)

AGENT_JWT = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiMTMzN2NkMi05YTI0LTQxODktYWI5Ni1lM2NkNzgwMjhlYjMiLCJleHAiOjI1MzQwMjMwMDc5OSwidXNlcl9pZCI6ImUyMzFlYzg0LTc1NTYtNDVhOC05M2JkLWI5ZTdiZWY3MmNlZSJ9.sTrqPVG0WvDrCqANp9wfo_AjXSofTgKQR2Z9tXuagq8" # noqa: E501
session = GenAISession(jwt_token=AGENT_JWT)



@session.bind(name="get_translation", description="Translate the text into specified language")
async def get_translation(
        agent_context, text: Annotated[str, "Text to translate"],
        language: Annotated[str, "Code of the language to translate to (e.g. 'fr', 'es')"]
) -> dict[str, Any]:
    agent_context.logger.info("Inside get_translation")
    prompt = f"Translate the text into specified language {language}.\n\n{text}"

    response = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="gpt-4o-mini"
    )
    translation = response.choices[0].message.content
    return {"translation": translation}


async def main():
    print(f"Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
