import asyncio
from typing import Any, Annotated
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
import fitz  # PyMuPDF
import io

AGENT_JWT = "" # noqa: E501

session = GenAISession(jwt_token=AGENT_JWT)

@session.bind(
    name="agent_pdf_reader",
    description="Reads and extracts text from an uploaded PDF file"
)
async def agent_pdf_reader(
    agent_context, 
    file_id: Annotated[str, "ID of the file to read"],
)->dict[str, Any]:
    agent_context.logger.info("Inside agent_pdf_reader")

    try:
        if not agent_context.files:
            return "No file uploaded."

        # Assuming only one file is uploaded
        file_info = await agent_context.files.get_by_id(file_id)
        file_content = file_info.read()  # Read binary content

        # Open the PDF from in-memory bytes
        doc = fitz.open(stream=file_content, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

        return full_text.strip() or "No text found in the PDF."
    except Exception as e:
        return f"Failed to read PDF: {str(e)}"

async def main():
    print(f"Agent with token '{AGENT_JWT}' started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
