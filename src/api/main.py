import sys
import joblib
import numpy as np
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Permite ejecutar tanto como módulo (uvicorn src.api.main) como script directo
try:
    from src.api.schemas import PredictionInput, PredictionOutput, HealthResponse
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from schemas import PredictionInput, PredictionOutput, HealthResponse

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"

FEATURE_ORDER = [
    "pregnancies", "glucose", "blood_pressure", "skin_thickness",
    "insulin", "bmi", "diabetes_pedigree", "age"
]

MESSAGES = {
    "riesgo_bajo": "Las variables introducidas no muestran combinaciones asociadas a un perfil de riesgo significativo.",
    "riesgo_moderado": "Las variables introducidas presentan algunos factores que podrían estar asociados a un riesgo moderado.",
    "riesgo_alto": "Las variables introducidas presentan una combinación asociada a un perfil de riesgo elevado.",
}

ADVERTENCIA = "Este resultado no constituye un diagnóstico médico."


def load_artifacts():
    model_path = PROCESSED_DIR / "model.pkl"
    scaler_path = PROCESSED_DIR / "scaler.pkl"
    threshold_path = PROCESSED_DIR / "threshold.txt"

    missing = [p for p in [model_path, scaler_path, threshold_path] if not p.exists()]
    if missing:
        raise RuntimeError(
            f"Artefactos no encontrados: {[str(p) for p in missing]}. "
            "Ejecuta primero los scripts de preprocesamiento y entrenamiento."
        )

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    threshold = float(threshold_path.read_text().strip())
    return model, scaler, threshold


try:
    model, scaler, threshold = load_artifacts()
except RuntimeError as e:
    print(f"ERROR al cargar artefactos: {e}")
    raise

app = FastAPI(
    title="GlucoCheck API",
    description="API de inferencia para clasificación del riesgo de Diabetes Tipo 2",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", model="Random Forest", threshold=threshold)


@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    try:
        features = np.array([[getattr(data, col) for col in FEATURE_ORDER]])
        features_scaled = scaler.transform(features)
        proba = float(model.predict_proba(features_scaled)[0][1])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error durante la predicción: {e}")

    if proba < 0.3:
        nivel, color = "riesgo_bajo", "verde"
    elif proba <= threshold:
        nivel, color = "riesgo_moderado", "amarillo"
    else:
        nivel, color = "riesgo_alto", "rojo"

    return PredictionOutput(
        probabilidad=round(proba, 4),
        nivel_riesgo=nivel,
        color=color,
        mensaje=MESSAGES[nivel],
        advertencia=ADVERTENCIA,
    )


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
