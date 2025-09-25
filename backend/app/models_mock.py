"""
Minimal implementation of required models for testing when pydantic is not available
"""

class BaseModel:
    def __init__(self, **data):
        for key, value in data.items():
            setattr(self, key, value)

class Field:
    def __init__(self, default=None, **kwargs):
        self.default = default
        self.kwargs = kwargs

class SentimentRequest(BaseModel):
    """Request model for sentiment analysis"""
    def __init__(self, text: str, **kwargs):
        super().__init__(text=text, **kwargs)

class SentimentResponse(BaseModel):
    """Response model for sentiment analysis"""
    def __init__(self, label: str, score: float, **kwargs):
        super().__init__(label=label, score=score, **kwargs)

class HealthResponse(BaseModel):
    """Health check response model"""
    def __init__(self, status: str, message: str, version: str = None, **kwargs):
        super().__init__(status=status, message=message, version=version, **kwargs)