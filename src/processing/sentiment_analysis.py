# src/processing/sentiment_analysis.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType
from textblob import TextBlob

# Crear sesión de Spark
spark = SparkSession.builder \
    .appName("SentimentAnalysis") \
    .getOrCreate()

# Esquema para los datos de Kafka
schema = StructType([
    StructField("body", StringType(), True),
    StructField("author", StringType(), True),
    StructField("created_utc", StringType(), True)
])

# Leer datos de Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "reddit_comments") \
    .load()

# Parsear JSON
df = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Analizar sentimientos
def analyze_sentiment(text):
    analysis = TextBlob(text)
    return "positive" if analysis.sentiment.polarity > 0 else "negative" if analysis.sentiment.polarity < 0 else "neutral"

sentiment_udf = spark.udf.register("analyze_sentiment", analyze_sentiment)

df_with_sentiment = df.withColumn("sentiment", sentiment_udf(col("body")))

# Mostrar resultados en consola
query = df_with_sentiment.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()