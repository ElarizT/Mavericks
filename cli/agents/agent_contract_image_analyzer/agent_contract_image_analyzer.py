import asyncio
import base64
import io
import json
import re
from typing import Any, Annotated, List, Dict, Optional
from datetime import datetime

import cv2
import numpy as np
import pytesseract
from PIL import Image
import requests
import aiohttp
from bs4 import BeautifulSoup
from genai_session.session import GenAISession
from genai_session.utils.context import GenAIContext
from tavily import TavilyClient
from duckduckgo_search import DDGS
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")

# Initialize clients  
tavily_client = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None

AGENT_JWT = ""  # noqa: E501

session = GenAISession(jwt_token=AGENT_JWT)

# Legal contract analysis system prompt
LEGAL_ANALYSIS_PROMPT = """
You are an expert legal AI assistant specializing in contract and agreement analysis. Your role is to:

1. **IDENTIFY HARMFUL CLAUSES**: Look for terms that could be unfavorable, unfair, or potentially harmful to the user:
   - Excessive penalties or fees
   - Unreasonable termination clauses
   - Liability limitations favoring only one party
   - Automatic renewal terms
   - Unclear or ambiguous language
   - Privacy violations
   - Unfair dispute resolution clauses
   - Hidden costs or charges
   - Restrictions on user rights
   - Warranty disclaimers

2. **RISK ASSESSMENT**: Categorize risks as:
   - **HIGH RISK**: Potentially severe financial or legal consequences
   - **MEDIUM RISK**: Notable concerns that should be addressed
   - **LOW RISK**: Minor issues worth noting

3. **RECOMMENDATIONS**: Provide specific, actionable next steps:
   - Negotiate specific terms
   - Seek legal counsel for complex issues
   - Request clarification on ambiguous terms
   - Consider alternative providers/agreements
   - Document concerns in writing

4. **LEGAL CONTEXT**: Use recent legal precedents and regulations to provide informed analysis.

Format your response as:
## HARMFUL CLAUSES IDENTIFIED
[List specific problematic clauses with explanations]

## RISK ASSESSMENT
[Categorize and explain each risk level]

## RECOMMENDED NEXT STEPS
[Specific actionable recommendations]

## LEGAL CONTEXT
[Relevant laws, regulations, or precedents]

Be thorough, clear, and user-focused in your analysis.
"""

class ImageProcessor:
    """Handles image processing and OCR extraction"""
    
    @staticmethod
    def preprocess_image(image: Image.Image) -> Image.Image:
        """Enhance image quality for better OCR results"""
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Convert PIL to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Apply image enhancement techniques
        # Denoise
        denoised = cv2.fastNlMeansDenoising(opencv_image)
        
        # Increase contrast and brightness
        alpha = 1.5  # Contrast control
        beta = 10    # Brightness control
        enhanced = cv2.convertScaleAbs(denoised, alpha=alpha, beta=beta)
        
        # Apply adaptive thresholding
        gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Convert back to PIL
        return Image.fromarray(thresh)
    
    @staticmethod
    def extract_text_from_image(image: Image.Image) -> str:
        """Extract text from image using OCR"""
        try:
            # Preprocess the image
            processed_image = ImageProcessor.preprocess_image(image)
            
            # Configure Tesseract for better accuracy
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?;:()[]{}"-/$%&@#*+=<>'
            
            # Extract text
            text = pytesseract.image_to_string(processed_image, config=custom_config)
            
            # Clean and normalize text
            text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
            text = text.strip()
            
            return text
        except Exception as e:
            logger.error(f"OCR extraction failed: {str(e)}")
            return ""

class WebSearcher:
    """Handles web search for legal information"""
    
    @staticmethod
    async def search_tavily(query: str, max_results: int = 5) -> List[Dict]:
        """Search using Tavily API"""
        if not tavily_client:
            return []
        
        try:
            search_result = tavily_client.search(
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_domains=["law.com", "legal.com", "findlaw.com", "justia.com", "nolo.com"]
            )
            return search_result.get("results", [])
        except Exception as e:
            logger.error(f"Tavily search failed: {str(e)}")
            return []
    
    @staticmethod
    async def search_duckduckgo(query: str, max_results: int = 5) -> List[Dict]:
        """Search using DuckDuckGo"""
        try:
            ddg = DDGS()
            results = []
            
            # Perform text search
            search_results = ddg.text(
                keywords=query + " law legal regulation 2024 2025",
                max_results=max_results,
                backend="api"
            )
            
            for result in search_results:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("href", ""),
                    "content": result.get("body", "")
                })
            
            return results
        except Exception as e:
            logger.error(f"DuckDuckGo search failed: {str(e)}")
            return []
    
    @staticmethod
    async def get_recent_legal_info(contract_type: str, jurisdiction: str = "general") -> str:
        """Get recent legal information related to contract type"""
        queries = [
            f"{contract_type} contract law updates 2024 2025",
            f"recent {contract_type} legal cases rulings",
            f"{contract_type} consumer protection laws {jurisdiction}",
            f"unfair contract terms {contract_type} regulations"
        ]
        
        all_results = []
        
        for query in queries:
            # Try Tavily first, then DuckDuckGo as fallback
            tavily_results = await WebSearcher.search_tavily(query, 3)
            if tavily_results:
                all_results.extend(tavily_results)
            else:
                ddg_results = await WebSearcher.search_duckduckgo(query, 3)
                all_results.extend(ddg_results)
        
        # Compile search results into context
        context = f"Recent legal information for {contract_type} contracts:\n\n"
        for i, result in enumerate(all_results[:10], 1):
            context += f"{i}. {result.get('title', 'No title')}\n"
            context += f"   {result.get('content', 'No content')[:200]}...\n\n"
        
        return context

class ContractAnalyzer:
    """Main contract analysis engine"""
    
    @staticmethod
    def detect_contract_type(text: str) -> str:
        """Detect the type of contract from text content"""
        text_lower = text.lower()
        
        contract_patterns = {
            "rental": ["rent", "lease", "landlord", "tenant", "property"],
            "employment": ["employment", "employee", "employer", "salary", "wages"],
            "service": ["service", "provider", "client", "delivery"],
            "purchase": ["purchase", "buy", "sell", "goods", "product"],
            "insurance": ["insurance", "policy", "coverage", "premium"],
            "loan": ["loan", "credit", "interest", "repayment"],
            "subscription": ["subscription", "monthly", "annual", "recurring"],
            "terms of service": ["terms", "service", "user", "account", "platform"],
            "privacy policy": ["privacy", "data", "information", "personal"]
        }
        
        for contract_type, keywords in contract_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                return contract_type
        
        return "general agreement"
    
    @staticmethod
    async def analyze_contract_with_llm(text: str, legal_context: str) -> str:
        """Analyze contract using the default GenAI model"""
        try:
            analysis_prompt = f"""
{LEGAL_ANALYSIS_PROMPT}

CONTRACT TEXT:
{text}

RECENT LEGAL CONTEXT:
{legal_context}

Please analyze this contract thoroughly and provide your findings in the specified format.
"""
            
            # Use the GenAI session to analyze the contract
            # This will use the default configured model (gpt-4o)
            temp_session = GenAISession(jwt_token="")
            
            # Create a simple analysis request
            response = await temp_session.achat(
                messages=[
                    {"role": "system", "content": LEGAL_ANALYSIS_PROMPT},
                    {"role": "user", "content": analysis_prompt}
                ]
            )
            
            return response
        except Exception as e:
            logger.error(f"LLM analysis failed: {str(e)}")
            return f"Analysis failed: {str(e)}"

@session.bind(
    name="agent_contract_image_analyzer",
    description="Analyzes contracts and agreements from uploaded images, identifies harmful clauses, and provides legal recommendations with web-sourced legal context"
)
async def agent_contract_image_analyzer(
    agent_context: GenAIContext,
    file_ids: Annotated[List[str], "List of image file IDs to analyze"],
    jurisdiction: Annotated[str, "Legal jurisdiction (e.g., 'US', 'EU', 'UK', 'general')"] = "general",
    analysis_focus: Annotated[str, "Specific focus areas (e.g., 'consumer protection', 'privacy', 'financial terms')"] = "general"
) -> Dict[str, Any]:
    """
    Analyze contract images for harmful clauses and legal risks
    """
    agent_context.logger.info("Starting contract image analysis")
    
    try:
        if not agent_context.files or not file_ids:
            return {"error": "No files uploaded or file IDs provided"}
        
        results = {
            "analysis_timestamp": datetime.now().isoformat(),
            "jurisdiction": jurisdiction,
            "analysis_focus": analysis_focus,
            "processed_images": [],
            "extracted_text": "",
            "contract_type": "",
            "legal_analysis": "",
            "legal_context": "",
            "summary": {}
        }
        
        all_extracted_text = []
        
        # Process each uploaded image
        for file_id in file_ids:
            try:
                file_info = await agent_context.files.get_by_id(file_id)
                file_content = file_info.read()
                
                # Load image
                image = Image.open(io.BytesIO(file_content))
                
                # Extract text using OCR
                extracted_text = ImageProcessor.extract_text_from_image(image)
                
                if extracted_text:
                    all_extracted_text.append(extracted_text)
                    results["processed_images"].append({
                        "file_id": file_id,
                        "filename": getattr(file_info, 'name', f'image_{file_id}'),
                        "text_length": len(extracted_text),
                        "status": "success"
                    })
                else:
                    results["processed_images"].append({
                        "file_id": file_id,
                        "filename": getattr(file_info, 'name', f'image_{file_id}'),
                        "status": "no_text_found"
                    })
                    
            except Exception as e:
                logger.error(f"Failed to process image {file_id}: {str(e)}")
                results["processed_images"].append({
                    "file_id": file_id,
                    "status": "error",
                    "error": str(e)
                })
        
        if not all_extracted_text:
            return {"error": "No text could be extracted from the uploaded images"}
        
        # Combine all extracted text
        combined_text = "\n\n".join(all_extracted_text)
        results["extracted_text"] = combined_text
        
        # Detect contract type
        contract_type = ContractAnalyzer.detect_contract_type(combined_text)
        results["contract_type"] = contract_type
        
        # Get recent legal context
        legal_context = await WebSearcher.get_recent_legal_info(contract_type, jurisdiction)
        results["legal_context"] = legal_context
        
        # Perform legal analysis
        analysis = await ContractAnalyzer.analyze_contract_with_llm(combined_text, legal_context)
        results["legal_analysis"] = analysis
        
        # Create summary
        results["summary"] = {
            "total_images_processed": len([img for img in results["processed_images"] if img["status"] == "success"]),
            "contract_type": contract_type,
            "text_extracted": len(combined_text) > 0,
            "legal_context_available": len(legal_context) > 0,
            "analysis_completed": len(analysis) > 0
        }
        
        agent_context.logger.info(f"Contract analysis completed for {len(file_ids)} images")
        return results
        
    except Exception as e:
        agent_context.logger.error(f"Contract analysis failed: {str(e)}")
        return {"error": f"Analysis failed: {str(e)}"}

async def main():
    print(f"Contract Image Analyzer Agent started")
    await session.process_events()

if __name__ == "__main__":
    asyncio.run(main())
