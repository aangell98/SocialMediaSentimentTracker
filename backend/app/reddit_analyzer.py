import praw
import os
from dotenv import load_dotenv
from .analysis import analyze_sentiment
from collections import Counter
import logging

load_dotenv()

# Configurar logging para este módulo
logger = logging.getLogger(__name__)

def get_reddit_instance():
    return praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
        check_for_async=False
    )

def analyze_reddit_post(post_url: str):
    reddit = get_reddit_instance()
    submission = reddit.submission(url=post_url)
    
    logger.info(f"Analyzing post: '{submission.title}' with {submission.num_comments} total comments")
    
    # Reemplaza "MoreComments" para obtener todos los comentarios
    submission.comments.replace_more(limit=None)
    
    analyzed_comments = []
    sentiment_counts = Counter()
    raw_results_sample = []  # Para depuración
    
    for i, comment in enumerate(submission.comments.list()):
        if not comment.body or comment.body in ['[deleted]', '[removed]']:
            continue
            
        # Analizar el comentario
        sentiment_result = analyze_sentiment(comment.body)
        
        # LOGGING DETALLADO para los primeros 5 comentarios
        if i < 5:
            logger.info(f"Comment {i+1}: '{comment.body[:100]}...'")
            logger.info(f"Raw sentiment result: {sentiment_result}")
            raw_results_sample.append({
                "text": comment.body[:100],
                "raw_result": sentiment_result
            })
        
        # El modelo nlptown da estrellas, vamos a mapearlas a etiquetas simples
        label_map = {
            "1 star": "negative", "2 stars": "negative",
            "3 stars": "neutral",
            "4 stars": "positive", "5 stars": "positive"
        }
        
        # MEJORA: Manejo más robusto del mapeo
        raw_label = sentiment_result.get('label', 'unknown')
        simple_label = label_map.get(raw_label, 'neutral')  # Por defecto neutral si no encuentra
        
        # LOGGING: Si el mapeo falla
        if raw_label not in label_map:
            logger.warning(f"Unknown sentiment label received: '{raw_label}'. Defaulting to neutral.")
        
        analyzed_comments.append({
            "text": comment.body,
            "author": str(comment.author),
            "sentiment": simple_label,
            "score": sentiment_result.get('score', 0.0),
            "raw_label": raw_label  # Para depuración
        })
        sentiment_counts[simple_label] += 1
        
    total_comments = len(analyzed_comments)
    
    # LOGGING DE RESUMEN
    logger.info(f"Analysis complete: {total_comments} comments processed")
    logger.info(f"Sentiment distribution: {dict(sentiment_counts)}")
    logger.info(f"Sample of raw results: {raw_results_sample}")
    
    summary = {
        "post_title": submission.title,
        "total_comments_analyzed": total_comments,
        "positive_count": sentiment_counts['positive'],
        "negative_count": sentiment_counts['negative'],
        "neutral_count": sentiment_counts['neutral'],
    }
    
    return {"summary": summary, "comments": analyzed_comments}