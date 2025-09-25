# Mock analysis module for testing when transformers is not available
import logging

logger = logging.getLogger(__name__)

def get_sentiment_pipeline():
    """Mock pipeline that simulates the real transformers pipeline"""
    logger.info("Using mock sentiment pipeline for testing")
    return MockSentimentPipeline()

class MockSentimentPipeline:
    """Mock sentiment analysis pipeline for testing purposes"""
    
    def __call__(self, text: str):
        # Simple rule-based mock analysis
        text_lower = text.lower()
        
        positive_words = ['love', 'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome', 'happy', 'excited']
        negative_words = ['hate', 'bad', 'terrible', 'awful', 'horrible', 'disappointing', 'sad', 'angry', 'frustrated', 'worst']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return [{"label": "5 stars", "score": 0.85 + (positive_count * 0.05)}]
        elif negative_count > positive_count:
            return [{"label": "1 star", "score": 0.80 + (negative_count * 0.05)}]
        else:
            return [{"label": "3 stars", "score": 0.60}]

def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of a text using mock analysis.
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Truncate text if too long
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
        if '5' in label or '4' in label or 'positive' in label:
            label = 'positive'
        elif '1' in label or '2' in label or 'negative' in label:
            label = 'negative'
        else:
            label = 'neutral'
            
        return {
            "label": label,
            "score": min(score, 1.0)  # Ensure score doesn't exceed 1.0
        }
        
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {e}")
        # Return neutral sentiment as fallback
        return {
            "label": "neutral",
            "score": 0.5
        }