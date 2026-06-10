from pydantic import BaseModel
from typing import List, Dict, Optional


class SummaryResponse(BaseModel):
    """Response model for document summary"""
    filename: str
    original_text_length: int
    summary: str
    insights: Dict
    processed_at: str


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
