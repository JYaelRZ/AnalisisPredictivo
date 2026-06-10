import psycopg2
import uuid
import json
from datetime import datetime, timedelta

def create_more_patients():
    conn_str = "postgresql://postgres:kVvVVGsFc150i2rt@db.vlftdeynabukgoazxrwd.supabase.co:5432/postgres"
    doctor_uuid = "70af24be-6be4-4e7d-ac3f-d4399be0ff0d" # evaluador@cardio.fit UUID
    
    print("Conectando a la base de datos Supabase...")
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    
    patients_data = [
        {
            "id": str(uuid.uuid4()),
            "first_name": "Sofía Isabel",
            "last_name": "Mendoza (Bajo)",
            "curp": "MENS890715HDFRNS04",
            "fecha_nacimiento": "1989-07-15",
            "activo": True,
            "eval": {
                "id": str(uuid.uuid4()),
                "sexo": "Mujer",
                "edad": 37,
                "peso": 58.5,
                "medida_cintura": 74.0,
                "masa_corporal": 21.5,
                "tension_arterial": 110.0,
                "valor_colesterol_ldl": 75.0,
                "valor_colesterol_total": 160.0,
                "valor_hemoglobina_glucosilada": 4.9,
                "valor_proteinac_reactiva": 0.3,
                "valor_insulina": 5.5,
                "sueno_horas": 8.0,
                "actividad_total": 240.0,
                "nivel_riesgo_predicho": "Bajo",
                "probabilidad_predicha": 97.5,
                "distribucion_probabilidades": {"Bajo": 97.5, "Medio": 2.0, "Alto": 0.5},
                "explicacion_shap": "Paciente femenina con perfil óptimo. Biomarcadores dentro de rangos normales e ideal estilo de vida con 240 minutos semanales de actividad física y 8 horas de sueño.",
                "valores_shap": {"valor_hemoglobina_glucosilada": -0.35, "valor_proteinac_reactiva": -0.30, "valor_colesterol_ldl": -0.20},
                "resultado_real": "Bajo"
            }
        },
        {
            "id": str(uuid.uuid4()),
            "first_name": "Mateo Alejandro",
            "last_name": "Herrera (Medio)",
            "curp": "HERM760412HDFRNS06",
            "fecha_nacimiento": "1976-04-12",
            "activo": True,
            "eval": {
                "id": str(uuid.uuid4()),
                "sexo": "Hombre",
                "edad": 50,
                "peso": 86.0,
                "medida_cintura": 96.0,
                "masa_corporal": 27.8,
                "tension_arterial": 132.0,
                "valor_colesterol_ldl": 135.0,
                "valor_colesterol_total": 224.0,
                "valor_hemoglobina_glucosilada": 5.9,
                "valor_proteinac_reactiva": 2.1,
                "valor_insulina": 13.0,
                "sueno_horas": 6.5,
                "actividad_total": 75.0,
                "nivel_riesgo_predicho": "Medio",
                "probabilidad_predicha": 79.2,
                "distribucion_probabilidades": {"Bajo": 12.3, "Medio": 79.2, "Alto": 8.5},
                "explicacion_shap": "Riesgo cardiovascular intermedio. El paciente presenta sobrepeso (IMC de 27.8), prehipertensión (sistólica de 132 mmHg) y colesterol LDL elevado (135 mg/dL), lo que justifica el nivel predictivo de riesgo Medio.",
                "valores_shap": {"valor_colesterol_ldl": 0.22, "valor_hemoglobina_glucosilada": 0.15, "tension_arterial": 0.10},
                "resultado_real": "Medio"
            }
        },
        {
            "id": str(uuid.uuid4()),
            "first_name": "Elena Victoria",
            "last_name": "Martínez (Alto)",
            "curp": "MARE520822HDFRNS03",
            "fecha_nacimiento": "1952-08-22",
            "activo": True,
            "eval": {
                "id": str(uuid.uuid4()),
                "sexo": "Mujer",
                "edad": 73,
                "peso": 89.0,
                "medida_cintura": 102.0,
                "masa_corporal": 31.2,
                "tension_arterial": 152.0,
                "valor_colesterol_ldl": 182.0,
                "valor_colesterol_total": 285.0,
                "valor_hemoglobina_glucosilada": 7.8,
                "valor_proteinac_reactiva": 5.2,
                "valor_insulina": 28.0,
                "sueno_horas": 4.5,
                "actividad_total": 15.0,
                "nivel_riesgo_predicho": "Alto",
                "probabilidad_predicha": 98.9,
                "distribucion_probabilidades": {"Bajo": 0.1, "Medio": 1.0, "Alto": 98.9},
                "explicacion_shap": "ALERTA DE RIESGO SEVERO. Paciente de edad avanzada con obesidad clínica (IMC 31.2), hipertensión descontrolada (152 mmHg), diabetes descompensada (HbA1c 7.8%) y dislipidemia severa.",
                "valores_shap": {"valor_hemoglobina_glucosilada": 0.42, "tension_arterial": 0.35, "valor_proteinac_reactiva": 0.28, "edad": 0.22},
                "resultado_real": "Alto"
            }
        }
    ]
    
    try:
        # Asegurarnos de que el doctor existe
        cur.execute("INSERT INTO public.doctors (id, email) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;", (doctor_uuid, "evaluador@cardio.fit"))
        
        for p in patients_data:
            print(f"Registrando paciente: {p['first_name']} {p['last_name']}...")
            
            # 1. Insertar paciente
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
            print(f"Registrando evaluación para paciente {p_id} con riesgo {ev['nivel_riesgo_predicho']}...")
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
                ev['id'], p_id, doctor_uuid, datetime.utcnow(), ev['sexo'], ev['edad'], ev['peso'], ev['medida_cintura'], ev['masa_corporal'], ev['tension_arterial'],
                ev['valor_colesterol_ldl'], ev['valor_colesterol_total'], ev['valor_hemoglobina_glucosilada'], ev['valor_proteinac_reactiva'],
                ev['valor_insulina'], ev['sueno_horas'], ev['actividad_total'], ev['nivel_riesgo_predicho'], ev['probabilidad_predicha'],
                json.dumps(ev['distribucion_probabilidades']), ev['explicacion_shap'], json.dumps(ev['valores_shap']), ev['resultado_real']
            ))
            
        conn.commit()
        print("¡Los 3 pacientes adicionales de prueba y sus evaluaciones correspondientes se insertaron con éxito!")
    except Exception as e:
        conn.rollback()
        print(f"Error al registrar pacientes de prueba: {str(e)}")
        
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_more_patients()
