import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

CONTROLLED_INPUT = {
    "pregnancies": 6,
    "glucose": 148,
    "blood_pressure": 72,
    "skin_thickness": 35,
    "insulin": 0,
    "bmi": 33.6,
    "diabetes_pedigree": 0.627,
    "age": 50
}

PREDICT_REQUIRED_FIELDS = {"probabilidad", "nivel_riesgo", "color", "mensaje", "advertencia"}


def test_health_returns_200():
    """GET /health devuelve status 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_ok_status():
    """GET /health devuelve {"status": "ok"}."""
    response = client.get("/health")
    assert response.json()["status"] == "ok"


def test_predict_returns_200():
    """POST /predict con ejemplo controlado devuelve status 200."""
    response = client.post("/predict", json=CONTROLLED_INPUT)
    assert response.status_code == 200


def test_predict_returns_required_fields():
    """POST /predict devuelve todos los campos requeridos."""
    response = client.post("/predict", json=CONTROLLED_INPUT)
    body = response.json()
    for field in PREDICT_REQUIRED_FIELDS:
        assert field in body, f"Falta el campo '{field}' en la respuesta"
