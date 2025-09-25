# src/visualization/dashboard.py
import json
import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def load_data(filename="data/analyzed_reddit_comments.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        print(f"Cantidad de comentarios originales: {len(data)}")

        # Aplanar la estructura del JSON
        flattened_data = []
        for item in data:
            sentiment = item.get("sentiment", {})
            flattened_item = {
                "post_title": item.get("post_title", ""),
                "post_text": item.get("post_text", ""),
                "post_url": item.get("post_url", ""),
                "comment_text": item.get("comment_text", ""),
                "upvotes": item.get("upvotes", 0),
                "created_utc": item.get("created_utc", None),
                "author": item.get("author", ""),
                "comment_url": item.get("comment_url", ""),
                "label": sentiment.get("label", "neutral"),  # Etiqueta de sentimiento
                "score": sentiment.get("score", 0),         # Puntuación del modelo
                "overall_sentiment": sentiment.get("overall_sentiment", "neutral")
            }
            flattened_data.append(flattened_item)

        df = pd.DataFrame(flattened_data)

        # Mapear etiquetas a valores numéricos
        sentiment_mapping = {
            "Very Positive": 1.0,
            "Positive": 0.5,
            "Neutral": 0.0,
            "Negative": -0.5,
            "Very Negative": -1.0
        }
        df["sentiment_value"] = df["label"].map(sentiment_mapping).fillna(0)

        print(f"Cantidad de comentarios procesados: {len(df)}")

        return df

    except FileNotFoundError:
        print(f"El archivo {filename} no existe.")
        return None

# Mostrar distribución de sentimientos
def show_sentiment_distribution(df):
    if "overall_sentiment" not in df.columns:
        st.error("La columna 'overall_sentiment' no está presente en los datos.")
        return

    sentiment_counts = df["overall_sentiment"].value_counts()
    fig = px.pie(
        sentiment_counts,
        names=sentiment_counts.index,
        values=sentiment_counts.values,
        title="Distribución de Sentimientos"
    )
    st.plotly_chart(fig)

# Mostrar tendencias temporales
def show_sentiment_trends(df):
    if "created_utc" not in df.columns or "sentiment_value" not in df.columns:
        st.error("Faltan columnas necesarias ('created_utc' o 'sentiment_value') en los datos.")
        return

    # Convertir 'created_utc' a datetime y eliminar filas con valores inválidos
    df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s", errors="coerce")
    df = df.dropna(subset=["created_utc"])  # Eliminar filas con fechas inválidas

    if df.empty:
        st.warning("No hay suficientes datos con fechas válidas para mostrar tendencias temporales.")
        return

    # Establecer 'created_utc' como índice (asegurando que sea un DatetimeIndex)
    df = df.set_index("created_utc")

    if not isinstance(df.index, pd.DatetimeIndex):
        st.error("El índice del DataFrame no es un DatetimeIndex. Verifica los datos cargados.")
        return

    # Resamplear los datos por hora y calcular el promedio del valor de sentimiento
    df_resampled = df["sentiment_value"].resample("1h").mean().reset_index()

    fig = px.line(
        df_resampled,
        x="created_utc",
        y="sentiment_value",
        title="Tendencias Temporales del Sentimiento"
    )
    st.plotly_chart(fig)

# Mostrar comentarios destacados
def show_top_comments(df):
    if "sentiment_value" not in df.columns:
        st.error("La columna 'sentiment_value' no está presente en los datos.")
        return

    st.subheader("Comentarios Más Positivos")
    top_positive = df[df["sentiment_value"] > 0].nlargest(5, "sentiment_value")[["comment_text", "sentiment_value"]]
    st.table(top_positive)

    st.subheader("Comentarios Más Negativos")
    top_negative = df[df["sentiment_value"] < 0].nsmallest(5, "sentiment_value")[["comment_text", "sentiment_value"]]
    st.table(top_negative)

# Main app
def main():
    st.title("Análisis de Sentimientos en Reddit")

    # Cargar datos
    df = load_data()
    if df is None or df.empty:
        st.error("No se pudieron cargar los datos.")
        return

    # Mostrar todos los datos cargados
    st.write("Datos cargados:")
    st.dataframe(df)

    # Verificar columnas necesarias
    required_columns = {"overall_sentiment", "sentiment_value", "created_utc"}
    if not required_columns.issubset(df.columns):
        st.error(f"Faltan columnas necesarias: {required_columns - set(df.columns)}")
        return

    # Mostrar distribución de sentimientos
    show_sentiment_distribution(df)

    # Mostrar tendencias temporales
    show_sentiment_trends(df)

    # Mostrar comentarios destacados
    show_top_comments(df)

if __name__ == "__main__":
    main()