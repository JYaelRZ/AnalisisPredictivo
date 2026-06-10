'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { supabase } from '@/lib/supabase';
import { 
  Heart, Users, ClipboardList, LogOut, Search, Plus, UserPlus, 
  TrendingUp, Activity, ShieldAlert, Sparkles, ChevronRight,
  UserCheck, UserMinus, Trash2, HelpCircle, AlertTriangle
} from 'lucide-react';
import { Patient, Evaluation } from '@/types';

// Datos de pacientes simulados iniciales (ENSANUT) por si localStorage está vacío
const INITIAL_PATIENTS: Patient[] = [
  { id: 'pat-1', doctor_id: 'doc-1', first_name: 'Alejandro', last_name: 'Mendoza Ruiz', curp: 'MERA780412HDFNRS0', fecha_nacimiento: '1978-04-12', created_at: '2026-05-10' },
  { id: 'pat-2', doctor_id: 'doc-1', first_name: 'Guadalupe', last_name: 'Hernández Gómez', curp: 'HEGG821105MDFNRS1', fecha_nacimiento: '1982-11-05', created_at: '2026-05-15' },
  { id: 'pat-3', doctor_id: 'doc-1', first_name: 'Roberto', last_name: 'Flores Silva', curp: 'FISR540920HDFNRS8', fecha_nacimiento: '1954-09-20', created_at: '2026-05-20' },
  { id: 'pat-4', doctor_id: 'doc-1', first_name: 'Silvia', last_name: 'López Domínguez', curp: 'LODS650715MDFNRS5', fecha_nacimiento: '1965-07-15', created_at: '2026-05-22' }
];

const INITIAL_EVALUATIONS: Evaluation[] = [
  {
    id: 'eval-1', patient_id: 'pat-3', doctor_id: 'doc-1', fecha_evaluacion: '2026-05-20T10:30:00Z',
    sexo: 'Hombre', edad: 71, peso: 88.5, estatura: 168.0, medida_cintura: 106.0, masa_corporal: 31.2, tension_arterial: 148.0,
    resultado_glucosa: 132.0, valor_colesterol_ldl: 168.0, valor_colesterol_hdl: 32.0, valor_colesterol_total: 245.0, valor_trigliceridos: 220.0,
    valor_hemoglobina_glucosilada: 7.4, valor_proteinac_reactiva: 4.2, valor_insulina: 24.5, valor_acido_urico: 7.8,
    sueno_horas: 5.5, actividad_total: 45.0, nivel_riesgo_predicho: 'Alto', probabilidad_predicha: 98.48,
    distribucion_probabilidades: { Bajo: 0.1, Medio: 1.42, Alto: 98.48 },
    explicacion_shap: '⚠️ ALERTA CLÍNICA: Paciente en nivel de riesgo cardiovascular ALTO. Este nivel de riesgo crítico es detonado de forma combinada por valores elevados o descontrolados de: Hemoglobina Glucosilada (HbA1c %) (7.4%), Proteína C Reactiva (PCR-hs mg/L) (4.2 mg/L), Colesterol LDL (168.0 mg/dL).',
    valores_shap: { valor_hemoglobina_glucosilada: 0.35, valor_proteinac_reactiva: 0.28, valor_colesterol_ldl: 0.22, edad: 0.1 },
    resultado_real: null
  },
  {
    id: 'eval-2', patient_id: 'pat-1', doctor_id: 'doc-1', fecha_evaluacion: '2026-05-10T12:00:00Z',
    sexo: 'Hombre', edad: 48, peso: 76.0, estatura: 172.0, medida_cintura: 89.0, masa_corporal: 25.3, tension_arterial: 124.0,
    resultado_glucosa: 88.0, valor_colesterol_ldl: 112.0, valor_colesterol_hdl: 46.0, valor_colesterol_total: 185.0, valor_trigliceridos: 130.0,
    valor_hemoglobina_glucosilada: 5.2, valor_proteinac_reactiva: 0.8, valor_insulina: 9.8, valor_acido_urico: 5.1,
    sueno_horas: 7.0, actividad_total: 180.0, nivel_riesgo_predicho: 'Bajo', probabilidad_predicha: 95.20,
    distribucion_probabilidades: { Bajo: 95.20, Medio: 4.3, Alto: 0.5 },
    explicacion_shap: 'El paciente muestra homeostasis metabólica y cardiovascular general. Esto es impulsado principalmente por valores estables en: Hemoglobina Glucosilada (5.2%) y Proteína C Reactiva (0.8 mg/L).',
    valores_shap: { valor_hemoglobina_glucosilada: -0.28, valor_proteinac_reactiva: -0.24, actividad_total: -0.15 },
    resultado_real: null
  },
  {
    id: 'eval-3', patient_id: 'pat-2', doctor_id: 'doc-1', fecha_evaluacion: '2026-05-15T09:15:00Z',
    sexo: 'Mujer', edad: 43, peso: 82.0, estatura: 166.0, medida_cintura: 96.0, masa_corporal: 29.8, tension_arterial: 132.0,
    resultado_glucosa: 104.0, valor_colesterol_ldl: 128.0, valor_colesterol_hdl: 42.0, valor_colesterol_total: 210.0, valor_trigliceridos: 165.0,
    valor_hemoglobina_glucosilada: 6.0, valor_proteinac_reactiva: 2.1, valor_insulina: 16.0, valor_acido_urico: 5.4,
    sueno_horas: 6.0, actividad_total: 90.0, nivel_riesgo_predicho: 'Medio', probabilidad_predicha: 82.40,
    distribucion_probabilidades: { Bajo: 8.20, Medio: 82.40, Alto: 9.40 },
    explicacion_shap: 'El paciente presenta un nivel de riesgo cardiovascular MEDIO. Este riesgo está impulsado principalmente por anomalías moderadas en: Colesterol LDL (128.0 mg/dL) y Hemoglobina Glucosilada (6.0%).',
    valores_shap: { valor_colesterol_ldl: 0.18, valor_hemoglobina_glucosilada: 0.15, medida_cintura: 0.08 },
    resultado_real: null
  }
];

export default function DashboardPage() {
  const router = useRouter();
  const [doctorEmail, setDoctorEmail] = useState('');
  const [patients, setPatients] = useState<Patient[]>([]);
  const [evaluations, setEvaluations] = useState<Evaluation[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [showAddPatient, setShowAddPatient] = useState(false);
  
  const [showSuspended, setShowSuspended] = useState(false);
  const [confirmDeletePatient, setConfirmDeletePatient] = useState<Patient | null>(null);
  
  // Formulario nuevo paciente
  const [newFirstName, setNewFirstName] = useState('');
  const [newLastName, setNewLastName] = useState('');
  const [newCurp, setNewCurp] = useState('');
  const [newDob, setNewDob] = useState('');

  useEffect(() => {
    // Validar sesión
    const email = localStorage.getItem('cdss_doctor_email');
    if (!email) {
      router.push('/login');
      return;
    }
    setDoctorEmail(email);

    // Cargar datos de localStorage o inicializar por defecto
    const savedPatients = localStorage.getItem('cdss_patients');
    const savedEvaluations = localStorage.getItem('cdss_evaluations');

    let localPats: Patient[] = savedPatients ? JSON.parse(savedPatients) : INITIAL_PATIENTS;
    let localEvals: Evaluation[] = savedEvaluations ? JSON.parse(savedEvaluations) : INITIAL_EVALUATIONS;

    setPatients(localPats);
    setEvaluations(localEvals);

    if (!savedPatients) {
      localStorage.setItem('cdss_patients', JSON.stringify(INITIAL_PATIENTS));
    }
    if (!savedEvaluations) {
      localStorage.setItem('cdss_evaluations', JSON.stringify(INITIAL_EVALUATIONS));
    }

    // Sincronización desde Supabase si la sesión no es simulada
    const isSimulated = localStorage.getItem('cdss_simulated_session') === 'true';
    let cleanupRealtime: (() => void) | undefined;

    if (!isSimulated) {
      const syncSupabase = async () => {
        try {
          // 1. Obtener pacientes
          const { data: dbPatients, error: patError } = await supabase
            .from('patients')
            .select('*');
          
          if (patError) throw patError;
          
          if (dbPatients) {
            setPatients(dbPatients);
            localStorage.setItem('cdss_patients', JSON.stringify(dbPatients));
          }

          // 2. Obtener evaluaciones
          const { data: dbEvals, error: evalError } = await supabase
            .from('evaluations')
            .select('*');
          
          if (evalError) throw evalError;
          
          if (dbEvals) {
            const mappedEvals: Evaluation[] = dbEvals.map(e => ({
              id: e.id,
              patient_id: e.patient_id,
              doctor_id: e.doctor_id,
              fecha_evaluacion: e.fecha_evaluacion,
              sexo: e.sexo,
              edad: e.edad,
              peso: e.peso,
              estatura: e.estatura || 165.0,
              medida_cintura: e.medida_cintura,
              masa_corporal: e.masa_corporal,
              tension_arterial: e.tension_arterial,
              resultado_glucosa: e.resultado_glucosa || 95.0,
              valor_colesterol_ldl: e.valor_colesterol_ldl,
              valor_colesterol_hdl: e.valor_colesterol_hdl || 45.0,
              valor_colesterol_total: e.valor_colesterol_total,
              valor_trigliceridos: e.valor_trigliceridos || 150.0,
              valor_hemoglobina_glucosilada: e.valor_hemoglobina_glucosilada,
              valor_proteinac_reactiva: e.valor_proteinac_reactiva,
              valor_insulina: e.valor_insulina,
              valor_acido_urico: e.valor_acido_urico || 5.0,
              sueno_horas: e.sueno_horas,
              actividad_total: e.actividad_total,
              nivel_riesgo_predicho: e.nivel_riesgo_predicho,
              probabilidad_predicha: e.probabilidad_predicha,
              distribucion_probabilidades: e.distribucion_probabilidades,
              explicacion_shap: e.explicacion_shap,
              valores_shap: e.valores_shap,
              resultado_real: e.resultado_real
            }));
            
            // Combinar evitando duplicados
            const combinedEvalsMap = new Map<string, Evaluation>();
            localEvals.forEach(ev => combinedEvalsMap.set(ev.id, ev));
            mappedEvals.forEach(ev => combinedEvalsMap.set(ev.id, ev));
            
            const sortedCombined = Array.from(combinedEvalsMap.values()).sort(
              (a, b) => new Date(b.fecha_evaluacion).getTime() - new Date(a.fecha_evaluacion).getTime()
            );
            
            setEvaluations(sortedCombined);
            localStorage.setItem('cdss_evaluations', JSON.stringify(sortedCombined));
          }
        } catch (err) {
          console.warn("No se pudo conectar a Supabase, usando datos locales:", err);
        }
      };
      
      syncSupabase();

      // Configurar suscripción en tiempo real
      const channel = supabase
        .channel('schema-db-changes')
        .on(
          'postgres_changes',
          { event: '*', schema: 'public', table: 'patients' },
          () => {
            console.log("Cambio en tabla 'patients' detectado en tiempo real.");
            syncSupabase();
          }
        )
        .on(
          'postgres_changes',
          { event: '*', schema: 'public', table: 'evaluations' },
          () => {
            console.log("Cambio en tabla 'evaluations' detectado en tiempo real.");
            syncSupabase();
          }
        )
        .subscribe();

      cleanupRealtime = () => {
        supabase.removeChannel(channel);
      };
    }

    return () => {
      if (cleanupRealtime) cleanupRealtime();
    };
  }, [router]);

  const handleLogout = async () => {
    await supabase.auth.signOut();
    localStorage.removeItem('cdss_doctor_email');
    localStorage.removeItem('cdss_simulated_session');
    router.push('/login');
  };

  const handleAddPatientSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFirstName || !newLastName || !newDob) return;

    const doctorId = localStorage.getItem('cdss_doctor_id') || 'doc-1';
    const patientId = typeof window !== 'undefined' && window.crypto && window.crypto.randomUUID
      ? window.crypto.randomUUID()
      : `pat-${Date.now()}`;

    const newPatient: Patient = {
      id: patientId,
      doctor_id: doctorId,
      first_name: newFirstName,
      last_name: newLastName,
      curp: newCurp.toUpperCase() || undefined,
      fecha_nacimiento: newDob,
      activo: true,
      created_at: new Date().toISOString().split('T')[0]
    };

    const updatedPatients = [newPatient, ...patients];
    setPatients(updatedPatients);
    localStorage.setItem('cdss_patients', JSON.stringify(updatedPatients));

    // Guardar en Supabase si la sesión no es simulada
    const isSimulated = localStorage.getItem('cdss_simulated_session') === 'true';
    if (!isSimulated) {
      try {
        const { error } = await supabase.from('patients').insert([{
          id: patientId,
          doctor_id: doctorId,
          first_name: newFirstName,
          last_name: newLastName,
          curp: newCurp.toUpperCase() || null,
          fecha_nacimiento: newDob,
          activo: true
        }]);

        if (error) {
          console.error("Error al registrar paciente en Supabase:", error.message);
        } else {
          console.log("Paciente registrado exitosamente en Supabase:", patientId);
        }
      } catch (err) {
        console.error("Error de conexión con Supabase:", err);
      }
    }

    // Resetear formulario
    setNewFirstName('');
    setNewLastName('');
    setNewCurp('');
    setNewDob('');
    setShowAddPatient(false);
  };

  // Cambiar el estado activo/suspendido de un paciente
  const handleToggleActive = async (patient: Patient) => {
    const nextActive = patient.activo === false ? true : false;
    
    // 1. Actualizar estado local y localStorage
    const updatedPatients = patients.map(p => {
      if (p.id === patient.id) {
        return { ...p, activo: nextActive };
      }
      return p;
    });
    setPatients(updatedPatients);
    localStorage.setItem('cdss_patients', JSON.stringify(updatedPatients));
    
    // 2. Persistir en Supabase
    const isSimulated = localStorage.getItem('cdss_simulated_session') === 'true';
    if (!isSimulated) {
      try {
        const { error } = await supabase
          .from('patients')
          .update({ activo: nextActive })
          .eq('id', patient.id);
        
        if (error) {
          console.error("Error al suspender/reactivar paciente en Supabase:", error.message);
        }
      } catch (err) {
        console.error("Error de conexión con Supabase:", err);
      }
    }
  };

  // Confirmar y eliminar físicamente al paciente de Supabase
  const handleDeletePatientConfirm = async () => {
    if (!confirmDeletePatient) return;
    const patientId = confirmDeletePatient.id;

    // 1. Actualizar estado local y localStorage de pacientes
    const updatedPatients = patients.filter(p => p.id !== patientId);
    setPatients(updatedPatients);
    localStorage.setItem('cdss_patients', JSON.stringify(updatedPatients));

    // Borrar evaluaciones del paciente en localStorage
    const savedEvaluations = localStorage.getItem('cdss_evaluations');
    if (savedEvaluations) {
      const parsed: Evaluation[] = JSON.parse(savedEvaluations);
      const filteredEvaluations = parsed.filter(e => e.patient_id !== patientId);
      setEvaluations(filteredEvaluations);
      localStorage.setItem('cdss_evaluations', JSON.stringify(filteredEvaluations));
    }

    // 2. Borrar en Supabase
    const isSimulated = localStorage.getItem('cdss_simulated_session') === 'true';
    if (!isSimulated) {
      try {
        const { error } = await supabase
          .from('patients')
          .delete()
          .eq('id', patientId);

        if (error) {
          console.error("Error al eliminar paciente de Supabase:", error.message);
        } else {
          console.log("Paciente eliminado con éxito de Supabase.");
        }
      } catch (err) {
        console.error("Error de conexión con Supabase:", err);
      }
    }

    setConfirmDeletePatient(null);
  };

  // Exportar todas las evaluaciones clínicas para entrenamiento continuo
  const handleExportTrainingData = () => {
    const features = [
      "sexo", "edad", "peso", "estatura", "medida_cintura", "masa_corporal", 
      "tension_arterial", "resultado_glucosa", "valor_colesterol_ldl", 
      "valor_colesterol_hdl", "valor_colesterol_total", "valor_trigliceridos",
      "valor_hemoglobina_glucosilada", "valor_proteinac_reactiva", 
      "valor_insulina", "valor_acido_urico", "sueno_horas", "actividad_total"
    ];
    
    // Header compatible con el preprocesamiento
    const csvHeader = [...features, "riesgo_cvd_3_niveles"].join(",") + "\n";
    
    // Generar renglones
    const csvRows = evaluations.map(e => {
      const rowValues = features.map(feat => {
        let val = e[feat as keyof Evaluation];
        return val !== undefined && val !== null ? val : "";
      });
      
      // La confirmación real del médico tiene prioridad para el entrenamiento continuo
      const targetLabel = e.resultado_real || e.nivel_riesgo_predicho;
      rowValues.push(targetLabel);
      
      return rowValues.join(",");
    }).join("\n");
    
    const blob = new Blob([csvHeader + csvRows], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `expedientes_entrenamiento_cdss_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Filtrar pacientes
  const filteredPatients = patients.filter(patient => {
    // Ocultar pacientes inactivos/suspendidos si no está habilitado el toggle
    if (!showSuspended && patient.activo === false) return false;

    const fullName = `${patient.first_name} ${patient.last_name}`.toLowerCase();
    const curp = (patient.curp || '').toLowerCase();
    return fullName.includes(searchQuery.toLowerCase()) || curp.includes(searchQuery.toLowerCase());
  });

  // Obtener última evaluación del paciente
  const getLatestEval = (patientId: string): Evaluation | undefined => {
    return evaluations
      .filter(e => e.patient_id === patientId)
      .sort((a, b) => new Date(b.fecha_evaluacion).getTime() - new Date(a.fecha_evaluacion).getTime())[0];
  };

  // Estadísticas globales
  const totalEvaluationsCount = evaluations.length;
  const highRiskCount = evaluations.filter(e => e.nivel_riesgo_predicho === 'Alto').length;

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      
      {/* Navbar Premium */}
      <header className="bg-white border-b border-slate-100 py-4 px-6 md:px-12 flex justify-between items-center shadow-sm z-10 glass-panel sticky top-0">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-slate-900 rounded-xl text-white">
            <Heart className="w-5 h-5 text-rose-500 fill-current animate-pulse-soft" />
          </div>
          <div>
            <span className="font-bold text-slate-900 text-lg block leading-none">CardioPredict</span>
            <span className="text-xs text-slate-400 font-medium tracking-wide uppercase">Apoyo Clínico CDSS</span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="hidden sm:block text-right">
            <span className="text-xs text-slate-400 block font-medium">Médico Activo</span>
            <span className="text-sm font-semibold text-slate-800">{doctorEmail}</span>
          </div>
          
          <button 
            onClick={handleLogout}
            className="p-2.5 text-slate-500 hover:text-rose-600 hover:bg-rose-50 rounded-xl transition cursor-pointer"
            title="Cerrar sesión médica"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </header>

      {/* Contenido Principal */}
      <main className="flex-1 max-w-[1400px] w-full mx-auto p-4 md:p-8 space-y-8">
        
        {/* Banner de Bienvenida y Estadísticas */}
        <section className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="md:col-span-2 bg-gradient-to-r from-slate-900 via-slate-950 to-blue-950 text-white rounded-2xl p-6 flex flex-col justify-between shadow-md relative overflow-hidden">
            <div className="absolute top-[-20%] right-[-10%] w-[200px] h-[200px] rounded-full bg-blue-500/10 blur-2xl" />
            <div className="z-10">
              <span className="text-xs text-blue-400 uppercase tracking-widest font-semibold">Consola de Evaluación de Riesgo</span>
              <h2 className="text-2xl font-bold mt-2">Bienvenido, Dr(a).</h2>
              <p className="text-slate-400 text-sm mt-1 leading-relaxed">
                Utilice el soporte de predicción cardiovascular para evaluar nuevos pacientes y realizar valoraciones de riesgo basadas en biomarcadores.
              </p>
            </div>
            
            <div className="mt-6 z-10 flex flex-wrap gap-3">
              <button 
                onClick={() => setShowAddPatient(true)}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm font-semibold text-white flex items-center gap-1.5 transition cursor-pointer"
              >
                <UserPlus className="w-4 h-4" />
                Registrar Paciente
              </button>
              
              <button 
                onClick={handleExportTrainingData}
                disabled={evaluations.length === 0}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 disabled:bg-slate-900 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-sm font-semibold text-white flex items-center gap-1.5 transition cursor-pointer border border-slate-700"
              >
                <TrendingUp className="w-4 h-4" />
                Exportar Datos de Entrenamiento (CSV)
              </button>
            </div>
          </div>

          {/* Tarjeta Stats: Pacientes */}
          <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm flex items-center gap-5 medical-card-shadow">
            <div className="p-4 bg-blue-50 rounded-xl text-blue-600">
              <Users className="w-6 h-6" />
            </div>
            <div>
              <span className="text-slate-400 text-xs font-semibold uppercase tracking-wider block">Pacientes en Base</span>
              <span className="text-3xl font-extrabold text-slate-800 mt-1 block">{patients.length}</span>
              <span className="text-[10px] text-slate-400 font-medium">Registrados en consulta</span>
            </div>
          </div>

          {/* Tarjeta Stats: Evaluaciones Críticas */}
          <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm flex items-center gap-5 medical-card-shadow">
            <div className="p-4 bg-rose-50 rounded-xl text-rose-600">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <div>
              <span className="text-slate-400 text-xs font-semibold uppercase tracking-wider block">Alertas de Riesgo Alto</span>
              <span className="text-3xl font-extrabold text-slate-800 mt-1 block">{highRiskCount}</span>
              <span className="text-[10px] text-rose-600 font-semibold">{totalEvaluationsCount > 0 ? `${Math.round((highRiskCount / totalEvaluationsCount) * 100)}%` : '0%'} del total evaluado</span>
            </div>
          </div>
        </section>

        {/* Tabla de Pacientes y Buscador */}
        <section className="bg-white border border-slate-100 rounded-2xl shadow-sm overflow-hidden medical-card-shadow">
          <div className="p-6 border-b border-slate-50 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h3 className="text-lg font-bold text-slate-800">Directorio de Pacientes y Evaluaciones</h3>
              <p className="text-slate-400 text-xs mt-0.5">Seleccione un paciente de la lista para gestionar sus antecedentes o iniciar una evaluación de riesgo.</p>
            </div>
            
            <div className="flex flex-wrap items-center gap-4 w-full sm:w-auto">
              <label className="flex items-center gap-2 cursor-pointer text-xs font-semibold text-slate-600 select-none">
                <input
                  type="checkbox"
                  checked={showSuspended}
                  onChange={(e) => setShowSuspended(e.target.checked)}
                  className="rounded border-slate-300 text-slate-900 focus:ring-slate-900 w-4 h-4 cursor-pointer"
                />
                <span>Mostrar Suspendidos</span>
              </label>

              <div className="relative w-full sm:max-w-[280px]">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="text"
                  placeholder="Buscar por nombre o CURP..."
                  className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-600/20 focus:border-slate-800 transition"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 text-[10px] font-bold text-slate-500 uppercase tracking-wider border-b border-slate-100">
                  <th className="py-4 px-6">Nombre Completo / CURP</th>
                  <th className="py-4 px-6">Fecha de Nacimiento</th>
                  <th className="py-4 px-6">Última Evaluación</th>
                  <th className="py-4 px-6">Riesgo CDSS</th>
                  <th className="py-4 px-6 text-right">Acciones</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50 text-sm text-slate-700">
                {filteredPatients.length > 0 ? (
                  filteredPatients.map(patient => {
                    const latestEval = getLatestEval(patient.id);
                    return (
                      <tr key={patient.id} className="hover:bg-slate-50/50 transition">
                        <td className="py-4.5 px-6">
                          <div className="flex items-center gap-2">
                            <div>
                              <span className="font-semibold text-slate-900 block">{patient.first_name} {patient.last_name}</span>
                              <span className="text-xs text-slate-400 font-mono">{patient.curp || 'S/N CURP'}</span>
                            </div>
                            {patient.activo === false && (
                              <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-100 uppercase tracking-wider scale-90">
                                Suspendido
                              </span>
                            )}
                          </div>
                        </td>
                        <td className="py-4.5 px-6 font-medium text-slate-600">
                          {patient.fecha_nacimiento}
                        </td>
                        <td className="py-4.5 px-6 font-medium text-slate-500">
                          {latestEval 
                            ? new Date(latestEval.fecha_evaluacion).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' })
                            : 'Ninguna'
                          }
                        </td>
                        <td className="py-4.5 px-6">
                          {latestEval ? (
                            <div className="flex items-center gap-1.5">
                              {latestEval.nivel_riesgo_predicho === 'Alto' ? (
                                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-rose-50 border border-rose-100 text-rose-700">
                                  🔴 Alto (Certeza: {latestEval.probabilidad_predicha}%)
                                </span>
                              ) : latestEval.nivel_riesgo_predicho === 'Medio' ? (
                                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-yellow-50 border border-yellow-100 text-yellow-800">
                                  🟡 Medio (Certeza: {latestEval.probabilidad_predicha}%)
                                </span>
                              ) : (
                                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-50 border border-emerald-100 text-emerald-700">
                                  🟢 Bajo (Certeza: {latestEval.probabilidad_predicha}%)
                                </span>
                              )}
                              
                              <div className="group relative cursor-help text-slate-400 hover:text-slate-650 transition">
                                <HelpCircle className="w-3.5 h-3.5" />
                                <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 hidden group-hover:block bg-slate-900 text-white text-[10px] p-2.5 rounded-lg shadow-xl z-50 text-center leading-normal font-sans font-medium">
                                  Este porcentaje representa la confianza del modelo XGBoost en su clasificación, no la magnitud del riesgo en sí.
                                  <div className="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-slate-900" />
                                </div>
                              </div>
                            </div>
                          ) : (
                            <span className="text-xs text-slate-400 italic">Sin evaluar</span>
                          )}
                        </td>
                        <td className="py-4.5 px-6 text-right">
                          <div className="flex items-center justify-end gap-2">
                            <button
                              onClick={() => router.push(`/paciente/${patient.id}`)}
                              className="inline-flex items-center gap-1 py-1.5 px-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-bold transition cursor-pointer border border-slate-200"
                              title="Ver expediente e historial clínico"
                            >
                              <TrendingUp className="w-3.5 h-3.5 text-slate-500" />
                              Historial
                            </button>
                            
                            <button
                              onClick={() => router.push(`/evaluacion?patientId=${patient.id}`)}
                              disabled={patient.activo === false}
                              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-900 hover:bg-slate-800 disabled:bg-slate-200 disabled:text-slate-400 disabled:cursor-not-allowed text-white rounded-lg text-xs font-semibold cursor-pointer transition shadow-sm"
                              title={patient.activo === false ? "Active al paciente para evaluar" : "Iniciar soporte CDSS"}
                            >
                              Evaluar CDSS
                              <ChevronRight className="w-3 h-3" />
                            </button>

                            <button
                              onClick={() => handleToggleActive(patient)}
                              className={`p-1.5 rounded-lg border text-xs font-bold transition cursor-pointer ${patient.activo === false ? 'bg-emerald-50 hover:bg-emerald-100 border-emerald-250 text-emerald-700' : 'bg-amber-50 hover:bg-amber-100 border-amber-250 text-amber-700'}`}
                              title={patient.activo === false ? "Reactivar expediente del paciente" : "Suspender expediente (preserva datos para IA)"}
                            >
                              {patient.activo === false ? <UserCheck className="w-3.5 h-3.5" /> : <UserMinus className="w-3.5 h-3.5" />}
                            </button>

                            <button
                              onClick={() => setConfirmDeletePatient(patient)}
                              className="p-1.5 bg-rose-50 hover:bg-rose-100 border border-rose-250 text-rose-600 rounded-lg text-xs font-bold transition cursor-pointer"
                              title="Eliminar expediente permanentemente"
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })
                ) : (
                  <tr>
                    <td colSpan={5} className="py-12 text-center text-slate-400">
                      <ClipboardList className="w-12 h-12 mx-auto text-slate-300 stroke-[1.5] mb-2" />
                      No se encontraron pacientes registrados con ese criterio.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

      </main>

      {/* Modal / Panel Flotante Agregar Paciente */}
      {showAddPatient && (
        <div className="fixed inset-0 bg-slate-950/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="w-full max-w-[500px] bg-white rounded-2xl border border-slate-100 shadow-2xl p-6 md:p-8 space-y-6">
            <div>
              <h3 className="text-xl font-bold text-slate-900">Registrar Paciente Nuevo</h3>
              <p className="text-slate-400 text-xs mt-0.5">Ingrese los datos generales para crear la ficha en el consultorio.</p>
            </div>

            <form onSubmit={handleAddPatientSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Nombre(s) *</label>
                  <input
                    type="text"
                    required
                    placeholder="ej. Juan"
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition"
                    value={newFirstName}
                    onChange={(e) => setNewFirstName(e.target.value)}
                  />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Apellido(s) *</label>
                  <input
                    type="text"
                    required
                    placeholder="ej. Pérez"
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition"
                    value={newLastName}
                    onChange={(e) => setNewLastName(e.target.value)}
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">CURP (18 Dígitos)</label>
                <input
                  type="text"
                  maxLength={18}
                  placeholder="ej. PEMA900101HDFRNS09"
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition font-mono uppercase"
                  value={newCurp}
                  onChange={(e) => setNewCurp(e.target.value)}
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1">Fecha de Nacimiento *</label>
                <input
                  type="date"
                  required
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition"
                  value={newDob}
                  onChange={(e) => setNewDob(e.target.value)}
                />
              </div>

              <div className="pt-4 flex justify-end gap-3 border-t border-slate-50 text-sm">
                <button
                  type="button"
                  onClick={() => setShowAddPatient(false)}
                  className="px-4 py-2 hover:bg-slate-100 rounded-lg font-semibold text-slate-500 cursor-pointer transition"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-slate-900 hover:bg-slate-800 rounded-lg font-semibold text-white cursor-pointer transition shadow-md"
                >
                  Confirmar Registro
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
      {confirmDeletePatient && (
        <div className="fixed inset-0 bg-slate-950/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="w-full max-w-[440px] bg-white rounded-2xl border border-slate-100 shadow-2xl p-6 md:p-8 space-y-5">
            <div className="flex items-center gap-3 text-rose-600">
              <div className="p-2 bg-rose-50 rounded-xl">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">¿Eliminar Expediente?</h3>
            </div>
            
            <p className="text-slate-600 text-xs leading-relaxed">
              Está a punto de eliminar de forma permanente el expediente de <strong>{confirmDeletePatient.first_name} {confirmDeletePatient.last_name}</strong> ({confirmDeletePatient.curp || 'Sin CURP'}) y todo su historial de evaluaciones clínicas. Esta acción no se puede deshacer.
            </p>

            <div className="p-3 bg-amber-50 border border-amber-100 text-amber-800 rounded-lg text-[10px] leading-relaxed">
              ⚠️ <strong>Recomendación médica:</strong> Para preservar el historial clínico para el reentrenamiento continuo de los modelos de IA de CardioPredict, se sugiere <strong>Suspender</strong> en vez de eliminar permanentemente.
            </div>

            <div className="pt-3 flex justify-end gap-3 border-t border-slate-50 text-sm">
              <button
                type="button"
                onClick={() => setConfirmDeletePatient(null)}
                className="px-4 py-2 hover:bg-slate-100 rounded-lg font-semibold text-slate-500 cursor-pointer transition"
              >
                Cancelar
              </button>
              <button
                type="button"
                onClick={handleDeletePatientConfirm}
                className="px-4 py-2 bg-rose-600 hover:bg-rose-550 rounded-lg font-semibold text-white cursor-pointer transition shadow-md"
              >
                Eliminar Permanentemente
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
