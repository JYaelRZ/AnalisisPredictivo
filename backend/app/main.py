from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import predict, train
from app.services.ml_service import ml_service

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API CDSS de soporte de diagnóstico para predecir 3 niveles de riesgo de Enfermedades Cardiovasculares (ECV) mediante biomarcadores, basado en XGBoost.",
    version=settings.VERSION,
)

# Configurar CORS para permitir comunicación fluida con Next.js (tanto local como en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modificar con URLs específicas en producción (ej. Vercel)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas desacopladas
app.include_router(predict.router, prefix=settings.API_STR, tags=["Inferencia"])
app.include_router(train.router, prefix=settings.API_STR, tags=["Entrenamiento"])

@app.get("/", tags=["Salud"])
async def root():
    """Endpoint básico para comprobar el estado y disponibilidad de la API."""
    model_loaded = ml_service.model is not None
    return {
        "api": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "model_loaded": model_loaded,
        "features_required": ml_service.features,
        "message": "Sistema de Soporte de Decisiones Clínicas (CDSS) funcionando correctamente."
    }

if __name__ == "__main__":
    import uvicorn
    # Ejecución manual local
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
