from transformers import pipeline, Pipeline
from typing import Optional

# Load the summarizer once at import
try:
    summarizer: Pipeline = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    print("✅ Summarization model loaded successfully.")
except Exception as e:
    summarizer = None
    print(f"⚠️ Failed to load summarization model: {e}")

def invoke_model(text: str) -> str:
    """
    Uses a pretrained summarization model to simplify legal clauses.
    Returns a concise explanation in plain English.
    """
    if not text or not text.strip():
        return "⚠️ No clause provided for simplification."

    if summarizer is None:
        return "⚠️ Summarization model is not loaded."

    try:
        clean_text = text.strip().replace("\n", " ")
        result = summarizer(
            clean_text,
            max_length=120,
            min_length=30,
            do_sample=False
        )
        return result[0]['summary_text'].strip()
    except Exception as e:
        return f"⚠️ Error during clause simplification: {str(e)}"
