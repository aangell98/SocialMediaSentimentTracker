# src/data_collection/reddit_scraper.py
import json
import praw
from .config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

# Configuración de PRAW
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# Recolectar posts de un subreddit
subreddit = reddit.subreddit("python")  # Cambia "python" por el subreddit que quieras analizar
posts = []

for post in subreddit.new(limit=10):  # Recolecta los 10 posts más recientes
    post_data = {
        "title": post.title,
        "text": post.selftext,
        "upvotes": post.score,
        "created_utc": post.created_utc,
        "author": str(post.author),
        "url": post.url
    }
    posts.append(post_data)

# Guardar los datos en un archivo JSON
with open("data/reddit_posts.json", "w") as f:
    json.dump(posts, f, indent=4)

print("Datos guardados en data/reddit_posts.json")