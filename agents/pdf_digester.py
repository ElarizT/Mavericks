"""
Extract text from PDFs, images, or DOCX documents.
"""

import pytesseract
from PyPDF2 import PdfReader
from PIL import Image
import io
import os
import docx2txt

def extract_text_from_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text
        print(f"\n📄 Extracted text from PDF ({file_path}):\n{text[:1000]}")
    except Exception as e:
        print(f"❌ Failed to extract text from PDF: {e}")
    return text

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        print(f"\n🖼️ Extracted text from image ({image_path}):\n{text[:1000]}")
        return text
    except Exception as e:
        print(f"❌ Failed to extract text from image: {e}")
        return ""

def extract_text_from_docx(docx_path):
    try:
        text = docx2txt.process(docx_path)
        print(f"\n📝 Extracted text from DOCX ({docx_path}):\n{text[:1000]}")
        return text
    except Exception as e:
        print(f"❌ Failed to extract text from DOCX: {e}")
        return ""

def extract_text_auto(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
