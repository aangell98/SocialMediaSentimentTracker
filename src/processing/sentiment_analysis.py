# src/processing/sentiment_analysis.py
from transformers import pipeline
import json

# Cargar el modelo preentrenado para análisis de sentimientos
sentiment_analyzer = pipeline("sentiment-analysis", model="tabularisai/multilingual-sentiment-analysis")

def analyze_sentiment(comment_text):
    """
    Analiza el sentimiento de un texto, truncando si es demasiado largo.
    """
    max_length = 512  # Límite de tokens para RoBERTa

    # Si el texto es demasiado largo, lo corta
    truncated_text = comment_text[:max_length]

    try:
        result = sentiment_analyzer(truncated_text)[0]
        return {
            "label": result["label"],  # Puede ser "positive", "neutral" o "negative"
            "score": result["score"]
        }
    except Exception as e:
        print(f"Error al analizar el sentimiento: {e}")
        return {"label": "neutral", "score": 0.0}



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
            "label": sentiment["label"],
            "score": sentiment["score"],
            "overall_sentiment": classify_sentiment(sentiment["label"])
        }

        analyzed_comments.append(comment)

    return analyzed_comments

def classify_sentiment(label):
    """
    Clasifica el sentimiento general basado en la etiqueta del modelo.
    :param label: Etiqueta del modelo ("POSITIVE", "NEGATIVE").
    :return: Etiqueta de sentimiento ("positive", "negative", "neutral").
    """
    if label == "Positive":
        return "positive"
    elif label == "Negative":
        return "negative"
    elif label == "Very Negative":
        return " very negative"
    elif label == "Very Positive":
        return " very positive"
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