import psycopg2

def update_policies():
    conn_str = "postgresql://postgres:kVvVVGsFc150i2rt@db.vlftdeynabukgoazxrwd.supabase.co:5432/postgres"
    
    print("Estableciendo conexión SQL con Supabase...")
    try:
        conn = psycopg2.connect(conn_str)
        cur = conn.cursor()
        
        # 1. Drop existing policies for patients
        print("Eliminando políticas antiguas de 'patients'...")
        cur.execute("DROP POLICY IF EXISTS \"Doctores pueden ver sus propios pacientes\" ON public.patients;")
        cur.execute("DROP POLICY IF EXISTS \"Doctores pueden registrar pacientes\" ON public.patients;")
        cur.execute("DROP POLICY IF EXISTS \"Doctores pueden actualizar sus pacientes\" ON public.patients;")
        cur.execute("DROP POLICY IF EXISTS \"Doctores pueden eliminar sus pacientes\" ON public.patients;")
        
        # 2. Create new collaborative policies for patients
        print("Creando nuevas políticas colaborativas para 'patients'...")
        cur.execute("""
            CREATE POLICY "Doctores pueden ver todos los pacientes" 
                ON public.patients FOR SELECT 
                USING (auth.role() = 'authenticated');
        """)
        cur.execute("""
            CREATE POLICY "Doctores pueden registrar pacientes" 
                ON public.patients FOR INSERT 
                WITH CHECK (auth.role() = 'authenticated');
        """)
        cur.execute("""
            CREATE POLICY "Doctores pueden actualizar cualquier paciente" 
                ON public.patients FOR UPDATE 
                USING (auth.role() = 'authenticated');
        """)
        cur.execute("""
            CREATE POLICY "Doctores pueden eliminar cualquier paciente" 
                ON public.patients FOR DELETE 
                USING (auth.role() = 'authenticated');
        """)
        
        # 3. Drop existing policies for evaluations
        print("Eliminando políticas antiguas de 'evaluations'...")
        cur.execute("DROP POLICY IF EXISTS \"Doctores pueden ver evaluaciones de sus pacientes\" ON public.evaluations;")
        cur.execute("DROP POLICY IF EXISTS \"Doctores pueden crear evaluaciones para sus pacientes\" ON public.evaluations;")
        cur.execute("DROP POLICY IF EXISTS \"Doctores pueden actualizar sus evaluaciones\" ON public.evaluations;")
        cur.execute("DROP POLICY IF EXISTS \"Doctores pueden eliminar sus evaluaciones\" ON public.evaluations;")
        
        # 4. Create new collaborative policies for evaluations
        print("Creando nuevas políticas colaborativas para 'evaluations'...")
        cur.execute("""
            CREATE POLICY "Doctores pueden ver todas las evaluaciones" 
                ON public.evaluations FOR SELECT 
                USING (auth.role() = 'authenticated');
        """)
        cur.execute("""
            CREATE POLICY "Doctores pueden registrar evaluaciones" 
                ON public.evaluations FOR INSERT 
                WITH CHECK (auth.role() = 'authenticated');
        """)
        cur.execute("""
            CREATE POLICY "Doctores pueden actualizar cualquier evaluación" 
                ON public.evaluations FOR UPDATE 
                USING (auth.role() = 'authenticated');
        """)
        cur.execute("""
            CREATE POLICY "Doctores pueden eliminar cualquier evaluación" 
                ON public.evaluations FOR DELETE 
                USING (auth.role() = 'authenticated');
        """)
        
        conn.commit()
        print("¡Políticas actualizadas exitosamente en la base de datos Supabase!")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al actualizar las políticas: {str(e)}")

if __name__ == "__main__":
    update_policies()
