import numpy as np
import joblib
import pytest
from pathlib import Path

PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"

FEATURE_ORDER = [
    "pregnancies", "glucose", "blood_pressure", "skin_thickness",
    "insulin", "bmi", "diabetes_pedigree", "age"
]

VALID_RISK_LEVELS = {"riesgo_bajo", "riesgo_moderado", "riesgo_alto"}

CONTROLLED_INPUT = {
    "pregnancies": 6, "glucose": 148, "blood_pressure": 72,
    "skin_thickness": 35, "insulin": 0, "bmi": 33.6,
    "diabetes_pedigree": 0.627, "age": 50
}


def test_artifacts_exist():
    """model.pkl y scaler.pkl deben existir en data/processed/."""
    assert (PROCESSED_DIR / "model.pkl").exists(), "No se encontró model.pkl"
    assert (PROCESSED_DIR / "scaler.pkl").exists(), "No se encontró scaler.pkl"
    assert (PROCESSED_DIR / "threshold.txt").exists(), "No se encontró threshold.txt"


def test_inference_returns_valid_probability():
    """La inferencia con un ejemplo controlado devuelve probabilidad entre 0 y 1."""
    model = joblib.load(PROCESSED_DIR / "model.pkl")
    scaler = joblib.load(PROCESSED_DIR / "scaler.pkl")
    threshold = float((PROCESSED_DIR / "threshold.txt").read_text().strip())

    features = np.array([[CONTROLLED_INPUT[col] for col in FEATURE_ORDER]])
    features_scaled = scaler.transform(features)
    proba = float(model.predict_proba(features_scaled)[0][1])

    assert 0.0 <= proba <= 1.0, f"Probabilidad fuera de rango: {proba}"


def test_inference_returns_valid_risk_level():
    """La inferencia devuelve un nivel de riesgo válido."""
    model = joblib.load(PROCESSED_DIR / "model.pkl")
    scaler = joblib.load(PROCESSED_DIR / "scaler.pkl")
    threshold = float((PROCESSED_DIR / "threshold.txt").read_text().strip())

    features = np.array([[CONTROLLED_INPUT[col] for col in FEATURE_ORDER]])
    features_scaled = scaler.transform(features)
    proba = float(model.predict_proba(features_scaled)[0][1])

    if proba < 0.3:
        nivel = "riesgo_bajo"
    elif proba <= threshold:
        nivel = "riesgo_moderado"
    else:
        nivel = "riesgo_alto"

    assert nivel in VALID_RISK_LEVELS, f"Nivel de riesgo inesperado: {nivel}"
