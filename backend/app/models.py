from pydantic import BaseModel, Field
from typing import Optional


class SentimentRequest(BaseModel):
    """Request model for sentiment analysis"""
    text: str = Field(..., min_length=1, max_length=2000, description="Text to analyze")
    
    class Config:
        json_schema_extra = {
            "example": {
                "text": "I love this new approach to the project!"
            }
        }


class SentimentResponse(BaseModel):
    """Response model for sentiment analysis"""
    label: str = Field(..., description="Sentiment label (positive/negative/neutral)")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    
    class Config:
        json_schema_extra = {
            "example": {
                "label": "positive",
                "score": 0.9845
            }
        }


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    message: str
    version: Optional[str] = None