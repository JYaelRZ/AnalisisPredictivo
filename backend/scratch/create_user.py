import os
from supabase import create_client

def create_user():
    url = "https://vlftdeynabukgoazxrwd.supabase.co"
    # Para crear un usuario confirmado directamente, usaremos la anon key para el registro.
    # Si la confirmación de correo está activa, el usuario quedará pendiente de confirmación.
    # Intentamos registrar el usuario de pruebas.
    key = "sb_publishable_m7UZPvFLnvtzA8C0pKKC6Q_1EOOQmVM"
    
    email = "evaluador@cardio.fit"
    password = "clinicalcdss2026"
    
    print(f"Intentando registrar al usuario {email}...")
    
    try:
        supabase = create_client(url, key)
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        print("Registro completado con éxito.")
        print(response)
    except Exception as e:
        print(f"Error al registrar: {str(e)}")

if __name__ == "__main__":
    create_user()
