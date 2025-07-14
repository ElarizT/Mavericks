# Contract Image Analyzer Agent

An AI-powered agent that analyzes contracts and legal agreements from uploaded images, identifies potentially harmful clauses, and provides legal recommendations with up-to-date legal context.

## Features

### 🔍 **Advanced Image Processing**
- **OCR Text Extraction**: Uses Tesseract OCR with image preprocessing for optimal text recognition
- **Multi-Image Support**: Processes multiple contract images simultaneously
- **Image Enhancement**: Automatic denoising, contrast adjustment, and adaptive thresholding

### ⚖️ **Legal Analysis**
- **Harmful Clause Detection**: Identifies unfavorable terms, excessive penalties, unclear language
- **Risk Assessment**: Categorizes risks as HIGH, MEDIUM, or LOW priority
- **Contract Type Detection**: Automatically identifies rental, employment, service, purchase agreements, etc.
- **Jurisdiction-Aware**: Tailors analysis to specific legal jurisdictions

### 🌐 **Real-Time Legal Context**
- **Web Search Integration**: Uses Tavily + DuckDuckGo for recent legal information
- **Current Law Updates**: Searches for 2024-2025 legal precedents and regulations
- **Consumer Protection Focus**: Emphasizes user protection and fair contract terms

### 🤖 **AI-Powered Analysis**
- **Groq LLM**: Uses Mistral-Saba-24B model for comprehensive legal analysis
- **Structured Output**: Provides organized recommendations and next steps
- **Actionable Advice**: Specific guidance on negotiation and risk mitigation

## Usage

### Input Parameters
- `file_ids`: List of uploaded image file IDs containing contract text
- `jurisdiction`: Legal jurisdiction ("US", "EU", "UK", "general") - default: "general"
- `analysis_focus`: Specific focus areas ("consumer protection", "privacy", "financial terms") - default: "general"

### Example Usage
```python
result = await agent_contract_image_analyzer(
    agent_context,
    file_ids=["image1_id", "image2_id"],
    jurisdiction="US",
    analysis_focus="consumer protection"
)
```

### Output Structure
```json
{
    "analysis_timestamp": "2025-01-13T...",
    "jurisdiction": "US",
    "analysis_focus": "consumer protection",
    "processed_images": [...],
    "extracted_text": "Combined text from all images",
    "contract_type": "rental",
    "legal_analysis": "Detailed analysis with harmful clauses, risks, and recommendations",
    "legal_context": "Recent legal information and precedents",
    "summary": {
        "total_images_processed": 2,
        "contract_type": "rental",
        "text_extracted": true,
        "legal_context_available": true,
        "analysis_completed": true
    }
}
```

## Dependencies

### Core Dependencies
- `genai-protocol`: Agent framework integration
- `groq`: Groq LLM API client
- `pytesseract`: OCR text extraction
- `pillow`: Image processing
- `opencv-python`: Advanced image preprocessing

### Web Search
- `tavily-python`: Primary web search (requires API key)
- `duckduckgo-search`: Fallback search (free)
- `beautifulsoup4`: Web content parsing

### Utilities
- `loguru`: Advanced logging
- `python-dotenv`: Environment configuration
- `aiohttp`: Async HTTP requests

## Installation

1. **Install System Dependencies**:
   ```bash
   # Windows (using chocolatey)
   choco install tesseract
   
   # Or download from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

2. **Install Python Dependencies**:
   ```bash
   cd agent_contract_image_analyzer
   pip install -e .
   ```

3. **Configure Environment**:
   ```bash
   # Copy and edit .env file
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Configuration

### Required Environment Variables
- `GROQ_API_KEY`: Your Groq API key (provided)
- `AGENT_JWT`: Agent authentication token

### Optional Environment Variables
- `TAVILY_API_KEY`: Enhanced web search capabilities
- `TESSERACT_CMD`: Custom Tesseract installation path

## Supported Contract Types

The agent automatically detects and analyzes various contract types:

- **Rental/Lease Agreements**: Property rentals, vehicle leases
- **Employment Contracts**: Job agreements, non-compete clauses
- **Service Agreements**: Professional services, SaaS terms
- **Purchase Agreements**: Goods, equipment, software licenses
- **Insurance Policies**: Coverage terms, exclusions
- **Loan Agreements**: Credit terms, repayment conditions
- **Subscription Services**: Recurring billing, cancellation terms
- **Terms of Service**: Platform usage, user agreements
- **Privacy Policies**: Data handling, user rights

## Risk Categories

### HIGH RISK 🔴
- Severe financial penalties
- Unlimited liability exposure
- Automatic binding renewals
- Waived consumer rights

### MEDIUM RISK 🟡
- Unclear termination terms
- Limited warranty coverage
- Dispute resolution restrictions
- Privacy concerns

### LOW RISK 🟢
- Minor administrative requirements
- Standard industry terms
- Reasonable notice periods

## Legal Disclaimer

This tool provides informational analysis only and should not be considered legal advice. Always consult with qualified legal professionals for important contract decisions.

## Support

For technical issues or feature requests, please contact the development team or submit an issue in the project repository.
