# ─────────────────────────────────────────────────────────────────────────────
# GlucoCheck — Dockerfile (backend)
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.10-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
      gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python (capa separada para cache de Docker)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar código fuente
COPY src/       ./src/
COPY data/      ./data/

EXPOSE 8000

CMD ["python", "src/api/main.py"]
