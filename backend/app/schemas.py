from pydantic import BaseModel, Field
from typing import Dict, Any

class PredictionInput(BaseModel):
    sexo: str = Field(..., description="Sexo del paciente (ej. 'Hombre', 'Mujer')")
    edad: int = Field(..., ge=18, le=120, description="Edad del paciente en años")
    peso: float = Field(..., ge=30.0, le=250.0, description="Peso del paciente en kg")
    estatura: float = Field(..., ge=100.0, le=250.0, description="Estatura del paciente en cm")
    medida_cintura: float = Field(..., ge=40.0, le=200.0, description="Circunferencia de cintura en cm")
    masa_corporal: float = Field(..., ge=10.0, le=60.0, description="Índice de Masa Corporal (IMC)")
    tension_arterial: float = Field(..., ge=50.0, le=250.0, description="Tensión arterial sistólica (o valor reportado)")
    resultado_glucosa: float = Field(..., ge=30.0, le=500.0, description="Nivel de glucosa en ayunas en mg/dL")
    valor_colesterol_ldl: float = Field(..., ge=30.0, le=300.0, description="Colesterol LDL en mg/dL")
    valor_colesterol_hdl: float = Field(..., ge=10.0, le=150.0, description="Colesterol HDL en mg/dL")
    valor_colesterol_total: float = Field(..., ge=50.0, le=500.0, description="Colesterol Total en mg/dL")
    valor_trigliceridos: float = Field(..., ge=30.0, le=1000.0, description="Nivel de triglicéridos en mg/dL")
    valor_hemoglobina_glucosilada: float = Field(..., ge=3.0, le=20.0, description="Hemoglobina Glucosilada (HbA1c) en %")
    valor_proteinac_reactiva: float = Field(..., ge=0.01, le=50.0, description="Proteína C Reactiva Ultra sensible (PCR-hs) en mg/L")
    valor_insulina: float = Field(..., ge=0.5, le=100.0, description="Nivel de Insulina en uIU/mL")
    valor_acido_urico: float = Field(..., ge=1.0, le=20.0, description="Nivel de ácido úrico en mg/dL")
    sueno_horas: float = Field(..., ge=2.0, le=24.0, description="Horas promedio de sueño diarias")
    actividad_total: float = Field(..., ge=0.0, le=1000.0, description="Minutos semanales o índice de actividad física")

    class Config:
        json_schema_extra = {
            "example": {
                "sexo": "Mujer",
                "edad": 45,
                "peso": 78.5,
                "estatura": 160.0,
                "medida_cintura": 95.0,
                "masa_corporal": 29.8,
                "tension_arterial": 135.0,
                "resultado_glucosa": 105.0,
                "valor_colesterol_ldl": 125.0,
                "valor_colesterol_hdl": 45.0,
                "valor_colesterol_total": 210.0,
                "valor_trigliceridos": 160.0,
                "valor_hemoglobina_glucosilada": 6.1,
                "valor_proteinac_reactiva": 2.8,
                "valor_insulina": 15.2,
                "valor_acido_urico": 5.4,
                "sueno_horas": 6.5,
                "actividad_total": 90.0
            }
        }

class PredictionOutput(BaseModel):
    nivel_riesgo: str = Field(..., description="Nivel de riesgo predicho ('Bajo', 'Medio', 'Alto')")
    probabilidad_porcentual: float = Field(..., description="Probabilidad de pertenencia a la clase predicha o distribución completa de probabilidades")
    distribucion_probabilidades: Dict[str, float] = Field(..., description="Distribución de probabilidad para cada uno de los 3 niveles")
    explicacion_clinica: str = Field(..., description="Explicación narrativa basada en valores SHAP de las variables predictoras clave")
    valores_shap: Dict[str, float] = Field(..., description="Contribuciones relativas de SHAP para cada variable en la decisión del modelo")
