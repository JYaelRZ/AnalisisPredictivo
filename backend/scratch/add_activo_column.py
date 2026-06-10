import psycopg2

def add_column():
    conn_str = "postgresql://postgres:kVvVVGsFc150i2rt@db.vlftdeynabukgoazxrwd.supabase.co:5432/postgres"
    print("Estableciendo conexión SQL con Supabase...")
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        # Alterar la tabla para agregar la columna 'activo'
        print("Agregando la columna 'activo' a la tabla 'patients'...")
        cur.execute("ALTER TABLE public.patients ADD COLUMN IF NOT EXISTS activo BOOLEAN NOT NULL DEFAULT TRUE;")
        
        conn.commit()
        print("¡Columna 'activo' agregada exitosamente!")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al agregar columna: {str(e)}")

if __name__ == "__main__":
    add_column()
