import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.config import settings
from app.services.ml_service import ml_service
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class TrainRequest(BaseModel):
    evaluations: Optional[List[Dict[str, Any]]] = None

router = APIRouter()

@router.post("/train", summary="Reentrenar modelo XGBoost")
async def train_model(payload: Optional[TrainRequest] = None):
    """
    Endpoint interno para reentrenar el modelo de Machine Learning.
    Lee el archivo CSV de datos clínicos históricos (ENSANUT) y opcionalmente nuevas evaluaciones consolidadas,
    aplica la estratificación clínica (Label Engineering), sobremuestreo (SMOTE),
    entrena el XGBClassifier y actualiza el modelo activo en disco.
    """
    try:
        if not os.path.exists(settings.DATASET_PATH):
            raise HTTPException(
                status_code=404, 
                detail=f"No se encontró el dataset base en la ruta {settings.DATASET_PATH}. "
                       f"Por favor sube o coloca el archivo 'Hipertension_Arterial_Mexico (1).csv' allí."
            )
            
        # Extraer evaluaciones opcionales
        evals_data = payload.evaluations if payload else None
        
        # Entrenar el modelo y obtener las métricas de rendimiento
        metrics = ml_service.train_model(settings.DATASET_PATH, evals_data)
        
        # Al entrenarse con éxito, intentamos forzar a shap_service a resetear su explainer para el nuevo modelo
        from app.services.shap_service import shap_service
        shap_service.explainer = None
        
        return {
            "status": "success",
            "message": "Modelo entrenado y actualizado con éxito en disco.",
            "metrics": metrics
        }
        
    except FileNotFoundError as fnf:
        raise HTTPException(status_code=404, detail=str(fnf))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el entrenamiento del modelo: {str(e)}")

@router.post("/upload-dataset", summary="Subir nuevo dataset para entrenamiento")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Sube un nuevo archivo CSV de datos para reemplazar el dataset actual en disco
    y permitir un entrenamiento actualizado.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Únicamente se permiten archivos en formato CSV.")
        
    try:
        # Asegurar directorio de datos
        os.makedirs(os.path.dirname(settings.DATASET_PATH), exist_ok=True)
        
        # Leer y escribir el archivo
        contents = await file.read()
        with open(settings.DATASET_PATH, "wb") as f:
            f.write(contents)
            
        return {
            "status": "success",
            "message": f"Dataset '{file.filename}' subido y guardado exitosamente en '{settings.DATASET_PATH}'."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al escribir el archivo: {str(e)}")
