import psycopg2
import os

def deploy_schema():
    conn_str = "postgresql://postgres:kVvVVGsFc150i2rt@db.vlftdeynabukgoazxrwd.supabase.co:5432/postgres"
    schema_path = "../supabase/schema.sql"
    
    print(f"Leyendo el archivo schema.sql en {schema_path}...")
    if not os.path.exists(schema_path):
        # Intentar ruta alternativa
        schema_path = "supabase/schema.sql"
        if not os.path.exists(schema_path):
            schema_path = "c:/Users/YaelR/OneDrive/Documents/Tesis - Web/supabase/schema.sql"
            
    with open(schema_path, 'r', encoding='utf-8') as f:
        sql = f.read()
        
    print("Estableciendo conexión SQL con Supabase para desplegar las tablas...")
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        # Ejecutar el script SQL
        cur.execute(sql)
        conn.commit()
        
        print("¡Esquema de Base de Datos desplegado exitosamente en Supabase!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al desplegar el esquema: {str(e)}")

if __name__ == "__main__":
    deploy_schema()
