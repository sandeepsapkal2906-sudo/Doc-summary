from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import tempfile
from typing import Optional
from datetime import datetime
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import our service modules
from app.services.document_processor import DocumentProcessor
from app.services.summarizer import Summarizer
from app.services.spell_checker import SpellCheckService
from app.models.schemas import SummaryResponse

# Initialize FastAPI app
app = FastAPI(
    title="Document Summarizer API",
    description="Local document summarization and insights extraction with spell check",
    version="1.0.0"
)

# CORS middleware - allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3030", "http://localhost:3031"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
doc_processor = DocumentProcessor()
summarizer = Summarizer()
spell_checker = SpellCheckService()

# Create upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Document Summarizer API",
        "status": "running",
        "version": "1.0.0",
        "features": ["PDF support", "DOCX support", "Local processing", "No cloud uploads", "Spell checking"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document
    
    Supported formats: PDF, DOCX
    """
    temp_path = None
    try:
        # Validate file type
        if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            if not (file.filename.endswith(".pdf") or file.filename.endswith(".docx")):
                raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
        
        # Create temporary file
        temp_path = os.path.join(UPLOAD_DIR, file.filename)
        
        # Save uploaded file
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Extract text from document
        text = doc_processor.extract_text(temp_path)
        
        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from document")
        
        # Generate summary
        summary = summarizer.summarize(text)
        
        # Extract insights
        insights = summarizer.extract_insights(text)
        
        # Check spelling in the summary
        spell_check_results = spell_checker.check_spelling(summary)
        
        # Clean up temporary file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        
        return SummaryResponse(
            filename=file.filename,
            original_text_length=len(text),
            summary=summary,
            insights=insights,
            spell_check=spell_check_results,
            processed_at=datetime.now().isoformat()
        ).dict()
    
    except Exception as e:
        # Clean up on error
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/spell-check")
async def spell_check(text: str):
    """
    Check spelling in provided text
    
    Args:
        text: Text to check spelling
    """
    try:
        if not text:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        results = spell_checker.check_spelling(text)
        return results
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/correct-text")
async def correct_text(text: str):
    """
    Auto-correct text
    
    Args:
        text: Text to correct
    """
    try:
        if not text:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        corrected = spell_checker.correct_text(text)
        return {
            "original": text,
            "corrected": corrected,
            "changed": text != corrected
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/supported-formats")
async def get_supported_formats():
    """Get list of supported document formats"""
    return {
        "formats": ["pdf", "docx"],
        "descriptions": {
            "pdf": "PDF documents",
            "docx": "Microsoft Word documents"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
