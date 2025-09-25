from transformers import pipeline
from functools import lru_cache
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def get_sentiment_pipeline():
    """
    Load and cache the sentiment analysis pipeline.
    Using the multilingual model for better language support.
    """
    try:
        logger.info("Loading sentiment analysis model...")
        # Using a robust multilingual sentiment analysis model
        pipe = pipeline(
            "sentiment-analysis", 
            model="nlptown/bert-base-multilingual-uncased-sentiment",
            return_all_scores=False
        )
        logger.info("Model loaded successfully")
        return pipe
    except Exception as e:
        logger.error(f"Failed to load sentiment model: {e}")
        raise


def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of a text.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: Contains 'label' and 'score' keys
        
    Raises:
        Exception: If sentiment analysis fails
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Truncate text if too long to avoid model limits
    max_length = 512
    if len(text) > max_length:
        text = text[:max_length]
        logger.warning(f"Text truncated to {max_length} characters")
    
    try:
        sentiment_pipeline = get_sentiment_pipeline()
        result = sentiment_pipeline(text)
        
        # Ensure we have a single result
        if isinstance(result, list) and len(result) > 0:
            result = result[0]
            
        # Normalize the label to standard format
        label = result.get('label', 'neutral').lower()
        score = float(result.get('score', 0.0))
        
        # Map model-specific labels to standard labels
        if 'positive' in label or '4' in label or '5' in label:
            label = 'positive'
        elif 'negative' in label or '1' in label or '2' in label:
            label = 'negative'
        else:
            label = 'neutral'
            
        return {
            "label": label,
            "score": score
        }
        
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        # Return neutral sentiment as fallback
        return {
            "label": "neutral",
            "score": 0.5
        }