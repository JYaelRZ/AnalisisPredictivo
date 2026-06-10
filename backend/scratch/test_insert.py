import psycopg2
import uuid

def test_rls():
    conn_str = "postgresql://postgres:kVvVVGsFc150i2rt@db.vlftdeynabukgoazxrwd.supabase.co:5432/postgres"
    doctor_uuid = "70af24be-6be4-4e7d-ac3f-d4399be0ff0d" # evaluador@cardio.fit UUID
    
    print("Conectando a la base de datos...")
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    
    try:
        # Emular RLS para el rol 'authenticated' y el doctor_id específico
        print(f"Configurando variables de sesion para emular RLS como el usuario {doctor_uuid}...")
        cur.execute("BEGIN;")
        cur.execute(f"SET LOCAL request.jwt.claims = '{{\"sub\": \"{doctor_uuid}\", \"role\": \"authenticated\"}}';")
        
        # Intentar insertar un paciente de prueba
        test_patient_id = str(uuid.uuid4())
        print(f"Intentando insertar paciente de prueba con ID: {test_patient_id}...")
        cur.execute("""
            INSERT INTO public.patients (id, doctor_id, first_name, last_name, curp, fecha_nacimiento, activo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (test_patient_id, doctor_uuid, "Test", "RLS", "TEST900101HDFRNS01", "1990-01-01", True))
        
        patient_id = cur.fetchone()[0]
        print(f"Patient inserted successfully. ID: {patient_id}")
        
        # Intentar seleccionar pacientes
        print("Intentando seleccionar pacientes...")
        cur.execute("SELECT id, first_name, last_name FROM public.patients;")
        patients = cur.fetchall()
        print(f"Selection successful. Patients visible: {len(patients)}")
        for p in patients:
            print(f"  - {p[0]}: {p[1]} {p[2]}")
            
        # Intentar insertar evaluación de prueba
        test_eval_id = str(uuid.uuid4())
        print(f"Intentando insertar evaluacion de prueba con ID: {test_eval_id}...")
        cur.execute("""
            INSERT INTO public.evaluations (
                id, patient_id, doctor_id, sexo, edad, peso, medida_cintura, masa_corporal, tension_arterial,
                valor_colesterol_ldl, valor_colesterol_total, valor_hemoglobina_glucosilada, valor_proteinac_reactiva,
                valor_insulina, sueno_horas, actividad_total, nivel_riesgo_predicho, probabilidad_predicha,
                distribucion_probabilidades, explicacion_shap, valores_shap
            ) VALUES (
                %s, %s, %s, 'Hombre', 35, 75.0, 85.0, 24.5, 120.0,
                90.0, 180.0, 5.2, 0.5,
                10.0, 7.5, 150.0, 'Bajo', 95.0,
                '{"Bajo": 95, "Medio": 4, "Alto": 1}'::jsonb, 'Explicacion de prueba', '{"edad": 0.1}'::jsonb
            ) RETURNING id;
        """, (test_eval_id, test_patient_id, doctor_uuid))
        
        eval_id = cur.fetchone()[0]
        print(f"Evaluation inserted successfully. ID: {eval_id}")
        
        # Deshacer los cambios de prueba
        cur.execute("ROLLBACK;")
        print("Test RLS completed without errors. Rollback successful.")
        
    except Exception as e:
        print(f"Error during RLS test: {str(e)}")
        try:
            cur.execute("ROLLBACK;")
        except:
            pass
            
    cur.close()
    conn.close()

if __name__ == "__main__":
    test_rls()
