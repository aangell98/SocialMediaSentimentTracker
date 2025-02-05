# src/processing/sentiment_analysis.py
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

# Inicializar el analizador de VADER
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(comment_text):
    """
    Analiza el sentimiento de un texto usando VADER.
    :param comment_text: Texto del comentario.
    :return: Diccionario con el análisis de sentimientos.
    """
    sentiment = analyzer.polarity_scores(comment_text)
    return sentiment


def process_comments_from_file(filename="data/reddit_comments.json"):
    """
    Procesa los comentarios de un archivo JSON y realiza análisis de sentimientos.
    :param filename: Nombre del archivo JSON con los comentarios.
    :return: Lista de comentarios con análisis de sentimientos.
    """
    try:
        with open(filename, "r") as f:
            comments = json.load(f)
    except FileNotFoundError:
        print(f"El archivo {filename} no existe.")
        return []

    analyzed_comments = []

    for comment in comments:
        # Obtener el texto del comentario
        comment_text = comment.get("comment_text", "")

        if not comment_text.strip():
            continue  # Saltar comentarios vacíos

        # Analizar el sentimiento del comentario
        sentiment = analyze_sentiment(comment_text)

        # Agregar el análisis al diccionario del comentario
        comment["sentiment"] = {
            "positive": sentiment["pos"],
            "negative": sentiment["neg"],
            "neutral": sentiment["neu"],
            "compound": sentiment["compound"],
            "overall_sentiment": classify_sentiment(sentiment["compound"])
        }

        analyzed_comments.append(comment)

    return analyzed_comments


def classify_sentiment(compound_score):
    """
    Clasifica el sentimiento general basado en el puntaje compound de VADER.
    :param compound_score: Puntaje compound de VADER.
    :return: Etiqueta de sentimiento ("positive", "negative", "neutral").
    """
    if compound_score >= 0.05:
        return "positive"
    elif compound_score <= -0.05:
        return "negative"
    else:
        return "neutral"


def save_analyzed_data(data, output_filename="data/analyzed_reddit_comments.json"):
    """
    Guarda los datos analizados en un archivo JSON.
    :param data: Datos analizados.
    :param output_filename: Nombre del archivo de salida.
    """
    with open(output_filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Datos analizados guardados en {output_filename}. Total de comentarios analizados: {len(data)}")


def main():
    # Procesar los comentarios y realizar análisis de sentimientos
    analyzed_comments = process_comments_from_file()

    if analyzed_comments:
        # Guardar los resultados en un archivo JSON
        save_analyzed_data(analyzed_comments)


if __name__ == "__main__":
    main()