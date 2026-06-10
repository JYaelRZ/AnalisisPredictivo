import os
import pickle
import json
import pandas as pd
import numpy as np
from typing import Dict, Tuple, Any
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from app.config import settings

# Mapeo de variables categóricas de texto a numéricas y viceversa
LABEL_MAP = {"Bajo": 0, "Medio": 1, "Alto": 2}
INV_LABEL_MAP = {0: "Bajo", 1: "Medio", 2: "Alto"}

def stratify_cvd_risk(row: pd.Series) -> str:
    """
    Estratifica el riesgo cardiovascular en 3 niveles (Bajo, Medio, Alto)
    basado en rangos clínicos por edad del documento de Notion.
    """
    age = row['edad']
    sex = int(row['sexo']) # 1 = Hombre, 2 = Mujer en ENSANUT
    ht_risk = row['riesgo_hipertension']
    hba1c = row['valor_hemoglobina_glucosilada']
    ldl = row['valor_colesterol_ldl']
    hdl = row['valor_colesterol_hdl']
    tg = row['valor_trigliceridos']
    glu = row['resultado_glucosa']
    pcr_hs = row['valor_proteinac_reactiva']
    imc = row['masa_corporal']
    ta = row['tension_arterial']
    
    # Mapeo de HDL bajo según sexo (0 = Hombre, 1 = Mujer en el preprocesamiento homologado)
    # En ENSANUT el valor original es 1 (Hombre) y 2 (Mujer)
    is_male = (sex == 1)
    hdl_low = hdl < 40 if is_male else hdl < 50

    if age < 30: # Jóvenes (18-29)
        # ALTO
        if hba1c >= 6.5 or glu >= 126:
            return 'Alto'
        if ldl >= 160 or tg >= 500 or ta >= 140:
            return 'Alto'
        if ht_risk == 1 and (ldl >= 130 or pcr_hs > 3.0 or hba1c >= 5.7):
            return 'Alto'
        
        # MEDIO
        if ht_risk == 1:
            return 'Medio'
        if hba1c >= 5.7 or glu >= 100:
            return 'Medio'
        if ldl >= 130 or tg >= 200:
            return 'Medio'
        if ta >= 130:
            return 'Medio'
        if imc >= 30 and pcr_hs >= 1.0:
            return 'Medio'
            
    elif age < 45: # Adultos Tempranos (30-44)
        # ALTO
        if hba1c >= 6.5 or glu >= 126:
            return 'Alto'
        if ldl >= 160 or tg >= 500 or ta >= 140:
            return 'Alto'
        if ht_risk == 1 and (ldl >= 130 or pcr_hs > 3.0 or hba1c >= 5.7):
            return 'Alto'
            
        # MEDIO
        if ht_risk == 1:
            return 'Medio'
        if hba1c >= 5.7 or glu >= 100:
            return 'Medio'
        if ldl >= 130 or tg >= 200:
            return 'Medio'
        if ta >= 130:
            return 'Medio'
        if imc >= 30 and pcr_hs >= 1.0:
            return 'Medio'
            
    elif age < 55: # Adultos Medios (45-54)
        # ALTO
        if hba1c >= 6.5 or glu >= 126:
            return 'Alto'
        if ldl >= 130 or tg >= 500 or ta >= 135 or pcr_hs > 3.0:
            return 'Alto'
        if ht_risk == 1 and (ldl >= 100 or hba1c >= 5.7):
            return 'Alto'
            
        # MEDIO
        if ht_risk == 1:
            return 'Medio'
        if hba1c >= 5.7 or glu >= 100:
            return 'Medio'
        if ldl >= 100 or tg >= 200:
            return 'Medio'
        if ta >= 125:
            return 'Medio'
        if imc >= 28 and pcr_hs >= 1.0:
            return 'Medio'
            
    else: # Mayores Tempranos & Mayores (>= 55)
        # ALTO
        if hba1c >= 6.5 or glu >= 126:
            return 'Alto'
        if ldl >= 130 or pcr_hs > 3.0 or ta >= 135:
            return 'Alto'
        if ht_risk == 1 and (ldl >= 100 or hba1c >= 5.7 or ta >= 130):
            return 'Alto'
        if tg >= 200 and (imc >= 25 or hdl_low):
            return 'Alto'
            
        # MEDIO
        if ht_risk == 1 or ta >= 125:
            return 'Medio'
        if hba1c >= 5.7 or glu >= 100:
            return 'Medio'
        if ldl >= 100 or tg >= 150:
            return 'Medio'
        if imc >= 25 and pcr_hs >= 1.0:
            return 'Medio'

    return 'Bajo'

class MLService:
    def __init__(self):
        self.model: XGBClassifier = None
        self.features = [
            "sexo", "edad", "peso", "estatura", "medida_cintura", "masa_corporal", 
            "tension_arterial", "resultado_glucosa", "valor_colesterol_ldl", 
            "valor_colesterol_hdl", "valor_colesterol_total", "valor_trigliceridos",
            "valor_hemoglobina_glucosilada", "valor_proteinac_reactiva", 
            "valor_insulina", "valor_acido_urico", "sueno_horas", "actividad_total"
        ]
        # Intentar cargar el modelo si ya existe
        self.load_model()

    def load_model(self) -> bool:
        """Carga el modelo XGBoost desde la ruta especificada en configuración."""
        if os.path.exists(settings.MODEL_PATH):
            try:
                self.model = XGBClassifier()
                self.model.load_model(settings.MODEL_PATH)
                print(f"Modelo cargado exitosamente desde {settings.MODEL_PATH}")
                return True
            except Exception as e:
                print(f"Error al cargar el modelo: {str(e)}")
        return False

    def preprocess_sex(self, val: Any) -> int:
        """Mapea el sexo de texto/numérico a entero (0 = Hombre, 1 = Mujer)."""
        if isinstance(val, str):
            clean_val = val.strip().lower()
            if clean_val in ['hombre', 'h', 'masculino', '1']:
                return 0
            if clean_val in ['mujer', 'm', 'femenino', '0', '2']:
                return 1
        elif isinstance(val, (int, float)):
            val_int = int(val)
            if val_int == 1: # Hombre en ENSANUT
                return 0
            elif val_int == 2 or val_int == 0: # Mujer en ENSANUT
                return 1
        return 0

    def preprocess_dataframe(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Aplica la ingeniería de etiquetas y el preprocesamiento del dataframe."""
        df_processed = df.copy()
        
        # 1. Label Engineering
        df_processed['riesgo_cvd_3_niveles'] = df_processed.apply(stratify_cvd_risk, axis=1)
        
        # 2. Descartar la variable original riesgo_hipertension para evitar Data Leakage
        if 'riesgo_hipertension' in df_processed.columns:
            df_processed = df_processed.drop(columns=['riesgo_hipertension'])
            
        # 3. Preprocesar 'sexo'
        df_processed['sexo'] = df_processed['sexo'].apply(self.preprocess_sex)
        
        # 4. Asegurar que las variables de entrada sean numéricas y no contengan nulos en las predictoras
        for col in self.features:
            df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
            # Imputar con la mediana de entrenamiento en caso de valores nulos (el usuario indica que no hay nulos, pero es por robustez)
            df_processed[col] = df_processed[col].fillna(df_processed[col].median())

        X = df_processed[self.features]
        y = df_processed['riesgo_cvd_3_niveles'].map(LABEL_MAP)
        
        return X, y

    def train_model(self, data_path: str, new_evaluations: list = None) -> Dict[str, Any]:
        """
        Entrena el modelo XGBoost a partir de un archivo CSV base (ENSANUT)
        y opcionalmente combina nuevas evaluaciones del consultorio aplicando SMOTE,
        y evalúa la sensibilidad. Guarda el modelo localmente.
        """
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"No se encontró el dataset en la ruta: {data_path}")
            
        df = pd.read_csv(data_path)
        X, y = self.preprocess_dataframe(df)
        
        # Si hay nuevas evaluaciones, las combinamos con el dataset base
        if new_evaluations:
            df_new = pd.DataFrame(new_evaluations)
            
            # Preprocesar sexo e imputar variables
            df_new['sexo'] = df_new['sexo'].apply(self.preprocess_sex)
            for col in self.features:
                if col not in df_new.columns:
                    df_new[col] = df[col].median() if col in df.columns else 0.0
                df_new[col] = pd.to_numeric(df_new[col], errors='coerce')
                df_new[col] = df_new[col].fillna(df[col].median() if col in df.columns else 0.0)
                
            X_new = df_new[self.features]
            
            # Obtener etiqueta target
            # resultado_real (doctor gold standard) tiene prioridad, de lo contrario nivel_riesgo_predicho
            target_series = pd.Series([None] * len(df_new))
            if 'resultado_real' in df_new.columns:
                target_series = df_new['resultado_real']
            elif 'diagnostico_real' in df_new.columns:
                target_series = df_new['diagnostico_real']
                
            if 'nivel_riesgo_predicho' in df_new.columns:
                target_series = target_series.fillna(df_new['nivel_riesgo_predicho'])
                
            target_series = target_series.fillna('Bajo')
            y_new = target_series.map(LABEL_MAP).fillna(0).astype(int)
            
            # Concatenar con los datos base
            X = pd.concat([X, X_new], ignore_index=True)
            y = pd.concat([y, y_new], ignore_index=True)
            
        # Dividir datos en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Aplicar SMOTE para sobremuestrear las clases minoritarias (Alto y Medio) en entrenamiento
        smote = SMOTE(random_state=42)
        X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
        
        # Inicializar y entrenar el clasificador XGBoost con enfoque multiclase
        # Maximizamos recall configurando hiperparámetros balanceados
        self.model = XGBClassifier(
            objective='multi:softprob',
            num_class=3,
            eval_metric='mlogloss',
            random_state=42,
            max_depth=6,
            learning_rate=0.1,
            n_estimators=150,
            subsample=0.8,
            colsample_bytree=0.8
        )
        
        self.model.fit(X_train_res, y_train_res)
        
        # Evaluar el modelo en datos de prueba
        y_pred = self.model.predict(X_test)
        
        # Generar métricas de reporte
        report = classification_report(
            y_test, y_pred, target_names=["Bajo", "Medio", "Alto"], output_dict=True
        )
        conf_mat = confusion_matrix(y_test, y_pred).tolist()
        
        # Asegurar directorio de modelos y guardar
        os.makedirs(os.path.dirname(settings.MODEL_PATH), exist_ok=True)
        self.model.save_model(settings.MODEL_PATH)
        
        # Guardar estadísticas de entrenamiento para la UI del CDSS
        metrics = {
            "accuracy": report["accuracy"],
            "recall_bajo": report["Bajo"]["recall"],
            "recall_medio": report["Medio"]["recall"],
            "recall_alto": report["Alto"]["recall"],
            "precision_bajo": report["Bajo"]["precision"],
            "precision_medio": report["Medio"]["precision"],
            "precision_alto": report["Alto"]["precision"],
            "f1_alto": report["Alto"]["f1-score"],
            "matriz_confusion": conf_mat,
            "total_registros_ensanut": len(df),
            "total_registros_combinado": len(X),
            "distribucion_clases_original": {INV_LABEL_MAP[k]: int(v) for k, v in y.value_counts().to_dict().items()}
        }
        
        return metrics

    def predict_risk(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza la predicción de riesgo para un nuevo registro de paciente.
        """
        if self.model is None:
            # Intentar recargar
            if not self.load_model():
                raise RuntimeError("El modelo no está entrenado ni cargado en memoria.")
        
        # Preparar la entrada como DataFrame de 1 fila
        df_input = pd.DataFrame([input_data])
        
        # Preprocesar variables individuales
        df_input['sexo'] = df_input['sexo'].apply(self.preprocess_sex)
        for col in self.features:
            df_input[col] = pd.to_numeric(df_input[col], errors='coerce')
            
        X_input = df_input[self.features]
        
        # Realizar predicción de clase y probabilidades
        pred_class_encoded = self.model.predict(X_input)[0]
        probabilities = self.model.predict_proba(X_input)[0]
        
        nivel_riesgo = INV_LABEL_MAP[int(pred_class_encoded)]
        prob_porcentual = float(probabilities[int(pred_class_encoded)] * 100)
        
        distribucion = {
            "Bajo": float(probabilities[0] * 100),
            "Medio": float(probabilities[1] * 100),
            "Alto": float(probabilities[2] * 100)
        }
        
        return {
            "nivel_riesgo": nivel_riesgo,
            "probabilidad_porcentual": round(prob_porcentual, 2),
            "distribucion_probabilidades": {k: round(v, 2) for k, v in distribucion.items()},
            "features_processed": X_input.iloc[0].to_dict()
        }

ml_service = MLService()
