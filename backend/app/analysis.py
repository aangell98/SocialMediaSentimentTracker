from transformers import pipeline
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

@lru_cache(maxsize=None)
def get_sentiment_pipeline():
    """
    Carga y cachea el modelo de análisis de sentimiento.
    """
    logger.info("Loading sentiment analysis model...")
    model = pipeline("sentiment-analysis", 
                    model="nlptown/bert-base-multilingual-uncased-sentiment")
    logger.info("Model loaded successfully")
    return model

def analyze_sentiment(text: str) -> dict:
    """
    Analiza el sentimiento de un texto dado.
    """
    if not text or not text.strip():
        logger.warning("Empty text provided for sentiment analysis")
        return {"label": "3 stars", "score": 0.5}
    
    try:
        sentiment_pipeline = get_sentiment_pipeline()
        result = sentiment_pipeline(text.strip())
        
        # El modelo devuelve una lista, tomamos el primer resultado
        if isinstance(result, list) and len(result) > 0:
            final_result = result[0]
        else:
            final_result = result
            
        logger.debug(f"Sentiment analysis result for text '{text[:50]}...': {final_result}")
        return final_result
        
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        return {"label": "3 stars", "score": 0.5}  # Fallback neutral