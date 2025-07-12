from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from agents.pdf_digester import extract_text_from_pdf, extract_text_from_docx
from agents.clause_detective import detect_risks
from agents.plain_translator import simplify_clause
from agents.report_generator import generate_pdf_report
import os
import traceback
import uuid

app = FastAPI(title="Contract Risk Analyzer", description="Detects risky legal clauses and generates PDF reports.", version="1.0")


# Fallback risk detector based on keywords
def fallback_risk_detector(text: str):
    fallback_clauses = []
    risk_keywords = {
        "termination": "High",
        "arbitration": "Medium",
        "liability": "High",
        "indemnify": "High",
        "non-disclosure": "Low",
        "non-compete": "Medium",
    }

    for sentence in text.split("."):
        for keyword, risk in risk_keywords.items():
            if keyword in sentence.lower():
                fallback_clauses.append((sentence.strip(), risk, 0.9))
    return fallback_clauses


@app.post("/analyze", response_class=FileResponse)
async def analyze_contract(file: UploadFile = File(...)):
    # Handle temporary file path
    file_ext = file.filename.split(".")[-1].lower()
    temp_path = f"temp_{uuid.uuid4().hex[:8]}.{file_ext}"

    try:
        # Save uploaded file to disk
        with open(temp_path, "wb") as f:
            f.write(await file.read())

        # Step 1: Extract contract text
        if file_ext == "pdf":
            text = extract_text_from_pdf(temp_path)
        elif file_ext == "docx":
            text = extract_text_from_docx(temp_path)
        else:
            return JSONResponse(status_code=400, content={"error": "❌ Unsupported file format. Use PDF or DOCX."})

        if not text.strip():
            return JSONResponse(status_code=400, content={"error": "❌ Unable to extract text from the document."})

        print("📝 Extracted Text:\n", text)

        # Step 2: Detect risky clauses using model
        try:
            risks = detect_risks(text)
        except Exception as e:
            print("❌ Error in detect_risks:", traceback.format_exc())
            risks = []

        if not risks:
            print("⚠️ No risks detected by model. Using fallback keywords.")
            risks = fallback_risk_detector(text)

        # Step 3: Simplify each clause
        simplified = []
        for clause, risk_label, score in risks:
            try:
                explanation = simplify_clause(clause)
            except Exception as e:
                print("⚠️ Error simplifying clause:", traceback.format_exc())
                explanation = f"⚠️ Error simplifying clause: {e}"
            simplified.append((clause, risk_label, explanation))

        # Step 4: Generate PDF report and return as response
        pdf_path = generate_pdf_report(simplified)
        return FileResponse(
            path=pdf_path,
            filename=os.path.basename(pdf_path),
            media_type='application/pdf'
        )

    except Exception as e:
        print("❌ Unexpected error:", traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": f"Internal error: {e}"})

    finally:
        # Clean up uploaded file
        if os.path.exists(temp_path):
            os.remove(temp_path)
