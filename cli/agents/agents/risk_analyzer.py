"""
Analyze the risk of a simplified clause using rule-based heuristics.
"""

import re

def assess_risk(clause: str, explanation: str, urgency: str, focus: str) -> tuple:
    """
    Determine the risk level of a clause based on keywords and urgency level.

    Returns a tuple: (risk_level, explanation)
    """

    clause_lower = clause.lower()
    explanation_lower = explanation.lower()
    combined = f"{clause_lower} {explanation_lower}"

    # Split and normalize focus areas
    focus_areas = [word.strip().lower() for word in focus.split(",") if word.strip()]
    
    high_risk_keywords = [
        "unlimited liability", "termination without cause", "penalty",
        "non-refundable", "forfeited", "binding arbitration", "no liability",
        "auto-renew", "cross-border restriction", "entire liability",
        "non-compete", "no refund", "over speed fine", "security forfeited"
    ]

    medium_risk_keywords = [
        "termination", "limited liability", "intellectual property", 
        "payment terms", "governing law", "late return", "fees", "restrictions"
    ]

    # Weight modifiers based on urgency
    urgency_weight = {
        "low": 0.8,
        "medium": 1.0,
        "high": 1.2
    }
    weight = urgency_weight.get(urgency.lower(), 1.0)

    # Check for focus keyword match
    focus_hits = sum(1 for focus_kw in focus_areas if focus_kw in combined)
    high_hits = sum(1 for kw in high_risk_keywords if kw in combined)
    med_hits = sum(1 for kw in medium_risk_keywords if kw in combined)

    score = (2 * high_hits + 1 * med_hits + 1.5 * focus_hits) * weight

    # Classify based on score thresholds
    if score >= 4:
        risk = "High"
    elif score >= 2:
        risk = "Medium"
    else:
        risk = "Low"

    return risk, explanation.strip().replace(" .", ".")
