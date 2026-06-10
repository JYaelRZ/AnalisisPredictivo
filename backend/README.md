# CVD CDSS Backend API

Este es el backend de Machine Learning y API para la **Plataforma web de predicción del riesgo de Enfermedades Cardiovasculares (ECV)** en adultos mexicanos. Construido sobre **FastAPI**, integra un modelo de clasificación multiclase **XGBoost** entrenado con datos de la ENSANUT (Encuesta Nacional de Salud y Nutrición), balanceo de datos mediante **SMOTE** y explicabilidad clínica en español provista por **SHAP**.

---

## 🛠️ Tecnologías y Librerías Utilizadas

*   **FastAPI:** Framework moderno, de alto rendimiento y fácil de documentar para construir APIs en Python.
*   **XGBoost:** Algoritmo de Gradient Boosting optimizado para predicciones de alta precisión sobre datos clínicos tabulares.
*   **SMOTE (imbalanced-learn):** Técnica de sobremuestreo sintético de minorías para balancear los casos de "Riesgo Alto" y "Riesgo Medio" en el dataset, mejorando la sensibilidad (Recall).
*   **SHAP (SHapley Additive exPlanations):** Engine matemático para explicar de forma individualizada las predicciones y brindar argumentos comprensibles a los médicos clínicos.
*   **Pydantic:** Validación estricta y tipado de datos de entrada/salida.

---

## 📂 Estructura del Proyecto Backend

```text
backend/
├── app/
│   ├── main.py              # Punto de arranque y middlewares (CORS)
│   ├── config.py            # Gestión de variables de entorno (.env)
│   ├── schemas.py           # Esquemas Pydantic para el API
│   ├── routes/
│   │   ├── predict.py       # Endpoint de inferencia /predict con SHAP
│   │   └── train.py         # Endpoints de reentrenamiento continuo /train
│   └── services/
│       ├── ml_service.py    # Pipeline de datos, SMOTE y entrenamiento XGBoost
│       └── shap_service.py  # Generador de explicaciones narrativas de SHAP
├── data/
│   └── Hipertension_Arterial_Mexico (1).csv # Dataset base (ENSANUT)
├── models/
│   └── cvd_xgb_model.json   # Archivo JSON del modelo XGBoost entrenado
├── requirements.txt         # Dependencias del sistema
└── .env                     # Archivo de configuración local (no versionado)
```

---

## 🚀 Instalación y Uso Local

### 1. Inicializar el Entorno Virtual de Python (Windows)
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 2. Instalar Dependencias
```powershell
pip install -r requirements.txt
```

### 3. Ejecutar el Servidor en Desarrollo
```powershell
# Desde el directorio root del backend (asegurar tener la carpeta app en el path)
python -m uvicorn app.main:app --reload --port 8000
```
La API estará disponible localmente en `http://localhost:8000`.

### 4. Documentación Interactiva
FastAPI autogenera documentación OpenAPI enriquecida a la que puedes acceder desde:
*   Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
*   ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧬 Endpoints Principales

### 1. Inferencia: `POST /api/v1/predict`
Recibe los biomarcadores del paciente y devuelve la predicción multiclase con soporte explicativo de SHAP.

**Payload de Ejemplo:**
```json
{
  "sexo": "Mujer",
  "edad": 52,
  "peso": 83.2,
  "medida_cintura": 102.5,
  "masa_corporal": 31.6,
  "tension_arterial": 142.0,
  "valor_colesterol_ldl": 145.0,
  "valor_colesterol_total": 235.0,
  "valor_hemoglobina_glucosilada": 6.8,
  "valor_proteinac_reactiva": 3.8,
  "valor_insulina": 18.5,
  "sueno_horas": 5.5,
  "actividad_total": 60
}
```

**Respuesta de Ejemplo:**
```json
{
  "nivel_riesgo": "Alto",
  "probabilidad_porcentual": 89.42,
  "distribucion_probabilidades": {
    "Bajo": 2.15,
    "Medio": 8.43,
    "Alto": 89.42
  },
  "explicacion_clinica": "⚠️ ALERTA CLÍNICA: Paciente en nivel de riesgo cardiovascular ALTO. Este nivel de riesgo crítico es detonado de forma combinada por valores elevados o descontrolados de: Hemoglobina Glucosilada (HbA1c %) (6.8%), Proteína C Reactiva (PCR-hs mg/L) (3.8 mg/L), Colesterol LDL (mg/dL) (145.0 mg/dL).",
  "valores_shap": {
    "sexo": -0.05,
    "edad": 0.12,
    "peso": 0.08,
    ...
  }
}
```

### 2. Entrenamiento: `POST /api/v1/train`
Ejecuta el pipeline clínico completo: aplica el script metodológico de Label Engineering para crear la variable `riesgo_cvd_3_niveles`, descarta la columna original de riesgo de hipertensión para prevenir *Data Leakage*, aplica balanceo de clases mediante SMOTE, y entrena un nuevo clasificador XGBoost evaluando su Sensibilidad (Recall > 90%).
