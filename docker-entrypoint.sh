#!/bin/sh
# ─────────────────────────────────────────────────────────────────────────────
# GlucoCheck — Docker entrypoint
# Ejecuta el pipeline de datos si faltan artefactos, luego arranca la API
# ─────────────────────────────────────────────────────────────────────────────
set -e

ARTIFACTS_DIR="/app/data/processed"
MISSING=0

for f in model.pkl scaler.pkl threshold.txt; do
  if [ ! -f "$ARTIFACTS_DIR/$f" ]; then
    MISSING=1
    break
  fi
done

if [ "$MISSING" -eq 1 ]; then
  echo "[GlucoCheck] Artefactos no encontrados — ejecutando pipeline de datos..."
  mkdir -p "$ARTIFACTS_DIR"

  python -m src.data.download_data
  echo "[GlucoCheck] ✔ Datos descargados"

  python -m src.data.preprocess
  echo "[GlucoCheck] ✔ Preprocesamiento completado"

  python -m src.models.train_model
  echo "[GlucoCheck] ✔ Modelo entrenado"
else
  echo "[GlucoCheck] Artefactos ya existen — omitiendo pipeline"
fi

echo "[GlucoCheck] Iniciando API en http://0.0.0.0:8000 ..."
exec "$@"
