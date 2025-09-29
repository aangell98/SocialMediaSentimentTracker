from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from contextlib import asynccontextmanager

# Configure logging FIRST, before imports
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- MODIFICACIÓN: Importar los nuevos modelos y el analizador de Reddit ---
from .models import SentimentRequest, SentimentResponse, HealthResponse, RedditPostRequest, RedditPostResponse

# Try to import real analysis, fall back to mock if not available
try:
    from .analysis import analyze_sentiment, get_sentiment_pipeline
    from . import reddit_analyzer # Importar el módulo de reddit
    USING_MOCK = False
    logger.info("Successfully imported real analysis modules")
except ImportError as e:
    # --- MODIFICACIÓN AQUÍ: Usar logging en lugar de print ---
    logger.critical(f"!!! IMPORT ERROR: Falling back to mock mode. Reason: {e}")
    from .analysis_mock import analyze_sentiment, get_sentiment_pipeline
    # Mock para reddit_analyzer si es necesario
    class MockRedditAnalyzer:
        def analyze_reddit_post(self, post_url: str):
            raise NotImplementedError("Reddit analysis is not available in mock mode")
    reddit_analyzer = MockRedditAnalyzer()
    USING_MOCK = True

# Version
__version__ = "2.0.0"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the ML model on startup and clean up on shutdown."""
    try:
        # Preload the model during startup
        logger.info("Preloading sentiment analysis model...")
        get_sentiment_pipeline()
        logger.info("Model preloaded successfully")
    except Exception as e:
        logger.error(f"Failed to preload model: {e}")
    
    yield
    
    # Cleanup can be added here if needed
    logger.info("Application shutting down")


# Initialize FastAPI app with lifespan management
app = FastAPI(
    title="Sentiment Analysis API",
    description="A modern microservice for analyzing text sentiment using state-of-the-art transformers models.",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint providing API information."""
    mode = "mock mode (for testing)" if USING_MOCK else "production mode"
    return HealthResponse(
        status="healthy",
        message=f"Sentiment Analysis API is running in {mode}. Visit /docs for API documentation.",
        version=__version__
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring."""
    try:
        # Quick test of the model
        get_sentiment_pipeline()
        return HealthResponse(
            status="healthy",
            message="All systems operational",
            version=__version__
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "message": f"Service unavailable: {str(e)}",
                "version": __version__
            }
        )


@app.post("/analyze", response_model=SentimentResponse)
async def analyze_text_sentiment(request: SentimentRequest):
    """
    Analyze the sentiment of provided text.
    
    Returns sentiment label (positive/negative/neutral) and confidence score.
    """
    try:
        # Validate input
        if not request.text or not request.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text field cannot be empty"
            )
        
        # Perform sentiment analysis
        logger.info(f"Analyzing sentiment for text of length {len(request.text)}")
        result = analyze_sentiment(request.text.strip())
        
        response = SentimentResponse(
            label=result["label"],
            score=result["score"]
        )
        
        logger.info(f"Analysis complete: {result['label']} (score: {result['score']:.4f})")
        return response
        
    except ValueError as ve:
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Unexpected error during sentiment analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred during sentiment analysis"
        )


@app.post("/batch-analyze")
async def batch_analyze_sentiment(texts: list[str]):
    """
    Analyze sentiment for multiple texts at once.
    Limited to 10 texts per request to prevent overload.
    """
    if len(texts) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 10 texts allowed per batch request"
        )
    
    if not texts or any(not text.strip() for text in texts):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All texts must be non-empty"
        )
    
    try:
        results = []
        for i, text in enumerate(texts):
            logger.info(f"Analyzing batch item {i+1}/{len(texts)}")
            result = analyze_sentiment(text.strip())
            results.append({
                "text": text[:50] + "..." if len(text) > 50 else text,
                "sentiment": result
            })
        
        return {"results": results, "count": len(results)}
        
    except Exception as e:
        logger.error(f"Error in batch analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error occurred during batch analysis"
        )

@app.post("/api/v1/reddit/analyze", response_model=RedditPostResponse)
async def analyze_reddit_post_endpoint(request: RedditPostRequest):
    """
    Fetches comments from a Reddit post URL, analyzes their sentiment,
    and returns a summary and a list of analyzed comments.
    """
    logger.info(f"Received request to analyze Reddit post: {request.post_url}")
    try:
        result = reddit_analyzer.analyze_reddit_post(request.post_url)
        logger.info(f"Successfully analyzed {result['summary']['total_comments_analyzed']} comments from post.")
        return result
    except NotImplementedError:
        logger.error("Reddit analysis called in mock mode.")
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Reddit analysis is not available in mock mode."
        )
    except Exception as e:
        logger.error(f"Error analyzing Reddit post '{request.post_url}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while analyzing the Reddit post: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )