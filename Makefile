# Makefile

# Variables
PROJECT_DIR := $(shell pwd)
VENV := venv

#Instalar dependencias
install:
    pip install -r requirements.txt

#Crear entorno virtual
setup: install
    python -m venv $(VENV)
    @echo "Entorno virtual creado. Actívalo con 'source venv/bin/activate'."

# Activar entorno virtual (solo funciona en sistemas UNIX)
activate:
    test -d $(VENV) || (echo "El entorno virtual no existe. Ejecuta 'make setup' primero." && exit 1)
    @source $(VENV)/bin/activate

# Analizar sentimientos
analyze:
    python src/processing/sentiment_analysis.py

# Recolectar comentarios de Reddit
scrape:
    python -m src.data_collection.reddit_scraper

# Iniciar el dashboard
visualize:
    streamlit run src/visualization/dashboard.py

# Limpiar archivos generados
clean:
    rm -rf data/analyzed_reddit_comments.json
    rm -rf data/reddit_comments.json

# Ayuda
help:
    @echo "Comandos disponibles:"
    @echo "  make install       - Instalar dependencias del proyecto."
    @echo "  make setup         - Configurar el entorno virtual y las dependencias."
    @echo "  make activate      - Activar el entorno virtual (solo UNIX)."
    @echo "  make analyze       - Analizar los sentimientos de los comentarios recolectados."
    @echo "  make scrape        - Recolectar comentarios de Reddit."
    @echo "  make visualize     - Iniciar el dashboard de visualización."
    @echo "  make clean         - Eliminar archivos generados por el proyecto."