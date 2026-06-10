import psycopg2
import uuid
import json
from datetime import datetime, timedelta

def create_patients():
    conn_str = "postgresql://postgres:kVvVVGsFc150i2rt@db.vlftdeynabukgoazxrwd.supabase.co:5432/postgres"
    doctor_uuid = "70af24be-6be4-4e7d-ac3f-d4399be0ff0d" # evaluador@cardio.fit UUID
    
    print("Conectando a la base de datos Supabase...")
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    
    patients_data = [
        {
            "id": str(uuid.uuid4()),
            "first_name": "Carlos",
            "last_name": "Ramírez Soto",
            "curp": "RASC850210HDFRNS08",
            "fecha_nacimiento": "1985-02-10",
            "activo": True,
            "eval": {
                "id": str(uuid.uuid4()),
                "sexo": "Hombre",
                "edad": 41,
                "peso": 72.5,
                "medida_cintura": 85.0,
                "masa_corporal": 22.8,
                "tension_arterial": 115.0,
                "valor_colesterol_ldl": 88.0,
                "valor_colesterol_total": 175.0,
                "valor_hemoglobina_glucosilada": 5.1,
                "valor_proteinac_reactiva": 0.4,
                "valor_insulina": 8.0,
                "sueno_horas": 7.5,
                "actividad_total": 180.0,
                "nivel_riesgo_predicho": "Bajo",
                "probabilidad_predicha": 96.2,
                "distribucion_probabilidades": {"Bajo": 96.2, "Medio": 3.3, "Alto": 0.5},
                "explicacion_shap": "El paciente presenta homeostasis metabolica y cardiovascular general. Esto es impulsado principalmente por valores estables en HbA1c (5.1%) y Proteina C Reactiva (0.4 mg/L).",
                "valores_shap": {"valor_hemoglobina_glucosilada": -0.32, "valor_proteinac_reactiva": -0.28, "valor_colesterol_ldl": -0.15},
                "resultado_real": "Bajo"
            }
        },
        {
            "id": str(uuid.uuid4()),
            "first_name": "Beatriz Elena",
            "last_name": "Gómez Ruiz",
            "curp": "GOMB740618MDFRNS02",
            "fecha_nacimiento": "1974-06-18",
            "activo": True,
            "eval": {
                "id": str(uuid.uuid4()),
                "sexo": "Mujer",
                "edad": 52,
                "peso": 78.5,
                "medida_cintura": 89.0,
                "masa_corporal": 28.2,
                "tension_arterial": 128.0,
                "valor_colesterol_ldl": 124.0,
                "valor_colesterol_total": 210.0,
                "valor_hemoglobina_glucosilada": 6.1,
                "valor_proteinac_reactiva": 1.8,
                "valor_insulina": 14.2,
                "sueno_horas": 6.0,
                "actividad_total": 90.0,
                "nivel_riesgo_predicho": "Medio",
                "probabilidad_predicha": 84.6,
                "distribucion_probabilidades": {"Bajo": 8.5, "Medio": 84.6, "Alto": 6.9},
                "explicacion_shap": "El paciente presenta un nivel de riesgo cardiovascular MEDIO. Este riesgo esta impulsado principalmente por anomalias moderadas en Colesterol LDL (124 mg/dL) y Hemoglobina Glucosilada (6.1%).",
                "valores_shap": {"valor_colesterol_ldl": 0.18, "valor_hemoglobina_glucosilada": 0.16, "valor_proteinac_reactiva": 0.12},
                "resultado_real": "Medio"
            }
        },
        {
            "id": str(uuid.uuid4()),
            "first_name": "Fernando Javier",
            "last_name": "Ortíz López",
            "curp": "ORTF601130HDFRNS05",
            "fecha_nacimiento": "1960-11-30",
            "activo": True,
            "eval": {
                "id": str(uuid.uuid4()),
                "sexo": "Hombre",
                "edad": 65,
                "peso": 92.0,
                "medida_cintura": 108.0,
                "masa_corporal": 31.8,
                "tension_arterial": 148.0,
                "valor_colesterol_ldl": 178.0,
                "valor_colesterol_total": 265.0,
                "valor_hemoglobina_glucosilada": 7.6,
                "valor_proteinac_reactiva": 4.8,
                "valor_insulina": 26.0,
                "sueno_horas": 5.0,
                "actividad_total": 45.0,
                "nivel_riesgo_predicho": "Alto",
                "probabilidad_predicha": 98.4,
                "distribucion_probabilidades": {"Bajo": 0.2, "Medio": 1.4, "Alto": 98.4},
                "explicacion_shap": "ALERTA CLINICA: Paciente en nivel de riesgo cardiovascular ALTO. Este nivel de riesgo critico es detonado por valores elevados de: HbA1c (7.6%), PCR-hs (4.8 mg/L) y Colesterol LDL (178 mg/dL).",
                "valores_shap": {"valor_hemoglobina_glucosilada": 0.38, "valor_proteinac_reactiva": 0.32, "valor_colesterol_ldl": 0.26},
                "resultado_real": "Alto"
            }
        }
    ]
    
    try:
        # Primero, asegurémonos de que el doctor existe en public.doctors
        cur.execute("INSERT INTO public.doctors (id, email) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;", (doctor_uuid, "evaluador@cardio.fit"))
        
        for p in patients_data:
            print(f"Registrando paciente: {p['first_name']} {p['last_name']}...")
            
            # 1. Insertar paciente (si ya existe por CURP, obtenemos su ID)
            cur.execute("""
                INSERT INTO public.patients (id, doctor_id, first_name, last_name, curp, fecha_nacimiento, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (curp) DO UPDATE SET 
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name
                RETURNING id;
            """, (p['id'], doctor_uuid, p['first_name'], p['last_name'], p['curp'], p['fecha_nacimiento'], p['activo']))
            p_id = cur.fetchone()[0]
            
            # 2. Insertar evaluación
            ev = p['eval']
            print(f"Registrando evaluacion para paciente {p_id} con riesgo {ev['nivel_riesgo_predicho']}...")
            cur.execute("""
                INSERT INTO public.evaluations (
                    id, patient_id, doctor_id, fecha_evaluacion, sexo, edad, peso, medida_cintura, masa_corporal, tension_arterial,
                    valor_colesterol_ldl, valor_colesterol_total, valor_hemoglobina_glucosilada, valor_proteinac_reactiva,
                    valor_insulina, sueno_horas, actividad_total, nivel_riesgo_predicho, probabilidad_predicha,
                    distribucion_probabilidades, explicacion_shap, valores_shap, resultado_real
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s
                ) ON CONFLICT (id) DO NOTHING;
            """, (
                ev['id'], p_id, doctor_uuid, datetime.utcnow() - timedelta(days=2), ev['sexo'], ev['edad'], ev['peso'], ev['medida_cintura'], ev['masa_corporal'], ev['tension_arterial'],
                ev['valor_colesterol_ldl'], ev['valor_colesterol_total'], ev['valor_hemoglobina_glucosilada'], ev['valor_proteinac_reactiva'],
                ev['valor_insulina'], ev['sueno_horas'], ev['actividad_total'], ev['nivel_riesgo_predicho'], ev['probabilidad_predicha'],
                json.dumps(ev['distribucion_probabilidades']), ev['explicacion_shap'], json.dumps(ev['valores_shap']), ev['resultado_real']
            ))
            
        conn.commit()
        print("¡3 pacientes de prueba y sus evaluaciones fueron insertados con exito!")
    except Exception as e:
        conn.rollback()
        print(f"Error al registrar pacientes de prueba: {str(e)}")
        
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_patients()
