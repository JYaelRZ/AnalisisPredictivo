import psycopg2

def confirm_user():
    # Cadena de conexión directa de PostgreSQL
    conn_str = "postgresql://postgres:kVvVVGsFc150i2rt@db.vlftdeynabukgoazxrwd.supabase.co:5432/postgres"
    email = "evaluador@cardio.fit"
    
    print(f"Estableciendo conexión SQL con Supabase...")
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        # Actualizar email_confirmed_at para bypass de email
        print(f"Confirmando correo del usuario '{email}'...")
        cur.execute(
            "UPDATE auth.users SET email_confirmed_at = NOW() WHERE email = %s;", 
            (email,)
        )
        
        # Confirmar los cambios
        conn.commit()
        
        # Verificar cuántos registros fueron afectados
        print(f"¡Hecho! Usuario '{email}' ha sido confirmado en la base de datos y ya puede iniciar sesión en CardioPredict.")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al conectar/actualizar la base de datos: {str(e)}")

if __name__ == "__main__":
    confirm_user()
