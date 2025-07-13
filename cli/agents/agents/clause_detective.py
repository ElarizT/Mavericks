"""
Use Legal-BERT and rule-based methods to identify risky clauses.
"""

from transformers import pipeline
import re

# Load zero-shot classification pipeline with Legal-BERT
classifier = pipeline(
    "zero-shot-classification",
    model="nlpaueb/legal-bert-base-uncased",
    local_files_only=True
)


RISK_TOPICS = ["automatic renewal", "unlimited liability", "termination", "data usage"]

def split_into_clauses(text: str) -> list:
    """
    Naively split the input contract text into clauses using double line breaks or full stops.
    """
    text = text.strip()
    if not text:
        return []

    # Split using paragraphs or semantically complete lines
    raw_clauses = re.split(r'\n{2,}|\.\s+', text)
    clauses = [clause.strip() for clause in raw_clauses if len(clause.strip()) > 20]
    return clauses

def detect_risks(text):
    """
    Run Legal-BERT zero-shot classification to tag risky clauses.
    """
    clauses = split_into_clauses(text)
    risky = []
    for clause in clauses:
        result = classifier(clause, RISK_TOPICS)
        if result['scores'][0] > 0.6:
            risky.append((clause, result['labels'][0], result['scores'][0]))
    return risky
