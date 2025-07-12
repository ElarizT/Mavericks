from fpdf import FPDF
import uuid
import os
from unidecode import unidecode  # ✅ Add this

def generate_pdf_report(simplified_clauses: list) -> str:
    def polish(text: str) -> str:
        if "⚠️" in text:
            return "Unable to simplify this clause due to a processing error."
        return text.strip().replace(" .", ".")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Contract Risk Analysis Report", ln=True, align='C')
    pdf.ln(10)

    for clause, risk, explanation in simplified_clauses:
        cleaned_explanation = polish(explanation)

        # ✅ Convert Unicode to ASCII-safe strings
        clause_ascii = unidecode(clause)
        risk_ascii = unidecode(risk)
        explanation_ascii = unidecode(cleaned_explanation)

        pdf.set_font("Arial", style='B', size=12)
        pdf.multi_cell(0, 10, f"Clause:\n{clause_ascii}")
        
        pdf.set_font("Arial", style='', size=12)
        pdf.cell(0, 10, f"Risk Level: {risk_ascii}", ln=True)
        pdf.multi_cell(0, 10, f"Explanation:\n{explanation_ascii}")
        pdf.ln(5)

    os.makedirs("reports", exist_ok=True)
    filename = f"report_{uuid.uuid4().hex[:8]}.pdf"
    output_path = os.path.join("reports", filename)
    pdf.output(output_path)

    return output_path
