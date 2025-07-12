 🤖 Contract Risk Finder

**Contract Risk Finder** is an AI-powered tool that automatically analyzes legal contracts (PDF/DOCX), detects risky clauses, simplifies them into plain English using GenAI, and generates a polished PDF report.

---

## 🚀 Features

- 📄 **Text Extraction** from PDF and DOCX contracts
- 🔍 **Clause Risk Detection** using Legal-BERT or fallback keyword detection
- ✨ **Plain English Simplification** with GenAI
- 🧾 **Polished PDF Report Generation**
- 🤝 **AgentOS Integration** (via `genai-agentos` and `master_agent`)
- 🔁 **Fallback Mode** for zero-shot clause identification

---

## 🧠 Architecture

```mermaid
graph TD
    A[User Uploads Contract] --> B[Extract Text (pdf/docx)]
    B --> C[Risk Detector Agent]
    C -->|None Found| D[Fallback Detector (Keywords)]
    C -->|Risks Found| E[Clause Simplifier Agent (GenAI)]
    D --> E
    E --> F[PDF Report Generator]
    F --> G[Download Polished Risk Report]
🗂️ Folder Structure

contract-risk-finder/
│
├── app/                  # FastAPI app (main.py)
├── agents/               # Risk detector, simplifier, summarizer
├── master_agent/         # GenAI invoke_model orchestrator
├── genai-agentos/        # Optional AgentOS integration logic
├── models/               # Optional pretrained model configs
├── reports/              # Auto-generated PDFs (gitignored)
├── utils/                # Helper functions
├── data/                 # Optional static content
├── temp/                 # Temp uploaded files (gitignored)
│
├── requirements.txt      # Python dependencies
├── Dockerfile            # For containerized deployment
└── README.md             # You're reading it!
⚙️ Setup Instructions
✅ Clone the Repo
git clone https://github.com/yourusername/contract-risk-finder.git
cd contract-risk-finder
✅ Create Virtual Environment

python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
✅ Install Requirements
pip install -r requirements.txt
✅ Run the API
uvicorn app.main:app --reload
Visit: http://127.0.0.1:8000/docs for Swagger UI.

🧪 Sample API Usage (cURL)
curl -X 'POST' \
  'http://127.0.0.1:8000/analyze' \
  -F 'file=@path_to_your_contract.docx'
📦 Docker (Optional)
docker build -t contract-risk-finder .
docker run -p 8000:8000 contract-risk-finder
📑 License
This project is licensed under the MIT License. See LICENSE file.

💡 Future Enhancements
 Add multi-language support (e.g., Hindi)

 Highlight risky clauses in uploaded documents

 Integration with contract signing platforms (e.g., DocuSign)

 Logging & audit reports

🙌 Credits
Built using:

FastAPI

HuggingFace Transformers (Legal-BERT)

GenAI AgentOS (via master_agent)

PyPDF2 / python-docx

FPDF for PDF generation
