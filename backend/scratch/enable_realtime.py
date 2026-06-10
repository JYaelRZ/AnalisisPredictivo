import psycopg2

def enable_realtime():
    conn_str = "postgresql://postgres:kVvVVGsFc150i2rt@db.vlftdeynabukgoazxrwd.supabase.co:5432/postgres"
    
    print("Estableciendo conexión SQL con Supabase para habilitar tiempo real...")
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        # Habilitar replica identity full para que los payloads de tiempo real tengan todos los datos
        print("Habilitando 'replica identity full' en las tablas...")
        cur.execute("ALTER TABLE public.patients REPLICA IDENTITY FULL;")
        cur.execute("ALTER TABLE public.evaluations REPLICA IDENTITY FULL;")
        
        # Ejecutar bloque PL/pgSQL para crear o agregar a la publicación supabase_realtime
        print("Agregando tablas a la publicación 'supabase_realtime'...")
        cur.execute("""
            DO $$
            BEGIN
                -- Crear la publicación si no existe
                IF NOT EXISTS (SELECT 1 FROM pg_publication WHERE pubname = 'supabase_realtime') THEN
                    CREATE PUBLICATION supabase_realtime;
                END IF;
                
                -- Agregar la tabla patients
                BEGIN
                    ALTER PUBLICATION supabase_realtime ADD TABLE public.patients;
                EXCEPTION
                    WHEN duplicate_object THEN NULL;
                END;
                
                -- Agregar la tabla evaluations
                BEGIN
                    ALTER PUBLICATION supabase_realtime ADD TABLE public.evaluations;
                EXCEPTION
                    WHEN duplicate_object THEN NULL;
                END;
            END $$;
        """)
        
        conn.commit()
        print("¡Tiempo real de Supabase habilitado exitosamente para 'patients' y 'evaluaciones'!")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al habilitar tiempo real: {str(e)}")

if __name__ == "__main__":
    enable_realtime()
