import json
import praw
from .config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT

# Configuración de PRAW
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def collect_comments_from_subreddit(subreddit_name="python", limit=5):
    """
    Recolecta comentarios de los posts más recientes de un subreddit.
    :param subreddit_name: Nombre del subreddit a analizar.
    :param limit: Número de posts a analizar.
    :return: Lista de datos de comentarios.
    """
    subreddit = reddit.subreddit(subreddit_name)
    comments = []

    for submission in subreddit.new(limit=limit):  # Obtener los 'limit' posts más recientes
        submission.comments.replace_more(limit=0)  # Limitar la profundidad de los comentarios
        for comment in submission.comments.list():  # Recorrer todos los comentarios del post
            comment_data = {
                "post_title": submission.title,  # Título del post
                "post_text": submission.selftext,  # Texto del post
                "post_url": f"https://reddit.com{submission.permalink}",  # URL del post
                "comment_text": comment.body,  # Texto del comentario
                "upvotes": comment.score,  # Upvotes del comentario
                "created_utc": comment.created_utc,  # Fecha de creación del comentario
                "author": str(comment.author),  # Autor del comentario
                "comment_url": f"https://reddit.com{comment.permalink}"  # URL del comentario
            }
            comments.append(comment_data)

    return comments


def collect_comments_from_post(post_url):
    """
    Recolecta comentarios de un post específico dado su enlace.
    :param post_url: Enlace del post a analizar.
    :return: Lista de datos de comentarios.
    """
    submission = reddit.submission(url=post_url)
    submission.comments.replace_more(limit=0)  # Limitar la profundidad de los comentarios
    comments = []

    for comment in submission.comments.list():  # Recorrer todos los comentarios del post
        comment_data = {
            "post_title": submission.title,  # Título del post
            "post_text": submission.selftext,  # Texto del post
            "post_url": f"https://reddit.com{submission.permalink}",  # URL del post
            "comment_text": comment.body,  # Texto del comentario
            "upvotes": comment.score,  # Upvotes del comentario
            "created_utc": comment.created_utc,  # Fecha de creación del comentario
            "author": str(comment.author),  # Autor del comentario
            "comment_url": f"https://reddit.com{comment.permalink}"  # URL del comentario
        }
        comments.append(comment_data)

    return comments


def save_to_json(data, filename="data/reddit_comments.json"):
    """
    Guarda los datos recolectados en un archivo JSON.
    :param data: Datos a guardar.
    :param filename: Nombre del archivo JSON.
    """
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Datos guardados en {filename}. Total de comentarios: {len(data)}")


def main():
    print("¿Qué tipo de análisis deseas realizar?")
    print("1. Analizar comentarios de un subreddit")
    print("2. Analizar comentarios de un post específico")

    choice = input("Selecciona una opción (1/2): ")

    if choice == "1":
        subreddit_name = input("Introduce el nombre del subreddit: ")
        limit = int(input("Introduce el número de posts a analizar (por defecto 5): ") or 5)
        comments = collect_comments_from_subreddit(subreddit_name=subreddit_name, limit=limit)
        save_to_json(comments)

    elif choice == "2":
        post_url = input("Introduce el enlace del post: ")
        comments = collect_comments_from_post(post_url=post_url)
        save_to_json(comments)

    else:
        print("Opción no válida. Saliendo del programa.")


if __name__ == "__main__":
    main()