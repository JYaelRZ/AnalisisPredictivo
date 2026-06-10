import shap
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from app.services.ml_service import ml_service, LABEL_MAP

# Nombres amigables y médicos en español de cada biomarcador y variable
FEATURE_CLINICAL_NAMES = {
    "sexo": "Sexo",
    "edad": "Edad",
    "peso": "Peso (kg)",
    "estatura": "Estatura (cm)",
    "medida_cintura": "Circunferencia de cintura (cm)",
    "masa_corporal": "Índice de Masa Corporal (IMC)",
    "tension_arterial": "Tensión arterial sistólica (mmHg)",
    "resultado_glucosa": "Glucosa en ayunas (mg/dL)",
    "valor_colesterol_ldl": "Colesterol LDL (mg/dL)",
    "valor_colesterol_hdl": "Colesterol HDL (mg/dL)",
    "valor_colesterol_total": "Colesterol Total (mg/dL)",
    "valor_trigliceridos": "Triglicéridos (mg/dL)",
    "valor_hemoglobina_glucosilada": "Hemoglobina Glucosilada (HbA1c %)",
    "valor_proteinac_reactiva": "Proteína C Reactiva (PCR-hs mg/L)",
    "valor_insulina": "Insulina sérica (uIU/mL)",
    "valor_acido_urico": "Ácido Úrico (mg/dL)",
    "sueno_horas": "Horas de sueño diarias",
    "actividad_total": "Actividad física total (minutos/semana)"
}

class SHAPService:
    def __init__(self):
        self.explainer = None

    def _get_explainer(self):
        """Inicializa de forma perezosa el TreeExplainer de SHAP."""
        if self.explainer is None:
            if ml_service.model is None:
                ml_service.load_model()
            if ml_service.model is not None:
                # TreeExplainer es ideal y muy rápido para XGBoost
                self.explainer = shap.TreeExplainer(ml_service.model)
            else:
                raise RuntimeError("No se puede iniciar SHAP porque el modelo no está cargado.")
        return self.explainer

    def explain_prediction(self, features_dict: Dict[str, float], predicted_class: str) -> Tuple[str, Dict[str, float]]:
        """
        Calcula los valores SHAP para una predicción individual y genera
        una explicación narrativa redactada clínicamente en español.
        """
        try:
            explainer = self._get_explainer()
            
            # Convertir las características a DataFrame con el orden correcto
            df_row = pd.DataFrame([features_dict])[ml_service.features]
            
            # Calcular valores SHAP
            # Para XGBoost multiclase, shap_values es una lista/array de dimensiones:
            # [clases, muestras, características]
            shap_values = explainer.shap_values(df_row)
            
            # Obtener el índice numérico de la clase predicha
            class_idx = LABEL_MAP[predicted_class]
            
            # Extraer las contribuciones (valores SHAP) para la clase predicha en la primera (y única) fila
            # Nota: shap >= 0.45 devuelve un objeto Explanation o un array según la versión.
            # TreeExplainer.shap_values suele retornar un listado de arrays para multiclase.
            if isinstance(shap_values, list):
                class_shap = shap_values[class_idx][0]
            elif isinstance(shap_values, np.ndarray):
                if len(shap_values.shape) == 3:
                    # Shape format is (samples, features, classes)
                    class_shap = shap_values[0, :, class_idx]
                else:
                    class_shap = shap_values[0]
            else:
                class_shap = shap_values[0]
                
            # Mapear características a sus valores SHAP
            shap_map = {feat: float(val) for feat, val in zip(ml_service.features, class_shap)}
            
            # Generar la explicación clínica narrativa
            narrative = self._generate_narrative(features_dict, shap_map, predicted_class)
            
            return narrative, shap_map
            
        except Exception as e:
            # Fallback en caso de que SHAP falle por temas de inicialización (ej. modelo no entrenado aún)
            fallback_narrative = (
                f"Predicción del sistema basada en reglas de decisión clínica. "
                f"El análisis de SHAP no está disponible temporalmente ({str(e)})."
            )
            return fallback_narrative, {feat: 0.0 for feat in ml_service.features}

    def _generate_narrative(self, features: Dict[str, float], shap_values: Dict[str, float], predicted_class: str) -> str:
        """
        Analiza las contribuciones SHAP positivas y negativas para estructurar una explicación
        médica coherente sobre qué factores impulsan o mitigan el riesgo cardiovascular,
        adaptada al grupo de edad del paciente según los rangos del Notion.
        """
        # Obtener contexto de edad
        age = features.get("edad", 45)
        if age < 30:
            age_group = "un paciente joven (18-29 años)"
        elif age < 45:
            age_group = "un adulto temprano (30-44 años)"
        elif age < 55:
            age_group = "un adulto medio (45-54 años)"
        else:
            age_group = "un adulto en edad avanzada (>=55 años)"

        # Clasificar variables por impacto (excluyendo el sexo para la narrativa si no es muy relevante, o manteniéndolo)
        sorted_impact = sorted(shap_values.items(), key=lambda item: item[1], reverse=True)
        
        # Factores de riesgo (SHAP positivo: aumentan la probabilidad de la clase predicha)
        risk_drivers = [item for item in sorted_impact if item[1] > 0.01][:3]
        
        # Factores protectores o mitigantes (SHAP negativo: reducen la probabilidad)
        protective_factors = [item for item in sorted_impact if item[1] < -0.01][-3:]
        protective_factors.reverse() # De más protector a menos protector

        # Formatear el valor real clínico
        def get_val_str(feat: str) -> str:
            val = features[feat]
            if feat == "sexo":
                return "Femenino" if val == 1 else "Masculino"
            elif feat == "valor_hemoglobina_glucosilada":
                return f"{val}%"
            elif feat in ["valor_colesterol_ldl", "valor_colesterol_total", "valor_colesterol_hdl", "valor_trigliceridos", "resultado_glucosa"]:
                return f"{val} mg/dL"
            elif feat == "valor_proteinac_reactiva":
                return f"{val} mg/L"
            elif feat == "masa_corporal":
                return f"{val} kg/m²"
            elif feat == "tension_arterial":
                return f"{val} mmHg"
            elif feat == "estatura":
                return f"{val} cm"
            elif feat == "valor_acido_urico":
                return f"{val} mg/dL"
            elif feat == "actividad_total":
                return f"{int(val)} min/sem"
            elif feat == "sueno_horas":
                return f"{val} hrs/día"
            return str(val)

        if predicted_class == "Bajo":
            narrative = f"Para {age_group}, el paciente muestra homeostasis metabólica y cardiovascular general. "
            if risk_drivers:
                factors_str = ", ".join([f"{FEATURE_CLINICAL_NAMES[f]} ({get_val_str(f)})" for f, v in risk_drivers[:2]])
                narrative += f"Esto es impulsado principalmente por valores estables en: {factors_str}. "
            if protective_factors:
                prot_str = ", ".join([f"{FEATURE_CLINICAL_NAMES[f]} ({get_val_str(f)})" for f, v in protective_factors[:2]])
                narrative += f"No se observan desequilibrios críticos en {prot_str} que amenacen su perfil de bajo riesgo."
                
        elif predicted_class == "Medio":
            narrative = f"Para {age_group}, el paciente presenta un nivel de riesgo cardiovascular MEDIO (riesgo subclínico o factores aislados). "
            if risk_drivers:
                factors_str = ", ".join([f"{FEATURE_CLINICAL_NAMES[f]} ({get_val_str(f)})" for f, v in risk_drivers])
                narrative += f"Este riesgo está impulsado principalmente por anomalías moderadas en: {factors_str}. "
            if protective_factors:
                prot_str = ", ".join([f"{FEATURE_CLINICAL_NAMES[f]} ({get_val_str(f)})" for f, v in protective_factors[:2]])
                narrative += f"Sin embargo, factores como {prot_str} ayudan a mitigar la progresión a un nivel de riesgo alto por el momento."
                
        else: # Alto
            narrative = f"⚠️ ALERTA CLÍNICA: Para {age_group}, el paciente se encuentra en un nivel de riesgo cardiovascular ALTO. "
            if risk_drivers:
                factors_str = ", ".join([f"{FEATURE_CLINICAL_NAMES[f]} ({get_val_str(f)})" for f, v in risk_drivers])
                narrative += f"Este nivel de riesgo crítico es detonado de forma combinada por valores elevados o descontrolados de: {factors_str}. "
            if protective_factors:
                prot_str = ", ".join([f"{FEATURE_CLINICAL_NAMES[f]} ({get_val_str(f)})" for f, v in protective_factors[:2]])
                narrative += f"Valores en rangos más estables de {prot_str} son insuficientes para contrarrestar el perfil inflamatorio/glucotóxico general."
            else:
                narrative += "No se identificaron factores protectores significativos en el perfil metabólico actual."

        return narrative

shap_service = SHAPService()
