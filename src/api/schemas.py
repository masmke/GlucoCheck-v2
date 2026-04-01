from pydantic import BaseModel, field_validator
from typing import Literal


class PredictionInput(BaseModel):
    pregnancies: float
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    diabetes_pedigree: float
    age: float

    @field_validator("*", mode="before")
    @classmethod
    def must_be_numeric(cls, v):
        try:
            return float(v)
        except (TypeError, ValueError):
            raise ValueError("Todos los campos deben ser numéricos")


class PredictionOutput(BaseModel):
    probabilidad: float
    nivel_riesgo: Literal["riesgo_bajo", "riesgo_moderado", "riesgo_alto"]
    color: Literal["verde", "amarillo", "rojo"]
    mensaje: str
    advertencia: str


class HealthResponse(BaseModel):
    status: str
    model: str
    threshold: float
