import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Configurar stdout para usar UTF-8 y soportar emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Asegurar que el directorio de la app esté en el path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ml_service import ml_service
from app.services.shap_service import shap_service, FEATURE_CLINICAL_NAMES

# Configuración de página de Streamlit
st.set_page_config(
    page_title="CDSS - Riesgo Cardiovascular México",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilización con CSS para lograr una UI médica premium
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .reportview-container {
        background: #f8fafc;
    }
    h1 {
        color: #1e293b;
        font-family: 'Outfit', 'Inter', sans-serif;
        font-weight: 700;
    }
    h3 {
        color: #334155;
    }
    .stButton>button {
        background-color: #0f172a;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #1e293b;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .card {
        background-color: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05), 0 2px 4px -2px rgb(0 0 0 / 0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    .badge-bajo {
        background-color: #dcfce7;
        color: #15803d;
        padding: 6px 16px;
        border-radius: 9999px;
        font-weight: 700;
        display: inline-block;
        font-size: 1.1rem;
        border: 1px solid #bbf7d0;
    }
    .badge-medio {
        background-color: #fef9c3;
        color: #a16207;
        padding: 6px 16px;
        border-radius: 9999px;
        font-weight: 700;
        display: inline-block;
        font-size: 1.1rem;
        border: 1px solid #fef08a;
    }
    .badge-alto {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 6px 16px;
        border-radius: 9999px;
        font-weight: 700;
        display: inline-block;
        font-size: 1.1rem;
        border: 1px solid #fecaca;
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: .8; }
    }
    </style>
""", unsafe_allow_html=True)

# Título y encabezado principal
st.markdown("""
    <div style='display: flex; align-items: center; gap: 16px; margin-bottom: 10px;'>
        <span style='font-size: 3rem;'>🩺</span>
        <div>
            <h1 style='margin: 0; font-size: 2.2rem;'>Sistema de Soporte a la Decisión Clínica (CDSS)</h1>
            <p style='margin: 0; color: #64748b; font-size: 1rem;'>Predicción de 3 niveles de Riesgo de Enfermedad Cardiovascular (ECV) en Adultos Mexicanos</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Verificar si el modelo está entrenado y cargado
if ml_service.model is None:
    ml_service.load_model()

if ml_service.model is None:
    st.error("⚠️ El modelo XGBoost no está cargado. Asegúrate de colocar el dataset en la carpeta `data` y realizar el entrenamiento inicial llamando al backend.")
    st.info("💡 Si acabas de agregar el dataset, puedes presionar el siguiente botón para entrenar el modelo ahora mismo:")
    if st.button("🚀 Entrenar Modelo Clínico con Dataset Real"):
        with st.spinner("Entrenando XGBoost con SMOTE y validando recall..."):
            try:
                metrics = ml_service.train_model("data/Hipertension_Arterial_Mexico (1).csv")
                st.success("¡Modelo entrenado y listo para inferencia!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error al entrenar: {str(e)}")
    st.stop()

# Diseño de dos columnas principales: Formulario a la izquierda, Diagnóstico a la derecha
col_inputs, col_results = st.columns([1.1, 1.2], gap="large")

# Inicialización de diccionario para capturar datos
paciente_data = {}

with col_inputs:
    st.markdown("### 📋 Datos Fisiológicos y Biomarcadores")
    st.write("Ingrese los parámetros clínicos obtenidos del expediente y laboratorio del paciente.")
    
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        # Categoría 1: Datos Demográficos y Antropometría
        st.markdown("##### 👤 Antropometría y Demografía")
        c1, c2 = st.columns(2)
        with c1:
            paciente_data["sexo"] = st.selectbox("Sexo del paciente:", ["Mujer", "Hombre"])
            paciente_data["edad"] = st.slider("Edad (años):", 18, 100, 45)
            paciente_data["peso"] = st.number_input("Peso (kg):", min_value=30.0, max_value=200.0, value=75.0, step=0.1)
        with c2:
            paciente_data["medida_cintura"] = st.number_input("Circunferencia de Cintura (cm):", min_value=40.0, max_value=180.0, value=90.0, step=0.1)
            # Calcular IMC automático pero permitir edición
            imc_calculado = float(paciente_data["peso"] / ((1.70)**2)) # Asumiendo altura estándar para precargar
            paciente_data["masa_corporal"] = st.number_input("Índice de Masa Corporal (IMC):", min_value=10.0, max_value=60.0, value=round(imc_calculado, 1), step=0.1)
            paciente_data["tension_arterial"] = st.number_input("Tensión Arterial Sistólica (mmHg):", min_value=70.0, max_value=220.0, value=120.0, step=1.0)
            
        st.markdown("---")
        
        # Categoría 2: Laboratorio Clínico (Biomarcadores metabólicos e inflamatorios)
        st.markdown("##### 🔬 Biomarcadores de Laboratorio")
        c3, c4 = st.columns(2)
        with c3:
            paciente_data["valor_colesterol_ldl"] = st.number_input("Colesterol LDL (mg/dL):", min_value=30.0, max_value=250.0, value=115.0, step=1.0)
            paciente_data["valor_colesterol_total"] = st.number_input("Colesterol Total (mg/dL):", min_value=50.0, max_value=450.0, value=195.0, step=1.0)
            paciente_data["valor_hemoglobina_glucosilada"] = st.number_input("Hemoglobina Glucosilada (HbA1c %):", min_value=3.0, max_value=18.0, value=5.6, step=0.1, help="Marcador de glucotoxicidad")
        with c4:
            paciente_data["valor_proteinac_reactiva"] = st.number_input("Proteína C Reactiva (PCR-hs mg/L):", min_value=0.01, max_value=40.0, value=1.5, step=0.01, help="Marcador de inflamación sistémica y estabilidad de placa de ateroma")
            paciente_data["valor_insulina"] = st.number_input("Insulina Sérica (uIU/mL):", min_value=0.5, max_value=80.0, value=12.0, step=0.1)
            
        st.markdown("---")
        
        # Categoría 3: Estilo de Vida
        st.markdown("##### 🏃 Estilo de Vida y Hábitos")
        c5, c6 = st.columns(2)
        with c5:
            paciente_data["sueno_horas"] = st.slider("Horas de Sueño diarias:", 3.0, 12.0, 7.0, 0.5)
        with c6:
            paciente_data["actividad_total"] = st.number_input("Actividad Física (minutos/semana):", min_value=0.0, max_value=900.0, value=150.0, step=10.0)
            
        st.markdown("</div>", unsafe_allow_html=True)

with col_results:
    st.markdown("### 📊 Evaluación Diagnóstica CDSS")
    st.write("Resultado predictivo y explicabilidad clínica generada por Inteligencia Artificial en tiempo real.")
    
    # Realizar inferencia clínica y SHAP de forma reactiva al cambiar inputs
    try:
        prediction = ml_service.predict_risk(paciente_data)
        nivel = prediction["nivel_riesgo"]
        probabilidad = prediction["probabilidad_porcentual"]
        distribucion = prediction["distribucion_probabilidades"]
        features_proc = prediction["features_processed"]
        
        # Obtener valores SHAP
        explicacion, valores_shap = shap_service.explain_prediction(features_proc, nivel)
        
        # 1. Renderizar Badge clínico y probabilidad principal
        st.markdown("<div class='card' style='text-align: center; padding: 30px;'>", unsafe_allow_html=True)
        st.write("NIVEL DE RIESGO CARDIOVASCULAR ESTIMADO:")
        
        if nivel == "Bajo":
            st.markdown(f"<span class='badge-bajo'>🟢 RIESGO {nivel.upper()}</span>", unsafe_allow_html=True)
        elif nivel == "Medio":
            st.markdown(f"<span class='badge-medio'>🟡 RIESGO {nivel.upper()}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span class='badge-alto'>🔴 RIESGO {nivel.upper()}</span>", unsafe_allow_html=True)
            
        st.markdown(f"<h2 style='margin-top: 15px; font-weight: 800; color: #0f172a;'>{probabilidad}% <span style='font-size: 1.1rem; color: #64748b; font-weight: normal;'>de certeza diagnóstica</span></h2>", unsafe_allow_html=True)
        
        # Gauge de probabilidad minimalista
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = probabilidad,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Probabilidad del Riesgo Predicho", 'font': {'size': 14}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                'bar': {'color': "#0f172a" if nivel != "Alto" else "#b91c1c"},
                'bgcolor': "white",
                'borderwidth': 1,
                'bordercolor': "#cbd5e1",
                'steps': [
                    {'range': [0, 33], 'color': '#f0fdf4'},
                    {'range': [33, 66], 'color': '#fef9c3'},
                    {'range': [66, 100], 'color': '#fee2e2'}
                ],
            }
        ))
        fig_gauge.update_layout(height=180, margin=dict(t=30, b=0, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 2. Explicación Narrativa Médica (SHAP)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("##### 🧬 Análisis de Explicabilidad Clínica (Valores SHAP)")
        st.info(explicacion)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 3. Gráfico de Barras SHAP Interactiva
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("##### 📊 Aporte de cada Biomarcador al Diagnóstico")
        st.write("Las barras muestran qué variables empujaron el riesgo del paciente hacia este resultado (valores positivos aumentan el riesgo; negativos actúan como protectores).")
        
        # Ordenar valores SHAP para graficarlos
        shap_df = pd.DataFrame([
            {"Característica": FEATURE_CLINICAL_NAMES.get(k, k), "Impacto (SHAP)": v} 
            for k, v in valores_shap.items()
        ]).sort_values(by="Impacto (SHAP)", key=abs, ascending=True)
        
        # Filtrar impactos significativos para no saturar el gráfico
        shap_df = shap_df[shap_df["Impacto (SHAP)"].abs() > 0.005]
        
        if not shap_df.empty:
            colors = ['#ef4444' if x >= 0 else '#22c55e' for x in shap_df["Impacto (SHAP)"]]
            fig_shap = go.Figure()
            fig_shap.add_trace(go.Bar(
                y=shap_df["Característica"],
                x=shap_df["Impacto (SHAP)"],
                orientation='h',
                marker_color=colors,
                hovertemplate="Variable: %{y}<br>Impacto SHAP: %{x:.4f}<extra></extra>"
            ))
            fig_shap.update_layout(
                height=350,
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(title="Dirección del Impacto (SHAP)", gridcolor="#f1f5f9"),
                yaxis=dict(gridcolor="#f1f5f9")
            )
            st.plotly_chart(fig_shap, use_container_width=True)
        else:
            st.write("No hay impactos significativos registrados para este perfil de variables.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error al computar la decisión clínica: {str(e)}")
        import traceback
        st.code(traceback.format_exc())
