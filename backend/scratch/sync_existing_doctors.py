import psycopg2

def sync_doctors():
    conn_str = "postgresql://postgres:kVvVVGsFc150i2rt@db.vlftdeynabukgoazxrwd.supabase.co:5432/postgres"
    
    print("Estableciendo conexión SQL con Supabase para sincronizar doctores...")
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        # Insertar usuarios de auth.users en public.doctors que falten
        cur.execute("""
            INSERT INTO public.doctors (id, email, first_name, last_name)
            SELECT 
                id, 
                email, 
                coalesce(raw_user_meta_data->>'first_name', ''), 
                coalesce(raw_user_meta_data->>'last_name', '')
            FROM auth.users
            ON CONFLICT (id) DO NOTHING;
        """)
        
        # Confirmar
        conn.commit()
        
        # Mostrar los doctores actuales
        cur.execute("SELECT id, email, first_name FROM public.doctors;")
        doctors = cur.fetchall()
        print("Doctores en base de datos:")
        for doc in doctors:
            print(f" - ID: {doc[0]}, Email: {doc[1]}, Nombre: {doc[2]}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al sincronizar doctores: {str(e)}")

if __name__ == "__main__":
    sync_doctors()
