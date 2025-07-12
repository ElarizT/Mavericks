
"""
Use Legal-BERT and rule-based methods to identify risky clauses.
"""
from transformers import pipeline
import re

classifier = pipeline("zero-shot-classification", model="nlpaueb/legal-bert-base-uncased")
RISK_TOPICS = ["automatic renewal", "unlimited liability", "termination", "data usage"]

def detect_risks(text):
    clauses = re.split(r"\n\n+", text)
    risky = []
    for clause in clauses:
        result = classifier(clause, RISK_TOPICS)
        if result['scores'][0] > 0.6:
            risky.append((clause, result['labels'][0], result['scores'][0]))
    return risky
