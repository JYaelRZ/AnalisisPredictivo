import psycopg2

def list_tables():
    conn_str = "postgresql://postgres:kVvVVGsFc150i2rt@db.vlftdeynabukgoazxrwd.supabase.co:5432/postgres"
    conn = psycopg2.connect(conn_str)
    cur = conn.cursor()
    
    cur.execute("""
        SELECT schemaname, tablename 
        FROM pg_catalog.pg_tables 
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
    """)
    tables = cur.fetchall()
    print("Tablas encontradas:")
    for t in tables:
        print(f" - {t[0]}.{t[1]}")
        
    cur.close()
    conn.close()

if __name__ == "__main__":
    list_tables()
