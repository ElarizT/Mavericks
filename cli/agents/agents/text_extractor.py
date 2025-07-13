import os
import textract
from docx import Document
from PyPDF2 import PdfReader

def extract_text_from_file(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()

    try:
        if ext == ".docx":
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        elif ext == ".pdf":
            reader = PdfReader(file_path)
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif ext in [".txt"]:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            # fallback using textract (requires external dependencies)
            return textract.process(file_path).decode("utf-8")
    except Exception as e:
        return f"❌ Error extracting text: {e}"
