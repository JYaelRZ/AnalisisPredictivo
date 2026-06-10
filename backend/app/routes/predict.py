from fastapi import APIRouter, HTTPException
from app.schemas import PredictionInput, PredictionOutput
from app.services.ml_service import ml_service
from app.services.shap_service import shap_service

router = APIRouter()

@router.post("/predict", response_model=PredictionOutput, summary="Predecir riesgo cardiovascular")
async def predict(payload: PredictionInput):
    """
    Predice el nivel de riesgo cardiovascular (Bajo, Medio, Alto) de un paciente
    basado en sus biomarcadores y variables clínicas, y genera explicabilidad clínica con valores SHAP.
    """
    try:
        # Convertir payload de Pydantic a diccionario de Python
        input_data = payload.model_dump()
        
        # 1. Ejecutar inferencia de Machine Learning con XGBoost
        prediction_result = ml_service.predict_risk(input_data)
        
        nivel_riesgo = prediction_result["nivel_riesgo"]
        probabilidad = prediction_result["probabilidad_porcentual"]
        distribucion = prediction_result["distribucion_probabilidades"]
        features_processed = prediction_result["features_processed"]
        
        # 2. Generar explicabilidad clínica interactiva con SHAP
        explicacion, valores_shap = shap_service.explain_prediction(
            features_processed, nivel_riesgo
        )
        
        return PredictionOutput(
            nivel_riesgo=nivel_riesgo,
            probabilidad_porcentual=probabilidad,
            distribucion_probabilidades=distribucion,
            explicacion_clinica=explicacion,
            valores_shap=valores_shap
        )
        
    except RuntimeError as re:
        raise HTTPException(status_code=400, detail=f"Modelo no inicializado: {str(re)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor de inferencia: {str(e)}")
