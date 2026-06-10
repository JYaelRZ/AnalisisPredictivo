-- Esquema de Base de Datos SQL para Supabase (PostgreSQL)
-- Plataforma CDSS de Predicción de Riesgo Cardiovascular
-- Habilita seguridad a nivel de fila (RLS) para cumplimiento de privacidad médica (LFPDPPP / HIPAA)

-- 1. EXTENSIONES REQUERIDAS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. TABLA DE DOCTORES (MÉDICOS)
CREATE TABLE IF NOT EXISTS public.doctors (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Habilitar RLS en doctores
ALTER TABLE public.doctors ENABLE ROW LEVEL SECURITY;

-- 3. TABLA DE PACIENTES
CREATE TABLE IF NOT EXISTS public.patients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    doctor_id UUID NOT NULL REFERENCES public.doctors(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    curp VARCHAR(18) UNIQUE, -- Identificador único oficial en México (opcional)
    fecha_nacimiento DATE NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Habilitar RLS en pacientes
ALTER TABLE public.patients ENABLE ROW LEVEL SECURITY;

-- 4. TABLA DE EVALUACIONES CLÍNICAS (BIOMARCADORES Y INFERENCIA)
CREATE TABLE IF NOT EXISTS public.evaluations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id UUID NOT NULL REFERENCES public.patients(id) ON DELETE CASCADE,
    doctor_id UUID NOT NULL REFERENCES public.doctors(id) ON DELETE CASCADE,
    fecha_evaluacion TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    
    -- Variables Demográficas y Antropometría
    sexo VARCHAR(10) NOT NULL CHECK (sexo IN ('Hombre', 'Mujer')),
    edad INT NOT NULL CHECK (edad >= 18 AND edad <= 120),
    peso NUMERIC(5,2) NOT NULL CHECK (peso > 30.0 AND peso < 250.0),
    medida_cintura NUMERIC(5,2) NOT NULL CHECK (medida_cintura > 40.0 AND medida_cintura < 200.0),
    masa_corporal NUMERIC(4,2) NOT NULL CHECK (masa_corporal > 10.0 AND masa_corporal < 60.0), -- IMC
    tension_arterial NUMERIC(5,2) NOT NULL CHECK (tension_arterial > 50.0 AND tension_arterial < 250.0), -- Sistólica
    
    -- Biomarcadores Metabólicos e Inflamatorios
    valor_colesterol_ldl NUMERIC(5,2) NOT NULL CHECK (valor_colesterol_ldl > 30.0 AND valor_colesterol_ldl < 300.0),
    valor_colesterol_total NUMERIC(5,2) NOT NULL CHECK (valor_colesterol_total > 50.0 AND valor_colesterol_total < 500.0),
    valor_hemoglobina_glucosilada NUMERIC(4,2) NOT NULL CHECK (valor_hemoglobina_glucosilada > 3.0 AND valor_hemoglobina_glucosilada < 20.0), -- HbA1c
    valor_proteinac_reactiva NUMERIC(5,2) NOT NULL CHECK (valor_proteinac_reactiva > 0.01 AND valor_proteinac_reactiva < 50.0), -- PCR-hs
    valor_insulina NUMERIC(5,2) NOT NULL CHECK (valor_insulina > 0.5 AND valor_insulina < 100.0),
    
    -- Estilo de Vida
    sueno_horas NUMERIC(3,1) NOT NULL CHECK (sueno_horas >= 2.0 AND sueno_horas <= 24.0),
    actividad_total NUMERIC(5,1) NOT NULL CHECK (actividad_total >= 0.0 AND actividad_total <= 1000.0),
    
    -- Resultados de Inferencia CDSS (Model Output)
    nivel_riesgo_predicho VARCHAR(10) NOT NULL CHECK (nivel_riesgo_predicho IN ('Bajo', 'Medio', 'Alto')),
    probabilidad_predicha NUMERIC(5,2) NOT NULL,
    distribucion_probabilidades JSONB NOT NULL, -- { "Bajo": x, "Medio": y, "Alto": z }
    explicacion_shap TEXT NOT NULL,
    valores_shap JSONB NOT NULL,
    
    -- Resultado Clínico Real (Gold Standard para Continuous Learning)
    resultado_real VARCHAR(10) CHECK (resultado_real IN ('Bajo', 'Medio', 'Alto'))
);

-- Habilitar RLS en evaluaciones
ALTER TABLE public.evaluations ENABLE ROW LEVEL SECURITY;


-- 5. POLÍTICAS DE ROW LEVEL SECURITY (RLS)
-- Asegura que todos los médicos autenticados puedan ver, crear o editar expedientes y evaluaciones

-- POLÍTICAS PARA LA TABLA 'doctors'
CREATE POLICY "Doctores pueden leer su propio perfil" 
    ON public.doctors FOR SELECT 
    USING (auth.uid() = id);

CREATE POLICY "Doctores pueden actualizar su propio perfil" 
    ON public.doctors FOR UPDATE 
    USING (auth.uid() = id);

-- POLÍTICAS PARA LA TABLA 'patients'
CREATE POLICY "Doctores pueden ver todos los pacientes" 
    ON public.patients FOR SELECT 
    USING (auth.role() = 'authenticated');

CREATE POLICY "Doctores pueden registrar pacientes" 
    ON public.patients FOR INSERT 
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Doctores pueden actualizar cualquier paciente" 
    ON public.patients FOR UPDATE 
    USING (auth.role() = 'authenticated');

CREATE POLICY "Doctores pueden eliminar cualquier paciente" 
    ON public.patients FOR DELETE 
    USING (auth.role() = 'authenticated');

-- POLÍTICAS PARA LA TABLA 'evaluations'
CREATE POLICY "Doctores pueden ver todas las evaluaciones" 
    ON public.evaluations FOR SELECT 
    USING (auth.role() = 'authenticated');

CREATE POLICY "Doctores pueden registrar evaluaciones" 
    ON public.evaluations FOR INSERT 
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Doctores pueden actualizar cualquier evaluación" 
    ON public.evaluations FOR UPDATE 
    USING (auth.role() = 'authenticated');

CREATE POLICY "Doctores pueden eliminar cualquier evaluación" 
    ON public.evaluations FOR DELETE 
    USING (auth.role() = 'authenticated');



-- 6. TRIGGERS AUTOMÁTICOS PARA NUEVOS DOCTORES
-- Sincroniza auth.users de Supabase Auth automáticamente con la tabla public.doctors
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.doctors (id, email, first_name, last_name)
    VALUES (
        new.id,
        new.email,
        coalesce(new.raw_user_meta_data->>'first_name', ''),
        coalesce(new.raw_user_meta_data->>'last_name', '')
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
