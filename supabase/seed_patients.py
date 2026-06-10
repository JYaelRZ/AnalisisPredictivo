import os
import uuid
import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "..", "backend", ".env")
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: SUPABASE_URL and SUPABASE_KEY must be set in backend/.env")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def seed_data():
    # 1. Fetch doctor evaluador@cardio.fit
    print("Buscando doctor evaluador@cardio.fit...")
    res = supabase.table("doctors").select("*").eq("email", "evaluador@cardio.fit").execute()
    
    if not res.data:
        print("Doctor evaluador@cardio.fit no encontrado en la tabla public.doctors.")
        print("Intentando buscar todos los doctores...")
        all_docs = supabase.table("doctors").select("*").execute()
        if all_docs.data:
            print("Doctores disponibles:")
            for d in all_docs.data:
                print(f"- {d['email']}: {d['id']}")
            # Use the first doctor as fallback
            doctor = all_docs.data[0]
            print(f"Usando fallback: {doctor['email']}")
        else:
            print("No hay doctores en la tabla public.doctors. Asegúrate de registrar uno.")
            return
    else:
        doctor = res.data[0]
        print(f"Doctor encontrado: {doctor['email']} con ID: {doctor['id']}")

    doctor_id = doctor["id"]

    # Definir datos para 3 pacientes de prueba
    patients_to_create = [
        {
            "first_name": "Ana María",
            "last_name": "Gómez (Bajo Riesgo)",
            "curp": "GOMA850214HMCDNR00",
            "fecha_nacimiento": "1985-02-14",
            "activo": True,
            "doctor_id": doctor_id
        },
        {
            "first_name": "Carlos Roberto",
            "last_name": "López (Riesgo Medio)",
            "curp": "LOPC700620HMCDNR01",
            "fecha_nacimiento": "1970-06-20",
            "activo": True,
            "doctor_id": doctor_id
        },
        {
            "first_name": "David Antonio",
            "last_name": "Rodríguez (Alto Riesgo)",
            "curp": "RODA551105HMCDNR02",
            "fecha_nacimiento": "1955-11-05",
            "activo": True,
            "doctor_id": doctor_id
        }
    ]

    for p_info in patients_to_create:
        # Verificar si el paciente ya existe por CURP
        exist_res = supabase.table("patients").select("id").eq("curp", p_info["curp"]).execute()
        if exist_res.data:
            print(f"Paciente {p_info['first_name']} {p_info['last_name']} ya existe. Eliminándolo para recrear...")
            supabase.table("patients").delete().eq("curp", p_info["curp"]).execute()

        # Insertar paciente
        p_res = supabase.table("patients").insert(p_info).execute()
        patient = p_res.data[0]
        p_id = patient["id"]
        print(f"Paciente creado: {patient['first_name']} {patient['last_name']} (ID: {p_id})")

        # Configurar evaluación correspondiente al nivel de riesgo del paciente
        # Bajo Riesgo: Adulto joven (1985 -> 41 años), biomarcadores normales
        if "Bajo" in p_info["last_name"]:
            eval_data = {
                "patient_id": p_id,
                "doctor_id": doctor_id,
                "sexo": "Mujer",
                "edad": 41,
                "peso": 62.0,
                "medida_cintura": 78.0,
                "masa_corporal": 23.5, # normal
                "tension_arterial": 115.0, # normal
                "valor_colesterol_ldl": 85.0, # normal
                "valor_colesterol_total": 170.0, # normal
                "valor_hemoglobina_glucosilada": 5.2, # normal
                "valor_proteinac_reactiva": 0.5, # normal
                "valor_insulina": 6.0,
                "sueno_horas": 7.5,
                "actividad_total": 180.0,
                "nivel_riesgo_predicho": "Bajo",
                "probabilidad_predicha": 94.20,
                "distribucion_probabilidades": {"Bajo": 94.20, "Medio": 4.10, "Alto": 1.70},
                "explicacion_shap": "Homeostasis metabólica general. Todos los biomarcadores se encuentran en rangos de referencia saludables. El estilo de vida (sueño y actividad física) contribuye positivamente.",
                "valores_shap": {
                    "valor_hemoglobina_glucosilada": -0.15,
                    "valor_colesterol_ldl": -0.12,
                    "tension_arterial": -0.10,
                    "masa_corporal": -0.08,
                    "actividad_total": -0.11
                },
                "resultado_real": "Bajo"
            }
        
        # Medio Riesgo: Adulto medio (1970 -> 56 años), sobrepeso, LDL moderado, HbA1c prediabética
        elif "Medio" in p_info["last_name"]:
            eval_data = {
                "patient_id": p_id,
                "doctor_id": doctor_id,
                "sexo": "Hombre",
                "edad": 56,
                "peso": 88.0,
                "medida_cintura": 98.0,
                "masa_corporal": 28.5, # sobrepeso
                "tension_arterial": 128.0, # elevada
                "valor_colesterol_ldl": 125.0, # elevado
                "valor_colesterol_total": 215.0, # elevado
                "valor_hemoglobina_glucosilada": 6.0, # prediabetes
                "valor_proteinac_reactiva": 1.8, # moderado
                "valor_insulina": 14.5,
                "sueno_horas": 6.0,
                "actividad_total": 60.0,
                "nivel_riesgo_predicho": "Medio",
                "probabilidad_predicha": 76.40,
                "distribucion_probabilidades": {"Bajo": 15.20, "Medio": 76.40, "Alto": 8.40},
                "explicacion_shap": "Riesgo cardiovascular moderado/medio. Impulsado por el nivel de hemoglobina glucosilada de 6.0% (prediabetes) y sobrepeso (IMC de 28.5). El colesterol LDL y la presión sistólica limítrofe también incrementan el riesgo.",
                "valores_shap": {
                    "valor_hemoglobina_glucosilada": 0.22,
                    "masa_corporal": 0.15,
                    "valor_colesterol_ldl": 0.12,
                    "tension_arterial": 0.08,
                    "actividad_total": 0.05
                },
                "resultado_real": "Medio"
            }

        # Alto Riesgo: Adulto mayor (1955 -> 71 años), obesidad abdominal, hipertensión, HbA1c alta (diabetes), PCR alta
        else:
            eval_data = {
                "patient_id": p_id,
                "doctor_id": doctor_id,
                "sexo": "Hombre",
                "edad": 71,
                "peso": 96.0,
                "medida_cintura": 112.0, # obesidad abdominal
                "masa_corporal": 32.2, # obesidad
                "tension_arterial": 145.0, # hipertensión
                "valor_colesterol_ldl": 165.0, # alto
                "valor_colesterol_total": 248.0, # alto
                "valor_hemoglobina_glucosilada": 7.2, # diabetes
                "valor_proteinac_reactiva": 4.2, # alto riesgo inflamatorio
                "valor_insulina": 22.0,
                "sueno_horas": 5.0,
                "actividad_total": 20.0,
                "nivel_riesgo_predicho": "Alto",
                "probabilidad_predicha": 89.50,
                "distribucion_probabilidades": {"Bajo": 2.10, "Medio": 8.40, "Alto": 89.50},
                "explicacion_shap": "Alerta de riesgo crítico. Determinado principalmente por edad avanzada (71 años), niveles diabéticos de HbA1c (7.2%), hipertensión sistólica (145 mmHg), dislipidemia y un estado inflamatorio sistémico marcado por la PCR-hs (4.2 mg/L).",
                "valores_shap": {
                    "valor_hemoglobina_glucosilada": 0.38,
                    "tension_arterial": 0.25,
                    "valor_proteinac_reactiva": 0.20,
                    "edad": 0.18,
                    "masa_corporal": 0.12
                },
                "resultado_real": "Alto"
            }

        # Insertar evaluación
        e_res = supabase.table("evaluations").insert(eval_data).execute()
        print(f"Evaluación creada para {p_info['first_name']} con nivel: {eval_data['nivel_riesgo_predicho']}")

    print("\n¡Sembrado de datos finalizado con éxito!")

if __name__ == "__main__":
    seed_data()
