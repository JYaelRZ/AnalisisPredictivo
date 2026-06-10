import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env si existe
load_dotenv()

class Settings:
    PROJECT_NAME: str = "CVD Decision Support System API"
    VERSION: str = "1.0.0"
    API_STR: str = "/api/v1"
    
    # Configuración de base de datos y seguridad (Supabase)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    # Configuración del modelo
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/cvd_xgb_model.json")
    DATASET_PATH: str = os.getenv("DATASET_PATH", "data/Hipertension_Arterial_Mexico (1).csv")

settings = Settings()
