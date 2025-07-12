"""
Simplify legal clauses into plain English using GenAI's built-in model.
"""

from master_agent.master import invoke_model
import difflib

def fallback_simplify(clause: str) -> str:
    """
    Rule-based fallback simplification for known risky terms.
    """
    clause_lower = clause.lower()
    if "liability" in clause_lower:
        return "You are fully responsible for anything that happens if the car is taken outside India without approval."
    elif "termination" in clause_lower:
        return "Either side can end the contract by giving a short written notice."
    elif "arbitration" in clause_lower:
        return "Disputes will be resolved outside court by a private arbitrator."
    elif "indemnify" in clause_lower:
        return "You agree to cover any losses or costs the other party faces."
    elif "non-disclosure" in clause_lower:
        return "You must keep shared information confidential."
    elif "non-compete" in clause_lower:
        return "You cannot work with competitors for a specific time."
    return "This clause may pose legal risks and should be reviewed carefully."

def simplify_clause(clause: str) -> str:
    """
    Takes a raw legal clause and returns a plain English explanation.
    Uses invoke_model() to generate the simplified output.
    Falls back to rule-based logic if result is too similar or invalid.
    """
    try:
        cleaned_clause = clause.strip()
        if not cleaned_clause:
            return "⚠️ Clause is empty."

        response = invoke_model(cleaned_clause)

        if isinstance(response, str):
            cleaned_response = response.strip().replace(" .", ".")
            
            # Use difflib to compare similarity
            similarity = difflib.SequenceMatcher(None, cleaned_clause.lower(), cleaned_response.lower()).ratio()
            if similarity > 0.85:
                return fallback_simplify(cleaned_clause)
            return cleaned_response

        return "⚠️ No valid explanation returned by the model."

    except Exception as e:
        return f"⚠️ Error during clause simplification: {str(e)}"
