export interface Doctor {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  created_at: string;
}

export interface Patient {
  id: string;
  doctor_id: string;
  first_name: string;
  last_name: string;
  curp?: string;
  fecha_nacimiento: string;
  created_at: string;
}

export interface Evaluation {
  id: string;
  patient_id: string;
  doctor_id: string;
  fecha_evaluacion: string;
  
  // Demográficos y Antropometría
  sexo: 'Hombre' | 'Mujer';
  edad: number;
  peso: number;
  estatura: number;
  medida_cintura: number;
  masa_corporal: number;
  tension_arterial: number;
  
  // Biomarcadores
  resultado_glucosa: number;
  valor_colesterol_ldl: number;
  valor_colesterol_hdl: number;
  valor_colesterol_total: number;
  valor_trigliceridos: number;
  valor_hemoglobina_glucosilada: number;
  valor_proteinac_reactiva: number;
  valor_insulina: number;
  valor_acido_urico: number;
  
  // Estilo de vida
  sueno_horas: number;
  actividad_total: number;
  
  // Salida CDSS
  nivel_riesgo_predicho: 'Bajo' | 'Medio' | 'Alto';
  probabilidad_predicha: number;
  distribucion_probabilidades: {
    Bajo: number;
    Medio: number;
    Alto: number;
  };
  explicacion_shap: string;
  valores_shap: Record<string, number>;
  
  // Gold Standard
  resultado_real?: 'Bajo' | 'Medio' | 'Alto' | null;
}

export interface PredictionResult {
  nivel_riesgo: 'Bajo' | 'Medio' | 'Alto';
  probabilidad_porcentual: number;
  distribucion_probabilidades: {
    Bajo: number;
    Medio: number;
    Alto: number;
  };
  explicacion_clinica: string;
  valores_shap: Record<string, number>;
}
