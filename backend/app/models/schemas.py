from pydantic import BaseModel
from typing import List, Dict, Optional


class SummaryResponse(BaseModel):
    """Response model for document summary"""
    filename: str
    original_text_length: int
    summary: str
    insights: Dict
    spell_check: Optional[Dict] = None
    processed_at: str


class SpellCheckResponse(BaseModel):
    """Response model for spell check"""
    misspelled_count: int
    misspelled_words: List[str]
    corrections: Dict
    accuracy_percentage: float


class InsightModel(BaseModel):
    """Model for document insights"""
    key_topics: List[str]
    entities: List[str]
    sentiment: str
    word_count: int
    reading_time_minutes: int


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
    status_code: int
