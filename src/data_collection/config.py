# src/data_collection/config.py
from dotenv import load_dotenv
import os

load_dotenv()

# Credenciales de la API de Reddit
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Validación de credenciales
if not all([REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT]):
    missing = [
        key for key, value in {
            "REDDIT_CLIENT_ID": REDDIT_CLIENT_ID,
            "REDDIT_CLIENT_SECRET": REDDIT_CLIENT_SECRET,
            "REDDIT_USER_AGENT": REDDIT_USER_AGENT
        }.items() if not value
    ]
    raise ValueError(f"Faltan las siguientes credenciales en el archivo .env: {', '.join(missing)}")