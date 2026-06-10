'use client';

import React, { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { supabase } from '@/lib/supabase';
import { 
  ArrowLeft, Calendar, User, TrendingUp, Plus, FileSpreadsheet, 
  Sparkles, ChevronDown, ChevronUp, CheckCircle, AlertCircle, 
  ShieldCheck, Heart, Info, ClipboardList, FileText
} from 'lucide-react';
import { Patient, Evaluation } from '@/types';
import { 
  ResponsiveContainer, LineChart, Line, XAxis, YAxis, 
  Tooltip, Legend, CartesianGrid, ReferenceLine 
} from 'recharts';

const BIOMARKER_METADATA: Record<string, { name: string; unit: string; normalMax: number; normalMin?: number; normalDesc: string }> = {
  "valor_hemoglobina_glucosilada": { name: "HbA1c", unit: "%", normalMax: 5.6, normalDesc: "Normal < 5.7%" },
  "valor_colesterol_ldl": { name: "Colesterol LDL", unit: "mg/dL", normalMax: 99, normalDesc: "Normal < 100 mg/dL" },
  "tension_arterial": { name: "Presión Sistólica", unit: "mmHg", normalMax: 119, normalDesc: "Normal < 120 mmHg" },
  "masa_corporal": { name: "IMC", unit: "kg/m²", normalMax: 24.9, normalMin: 18.5, normalDesc: "Normal: 18.5 - 24.9" },
  "resultado_glucosa": { name: "Glucosa", unit: "mg/dL", normalMax: 99, normalDesc: "Normal < 100 mg/dL" },
  "valor_colesterol_total": { name: "Colesterol Total", unit: "mg/dL", normalMax: 199, normalDesc: "Normal < 200 mg/dL" },
  "valor_trigliceridos": { name: "Triglicéridos", unit: "mg/dL", normalMax: 149, normalDesc: "Normal < 150 mg/dL" },
  "valor_proteinac_reactiva": { name: "Proteína C Reactiva", unit: "mg/L", normalMax: 1.0, normalDesc: "Bajo Riesgo < 1.0 mg/L" }
};

export default function PacienteDetallePage() {
  const router = useRouter();
  const params = useParams();
  const patientId = params.id as string;

  const [patient, setPatient] = useState<Patient | null>(null);
  const [evaluations, setEvaluations] = useState<Evaluation[]>([]);
  const [selectedBiomarker, setSelectedBiomarker] = useState<string>("valor_hemoglobina_glucosilada");
  const [expandedEvalId, setExpandedEvalId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'riesgo' | 'biomarcadores'>('riesgo');
  const [printMode, setPrintMode] = useState<'single' | 'history' | null>(null);

  const handlePrintActiveEvaluation = () => {
    setPrintMode('single');
    const afterPrint = () => {
      setPrintMode(null);
      window.removeEventListener('afterprint', afterPrint);
    };
    window.addEventListener('afterprint', afterPrint);
    setTimeout(() => {
      window.print();
    }, 250);
  };

  const handlePrintHistory = () => {
    setPrintMode('history');
    const afterPrint = () => {
      setPrintMode(null);
      window.removeEventListener('afterprint', afterPrint);
    };
    window.addEventListener('afterprint', afterPrint);
    setTimeout(() => {
      window.print();
    }, 250);
  };

  useEffect(() => {
    // Validar sesión
    const email = localStorage.getItem('cdss_doctor_email');
    if (!email) {
      router.push('/login');
      return;
    }

    // Cargar paciente de localStorage como fallback inicial
    const savedPatients = localStorage.getItem('cdss_patients');
    if (savedPatients) {
      const parsed: Patient[] = JSON.parse(savedPatients);
      const found = parsed.find(p => p.id === patientId);
      if (found) {
        setPatient(found);
      }
    }

    // Cargar evaluaciones de este paciente de localStorage como fallback inicial
    const savedEvaluations = localStorage.getItem('cdss_evaluations');
    let localEvals: Evaluation[] = [];
    if (savedEvaluations) {
      const parsed: Evaluation[] = JSON.parse(savedEvaluations);
      localEvals = parsed
        .filter(e => e.patient_id === patientId)
        .sort((a, b) => new Date(a.fecha_evaluacion).getTime() - new Date(b.fecha_evaluacion).getTime());
      setEvaluations(localEvals);
      
      if (localEvals.length > 0) {
        setExpandedEvalId(localEvals[localEvals.length - 1].id);
      }
    }

    // Cargar de Supabase en tiempo real si no es sesión simulada
    const isSimulated = localStorage.getItem('cdss_simulated_session') === 'true';
    if (!isSimulated) {
      const fetchFromSupabase = async () => {
        try {
          // 1. Fetch Patient
          const { data: dbPatient, error: patError } = await supabase
            .from('patients')
            .select('*')
            .eq('id', patientId)
            .single();
          
          if (patError) throw patError;
          if (dbPatient) {
            setPatient(dbPatient);
            // Sincronizar en localStorage
            const savedPats = localStorage.getItem('cdss_patients');
            let pats: Patient[] = savedPats ? JSON.parse(savedPats) : [];
            const index = pats.findIndex(p => p.id === dbPatient.id);
            if (index > -1) {
              pats[index] = dbPatient;
            } else {
              pats.push(dbPatient);
            }
            localStorage.setItem('cdss_patients', JSON.stringify(pats));
          }

          // 2. Fetch Evaluations
          const { data: dbEvals, error: evalError } = await supabase
            .from('evaluations')
            .select('*')
            .eq('patient_id', patientId);
          
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

            const sorted = mappedEvals.sort((a, b) => new Date(a.fecha_evaluacion).getTime() - new Date(b.fecha_evaluacion).getTime());
            setEvaluations(sorted);
            if (sorted.length > 0) {
              setExpandedEvalId(sorted[sorted.length - 1].id);
            }

            // Sincronizar en localStorage completo
            const savedAllEvaluations = localStorage.getItem('cdss_evaluations');
            let allEvals: Evaluation[] = savedAllEvaluations ? JSON.parse(savedAllEvaluations) : [];
            // Filtrar las previas de este paciente
            allEvals = allEvals.filter(e => e.patient_id !== patientId);
            // Añadir las nuevas
            allEvals.push(...sorted);
            localStorage.setItem('cdss_evaluations', JSON.stringify(allEvals));
          }
        } catch (err) {
          console.error("Error al sincronizar detalle del paciente con Supabase:", err);
        }
      };

      fetchFromSupabase();
    }
  }, [patientId, router]);

  // Actualizar el Gold Standard (resultado_real) de una evaluación e iniciar reentrenamiento automático
  const handleUpdateOutcome = async (evalId: string, value: 'Bajo' | 'Medio' | 'Alto' | null) => {
    // 1. Actualizar estado y localStorage
    const updatedEvals = evaluations.map(ev => {
      if (ev.id === evalId) {
        return { ...ev, resultado_real: value };
      }
      return ev;
    });
    
    // Guardar en el set completo
    const savedEvaluations = localStorage.getItem('cdss_evaluations');
    let updatedGlobal: Evaluation[] = [];
    if (savedEvaluations) {
      const parsed: Evaluation[] = JSON.parse(savedEvaluations);
      updatedGlobal = parsed.map(ev => {
        if (ev.id === evalId) {
          return { ...ev, resultado_real: value };
        }
        return ev;
      });
      localStorage.setItem('cdss_evaluations', JSON.stringify(updatedGlobal));
    }

    // Actualizar estado local (conservar orden para gráficos)
    setEvaluations(updatedEvals);

    // 2. Persistir en Supabase si no es sesión simulada
    const isSimulated = localStorage.getItem('cdss_simulated_session') === 'true';
    if (!isSimulated) {
      try {
        const { error } = await supabase
          .from('evaluations')
          .update({ resultado_real: value })
          .eq('id', evalId);

        if (error) {
          console.error("Error al actualizar resultado_real en Supabase:", error.message);
        } else {
          console.log("Resultado real actualizado de forma persistente en Supabase.");
        }
      } catch (err) {
        console.error("Fallo de comunicación con Supabase:", err);
      }
    }

    // 3. Disparar Reentrenamiento Automático en Tiempo Real
    try {
      const apiURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const payloadEvals = updatedGlobal.length > 0 ? updatedGlobal : updatedEvals;
      
      console.log("Disparando reentrenamiento automático en el backend...");
      fetch(`${apiURL}/api/v1/train`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ evaluations: payloadEvals })
      })
      .then(res => {
        if (!res.ok) throw new Error("Servidor de entrenamiento retornó error.");
        return res.json();
      })
      .then(data => {
        console.log("Reentrenamiento en tiempo real completado exitosamente:", data);
      })
      .catch(err => {
        console.warn("No se pudo completar el reentrenamiento automático. (Asegúrate de que el backend esté accesible):", err.message);
      });
    } catch (err: any) {
      console.error("Error al disparar reentrenamiento:", err.message);
    }
  };

  // Exportar historial de este paciente a CSV
  const handleExportPatientCSV = () => {
    if (!patient) return;
    const features = [
      "fecha_evaluacion", "sexo", "edad", "peso", "estatura", "medida_cintura", 
      "masa_corporal", "tension_arterial", "resultado_glucosa", "valor_colesterol_ldl", 
      "valor_colesterol_hdl", "valor_colesterol_total", "valor_trigliceridos",
      "valor_hemoglobina_glucosilada", "valor_proteinac_reactiva", "valor_insulina", 
      "valor_acido_urico", "sueno_horas", "actividad_total", "nivel_riesgo_predicho", 
      "probabilidad_predicha", "resultado_real"
    ];

    const csvHeader = features.join(",") + "\n";
    const csvRows = evaluations.map(e => {
      const rowValues = features.map(feat => {
        let val = e[feat as keyof Evaluation];
        return val !== undefined && val !== null ? val : "";
      });
      return rowValues.join(",");
    }).join("\n");

    const blob = new Blob([csvHeader + csvRows], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `historial_${patient.first_name}_${patient.last_name}_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (!patient) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <span className="text-slate-400 font-medium">Cargando expediente del paciente...</span>
      </div>
    );
  }

  // Estimar edad
  const birthYear = new Date(patient.fecha_nacimiento).getFullYear();
  const currentYear = new Date().getFullYear();
  const edadPaciente = currentYear - birthYear;

  // Preparar datos para los gráficos
  const chartData = evaluations.map(ev => {
    const dateStr = new Date(ev.fecha_evaluacion).toLocaleDateString('es-MX', { day: '2-digit', month: 'short' });
    return {
      name: dateStr,
      dateLong: new Date(ev.fecha_evaluacion).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' }),
      Bajo: ev.distribucion_probabilidades?.Bajo || 0,
      Medio: ev.distribucion_probabilidades?.Medio || 0,
      Alto: ev.distribucion_probabilidades?.Alto || 0,
      value: ev[selectedBiomarker as keyof Evaluation] || 0
    };
  });

  const selectedMeta = BIOMARKER_METADATA[selectedBiomarker];

  // Orden cronológico inverso (el más reciente primero) para el listado textual
  const reverseEvals = [...evaluations].reverse();

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      
      {/* Cabecera del Expediente */}
      <header className="bg-white border-b border-slate-100 py-4 px-6 md:px-12 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 shadow-sm z-10 sticky top-0 glass-panel print:hidden">
        <div className="flex items-center gap-4">
          <button 
            onClick={() => router.push('/dashboard')}
            className="p-2 hover:bg-slate-50 rounded-xl transition text-slate-500 cursor-pointer"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          
          <div className="h-6 w-px bg-slate-200" />

          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-slate-900 rounded-xl text-white">
              <User className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-slate-900 leading-tight">
                {patient.first_name} {patient.last_name}
              </h1>
              <span className="text-xs text-slate-400 font-mono block mt-0.5">
                CURP: {patient.curp || 'S/N'} • Edad: {edadPaciente} años ({patient.fecha_nacimiento})
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          <button 
            onClick={handleExportPatientCSV}
            disabled={evaluations.length === 0}
            className="flex-1 md:flex-none px-4 py-2 border border-slate-200 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-xs font-bold text-slate-600 flex items-center justify-center gap-1.5 transition cursor-pointer print:hidden"
          >
            <FileSpreadsheet className="w-3.5 h-3.5" />
            Exportar Historial (CSV)
          </button>

          {/* Menú de Reportes PDF */}
          <div className="relative group flex-1 md:flex-none print:hidden">
            <button
              disabled={evaluations.length === 0}
              className="w-full md:w-auto px-4 py-2 border border-slate-200 bg-white hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-xs font-bold text-slate-700 flex items-center justify-center gap-1.5 transition cursor-pointer"
            >
              <FileText className="w-3.5 h-3.5 text-rose-500" />
              Reportes PDF
              <ChevronDown className="w-3 h-3 text-slate-400" />
            </button>
            <div className="absolute right-0 top-full mt-1.5 w-56 bg-white border border-slate-200 rounded-xl shadow-xl z-50 py-1.5 hidden group-hover:block transition font-sans">
              <button
                onClick={handlePrintActiveEvaluation}
                className="w-full text-left px-4 py-2 hover:bg-slate-50 text-xs font-semibold text-slate-700 flex items-center gap-2 cursor-pointer"
              >
                📄 Imprimir Evaluación Actual
              </button>
              <button
                onClick={handlePrintHistory}
                className="w-full text-left px-4 py-2 hover:bg-slate-50 text-xs font-semibold text-slate-700 flex items-center gap-2 cursor-pointer"
              >
                📊 Imprimir Evolución Completa
              </button>
            </div>
          </div>

          <button 
            onClick={() => router.push(`/evaluacion?patientId=${patient.id}`)}
            className="flex-1 md:flex-none px-4 py-2 bg-slate-900 hover:bg-slate-800 rounded-lg text-xs font-bold text-white flex items-center justify-center gap-1.5 transition cursor-pointer shadow-md print:hidden"
          >
            <Plus className="w-3.5 h-3.5" />
            Nueva Evaluación
          </button>
        </div>
      </header>

      {/* Grid Principal */}
      <main className="flex-1 max-w-[1400px] w-full mx-auto p-4 md:p-8 grid grid-cols-1 lg:grid-cols-12 gap-8 print:hidden">
        
        {/* Columna Izquierda: Visualización de Evolución (8 columnas) */}
        <section className="lg:col-span-8 space-y-6">
          <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm space-y-6 medical-card-shadow">
            
            {/* Header de Visualizaciones */}
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-slate-100 pb-4">
              <div>
                <h3 className="text-base font-bold text-slate-800 flex items-center gap-1.5">
                  <TrendingUp className="w-4 h-4 text-blue-600" />
                  Evolución Clínica del Paciente
                </h3>
                <p className="text-slate-400 text-xs mt-0.5">Línea del tiempo que demuestra el progreso médico del paciente en las consultas.</p>
              </div>

              {/* Tabs */}
              <div className="flex bg-slate-50 border border-slate-150 p-1 rounded-xl text-xs font-semibold">
                <button
                  onClick={() => setActiveTab('riesgo')}
                  className={`px-3 py-1.5 rounded-lg transition cursor-pointer ${activeTab === 'riesgo' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-400 hover:text-slate-600'}`}
                >
                  Riesgo CVD
                </button>
                <button
                  onClick={() => setActiveTab('biomarcadores')}
                  className={`px-3 py-1.5 rounded-lg transition cursor-pointer ${activeTab === 'biomarcadores' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-400 hover:text-slate-600'}`}
                >
                  Biomarcadores
                </button>
              </div>
            </div>

            {/* Contenido de Gráfico */}
            {evaluations.length > 1 ? (
              <div className="space-y-4">
                
                {/* Controles para Biomarcadores */}
                {activeTab === 'biomarcadores' && (
                  <div className="flex flex-wrap items-center gap-3 bg-slate-50 border border-slate-100 rounded-xl p-3.5">
                    <span className="text-xs font-bold text-slate-500">Seleccionar Indicador:</span>
                    <select
                      className="px-2.5 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-600/20"
                      value={selectedBiomarker}
                      onChange={(e) => setSelectedBiomarker(e.target.value)}
                    >
                      {Object.entries(BIOMARKER_METADATA).map(([key, meta]) => (
                        <option key={key} value={key}>{meta.name} ({meta.unit})</option>
                      ))}
                    </select>

                    <div className="text-xs font-medium text-slate-500 flex items-center gap-1.5 ml-auto">
                      <Info className="w-3.5 h-3.5 text-blue-500" />
                      <span>Rango objetivo: {selectedMeta.normalDesc}</span>
                    </div>
                  </div>
                )}

                {/* El Gráfico */}
                <div className="h-[320px] w-full text-xs font-medium pr-4">
                  <ResponsiveContainer width="100%" height="100%">
                    {activeTab === 'riesgo' ? (
                      <LineChart data={chartData} margin={{ top: 10, right: 10, left: -10, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                        <XAxis dataKey="name" stroke="#94a3b8" />
                        <YAxis domain={[0, 100]} stroke="#94a3b8" />
                        <Tooltip 
                          contentStyle={{ borderRadius: 12, boxShadow: '0 4px 12px rgba(0,0,0,0.05)', border: '1px solid #f1f5f9' }}
                          formatter={(value: any, name: any) => [`${parseFloat(value).toFixed(1)}%`, name]}
                        />
                        <Legend iconType="circle" />
                        <Line type="monotone" dataKey="Bajo" name="Prob. Bajo Riesgo" stroke="#10b981" strokeWidth={3} activeDot={{ r: 6 }} />
                        <Line type="monotone" dataKey="Medio" name="Prob. Medio Riesgo" stroke="#eab308" strokeWidth={3} activeDot={{ r: 6 }} />
                        <Line type="monotone" dataKey="Alto" name="Prob. Alto Riesgo" stroke="#ef4444" strokeWidth={3} activeDot={{ r: 6 }} />
                      </LineChart>
                    ) : (
                      <LineChart data={chartData} margin={{ top: 10, right: 10, left: -10, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                        <XAxis dataKey="name" stroke="#94a3b8" />
                        <YAxis stroke="#94a3b8" />
                        <Tooltip 
                          contentStyle={{ borderRadius: 12, boxShadow: '0 4px 12px rgba(0,0,0,0.05)', border: '1px solid #f1f5f9' }}
                          formatter={(value: any) => [`${value} ${selectedMeta.unit}`, selectedMeta.name]}
                        />
                        <Legend iconType="circle" />
                        <ReferenceLine y={selectedMeta.normalMax} stroke="#ef4444" strokeDasharray="3 3" label={{ value: 'Límite Máximo', position: 'top', fill: '#ef4444', fontSize: 9 }} />
                        {selectedMeta.normalMin && (
                          <ReferenceLine y={selectedMeta.normalMin} stroke="#3b82f6" strokeDasharray="3 3" label={{ value: 'Límite Mínimo', position: 'bottom', fill: '#3b82f6', fontSize: 9 }} />
                        )}
                        <Line type="monotone" dataKey="value" name={selectedMeta.name} stroke="#3b82f6" strokeWidth={3} activeDot={{ r: 6 }} />
                      </LineChart>
                    )}
                  </ResponsiveContainer>
                </div>
              </div>
            ) : (
              <div className="py-16 text-center border border-dashed border-slate-200 rounded-2xl bg-slate-50 flex flex-col justify-center items-center">
                <TrendingUp className="w-12 h-12 text-slate-300 stroke-[1.5] mb-2" />
                <h4 className="text-sm font-bold text-slate-700">Esperando Más Evaluaciones</h4>
                <p className="text-slate-400 text-xs mt-1 max-w-[340px] leading-relaxed">
                  Se requieren al menos **2 chequeos** clínicos para generar gráficos de tendencia y visualizaciones de evolución temporal.
                </p>
              </div>
            )}
          </div>
        </section>

        {/* Columna Derecha: Expedientes Históricos (4 columnas) */}
        <section className="lg:col-span-4 space-y-6">
          <div className="bg-white border border-slate-100 rounded-2xl p-6 shadow-sm space-y-5 medical-card-shadow">
            <div>
              <h3 className="text-base font-bold text-slate-800 flex items-center gap-1.5">
                <ClipboardList className="w-4 h-4 text-blue-600" />
                Línea de Tiempo de Consultas
              </h3>
              <p className="text-slate-400 text-xs mt-0.5">Registro de cada evaluación realizada en CardioPredict.</p>
            </div>

            {reverseEvals.length > 0 ? (
              <div className="space-y-4 max-h-[500px] overflow-y-auto pr-1">
                {reverseEvals.map((ev, index) => {
                  const isExpanded = expandedEvalId === ev.id;
                  const evalDate = new Date(ev.fecha_evaluacion).toLocaleDateString('es-MX', { 
                    day: '2-digit', 
                    month: 'short',
                    year: 'numeric'
                  });
                  
                  return (
                    <div 
                      key={ev.id} 
                      className={`border rounded-xl transition overflow-hidden ${isExpanded ? 'border-slate-200 bg-white shadow-sm' : 'border-slate-100 hover:border-slate-200 bg-slate-50/50'}`}
                    >
                      {/* Cabecera de la evaluación */}
                      <button
                        onClick={() => setExpandedEvalId(isExpanded ? null : ev.id)}
                        className="w-full p-4 flex justify-between items-center text-left cursor-pointer"
                      >
                        <div className="space-y-1">
                          <span className="text-xs font-bold text-slate-800 block">{evalDate}</span>
                          <span className="text-[10px] text-slate-400 font-medium block">
                            Inferencia (Certeza: {ev.probabilidad_predicha}%)
                          </span>
                        </div>

                        <div className="flex items-center gap-2">
                          {ev.nivel_riesgo_predicho === 'Alto' ? (
                            <span className="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-rose-50 text-rose-700 border border-rose-100">
                              Alto
                            </span>
                          ) : ev.nivel_riesgo_predicho === 'Medio' ? (
                            <span className="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-yellow-50 text-yellow-800 border border-yellow-100">
                              Medio
                            </span>
                          ) : (
                            <span className="px-2 py-0.5 rounded-full text-[10px] font-extrabold bg-emerald-50 text-emerald-700 border border-emerald-100">
                              Bajo
                            </span>
                          )}
                          {isExpanded ? <ChevronUp className="w-4 h-4 text-slate-400" /> : <ChevronDown className="w-4 h-4 text-slate-400" />}
                        </div>
                      </button>

                      {/* Detalles extendidos */}
                      {isExpanded && (
                        <div className="px-4 pb-4 pt-1 border-t border-slate-50 space-y-4 text-xs">
                          {/* Biomarcadores clave */}
                          <div className="grid grid-cols-2 gap-x-4 gap-y-2 bg-slate-50 p-2.5 rounded-xl border border-slate-100 font-medium text-slate-600">
                            <div>HbA1c: <span className="font-bold text-slate-800">{ev.valor_hemoglobina_glucosilada}%</span></div>
                            <div>LDL: <span className="font-bold text-slate-800">{ev.valor_colesterol_ldl} mg/dL</span></div>
                            <div>Presión: <span className="font-bold text-slate-800">{ev.tension_arterial} mmHg</span></div>
                            <div>IMC: <span className="font-bold text-slate-800">{ev.masa_corporal} kg/m²</span></div>
                          </div>

                          {/* Explicación SHAP narrativa */}
                          <div className="space-y-1">
                            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wide block">Explicación Clínica del CDSS</span>
                            <p className="text-slate-600 leading-relaxed text-[11px] bg-slate-50/50 p-2 rounded-lg border border-slate-100">
                              {ev.explicacion_shap}
                            </p>
                          </div>

                          {/* Validación del Médico (Gold Standard) */}
                          <div className="pt-2 border-t border-slate-50 space-y-1.5">
                            <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wide block flex items-center gap-1">
                              <ShieldCheck className="w-3.5 h-3.5 text-blue-600" />
                              Resultado Clínico Real (Feedback CDSS)
                            </label>
                            
                            <select
                              value={ev.resultado_real || ''}
                              onChange={(e) => handleUpdateOutcome(ev.id, (e.target.value || null) as any)}
                              className="w-full px-2.5 py-1.5 bg-white border border-slate-200 rounded-lg text-xs font-bold text-slate-800 focus:outline-none focus:border-blue-500"
                            >
                              <option value="">🟡 Sin Confirmar (Usar predicción de IA)</option>
                              <option value="Bajo">🟢 Bajo Riesgo Confirmado</option>
                              <option value="Medio">🟡 Medio Riesgo Confirmado</option>
                              <option value="Alto">🔴 Alto Riesgo Confirmado</option>
                            </select>
                            
                            <p className="text-[10px] text-slate-400 leading-tight">
                              Establecer este campo consolida los datos como *Gold Standard* para futuros reentrenamientos del modelo XGBoost.
                            </p>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="py-12 text-center text-slate-400">
                Ninguna evaluación registrada para este paciente aún.
              </div>
            )}
          </div>
        </section>

      </main>

      {/* ========================================================================= */}
      {/* VISTA DE IMPRESIÓN: REPORTE CLÍNICO INDIVIDUAL (PDF) */}
      {/* ========================================================================= */}
      {printMode === 'single' && (
        (() => {
          const activeEval = evaluations.find(e => e.id === expandedEvalId) || evaluations[evaluations.length - 1];
          if (!activeEval) return null;
          return (
            <div className="hidden print:block w-full max-w-4xl mx-auto p-8 bg-white text-slate-800 font-sans text-xs space-y-6">
              {/* Cabecera / Membrete */}
              <div className="flex justify-between items-center border-b-2 border-slate-900 pb-4">
                <div>
                  <h1 className="text-xl font-bold uppercase tracking-wider text-slate-900">CardioPredict CDSS</h1>
                  <p className="text-slate-500 font-semibold text-[10px] uppercase">Sistema de Soporte de Decisiones Clínicas - Riesgo Cardiovascular</p>
                </div>
                <div className="text-right text-[10px] text-slate-500 font-semibold">
                  <p>Reporte Clínico de Inferencia</p>
                  <p>Fecha de Impresión: {new Date().toLocaleDateString('es-MX')}</p>
                </div>
              </div>

              {/* Datos Demográficos del Paciente */}
              <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 grid grid-cols-2 gap-4">
                <div>
                  <p className="text-[10px] font-bold text-slate-400 uppercase">Paciente</p>
                  <p className="text-sm font-bold text-slate-850">{patient.first_name} {patient.last_name}</p>
                </div>
                <div>
                  <p className="text-[10px] font-bold text-slate-400 uppercase">CURP</p>
                  <p className="text-xs font-mono font-bold text-slate-700">{patient.curp || 'No Registrado'}</p>
                </div>
                <div>
                  <p className="text-[10px] font-bold text-slate-400 uppercase">Fecha de Nacimiento</p>
                  <p className="text-xs font-semibold text-slate-700">{patient.fecha_nacimiento} ({edadPaciente} años)</p>
                </div>
                <div>
                  <p className="text-[10px] font-bold text-slate-400 uppercase">Fecha de Evaluación</p>
                  <p className="text-xs font-semibold text-slate-700">
                    {new Date(activeEval.fecha_evaluacion).toLocaleDateString('es-MX', { day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>

              {/* Resultado de la Clasificación de Riesgo */}
              <div className="p-4 rounded-xl border flex items-center justify-between gap-6 bg-slate-50/50">
                <div className="space-y-1">
                  <p className="text-[10px] font-bold text-slate-400 uppercase">Riesgo Cardiovascular CDSS</p>
                  <div className="flex items-center gap-2">
                    {activeEval.nivel_riesgo_predicho === 'Alto' ? (
                      <span className="text-sm font-extrabold text-rose-700">🔴 RIESGO CARDIOVASCULAR ALTO</span>
                    ) : activeEval.nivel_riesgo_predicho === 'Medio' ? (
                      <span className="text-sm font-extrabold text-amber-700">🟡 RIESGO CARDIOVASCULAR MEDIO</span>
                    ) : (
                      <span className="text-sm font-extrabold text-emerald-700">🟢 RIESGO CARDIOVASCULAR BAJO</span>
                    )}
                  </div>
                </div>
                <div className="text-right space-y-1">
                  <p className="text-[10px] font-bold text-slate-400 uppercase">Certeza de Clasificación</p>
                  <p className="text-lg font-extrabold text-slate-900">{activeEval.probabilidad_predicha}% <span className="text-xs font-normal text-slate-500">(Confianza XGBoost)</span></p>
                </div>
              </div>

              {/* Tabla de Biomarcadores y Mediciones */}
              <div className="space-y-2">
                <h3 className="text-xs font-bold text-slate-850 border-b border-slate-200 pb-1 uppercase tracking-wide">Ficha de Biomarcadores e Indicadores</h3>
                <table className="w-full text-left border-collapse border border-slate-200">
                  <thead>
                    <tr className="bg-slate-50 text-[9px] font-bold text-slate-600 uppercase border-b border-slate-200">
                      <th className="p-2 border-r border-slate-200">Biomarcador / Indicador</th>
                      <th className="p-2 border-r border-slate-200 text-center">Valor Obtenido</th>
                      <th className="p-2 border-r border-slate-200 text-center">Rango Objetivo / Referencia</th>
                      <th className="p-2 text-center">Evaluación Clínica</th>
                    </tr>
                  </thead>
                  <tbody className="text-[10px] divide-y divide-slate-150">
                    <tr>
                      <td className="p-2 border-r border-slate-200 font-semibold">Hemoglobina Glucosilada (HbA1c)</td>
                      <td className="p-2 border-r border-slate-200 text-center font-bold">{activeEval.valor_hemoglobina_glucosilada}%</td>
                      <td className="p-2 border-r border-slate-200 text-center text-slate-500">{"< 5.7% (Normal)"}</td>
                      <td className="p-2 text-center">
                        {activeEval.valor_hemoglobina_glucosilada >= 5.7 ? (
                          <span className="text-rose-600 font-bold">⚠️ Alterado (Pre/Diabetes)</span>
                        ) : (
                          <span className="text-emerald-600 font-bold">✓ Normal</span>
                        )}
                      </td>
                    </tr>
                    <tr>
                      <td className="p-2 border-r border-slate-200 font-semibold">Colesterol LDL</td>
                      <td className="p-2 border-r border-slate-200 text-center font-bold">{activeEval.valor_colesterol_ldl} mg/dL</td>
                      <td className="p-2 border-r border-slate-200 text-center text-slate-500">{"< 100 mg/dL (Normal)"}</td>
                      <td className="p-2 text-center">
                        {activeEval.valor_colesterol_ldl >= 100 ? (
                          <span className="text-rose-600 font-bold">⚠️ Elevado</span>
                        ) : (
                          <span className="text-emerald-600 font-bold">✓ Normal</span>
                        )}
                      </td>
                    </tr>
                    <tr>
                      <td className="p-2 border-r border-slate-200 font-semibold">Presión Arterial Sistólica</td>
                      <td className="p-2 border-r border-slate-200 text-center font-bold">{activeEval.tension_arterial} mmHg</td>
                      <td className="p-2 border-r border-slate-200 text-center text-slate-500">{"< 120 mmHg (Normal)"}</td>
                      <td className="p-2 text-center">
                        {activeEval.tension_arterial >= 130 ? (
                          <span className="text-rose-600 font-bold">⚠️ Hipertensión</span>
                        ) : activeEval.tension_arterial >= 120 ? (
                          <span className="text-amber-600 font-bold">⚠️ Elevada</span>
                        ) : (
                          <span className="text-emerald-600 font-bold">✓ Normal</span>
                        )}
                      </td>
                    </tr>
                    <tr>
                      <td className="p-2 border-r border-slate-200 font-semibold">Índice de Masa Corporal (IMC)</td>
                      <td className="p-2 border-r border-slate-200 text-center font-bold">{activeEval.masa_corporal} kg/m²</td>
                      <td className="p-2 border-r border-slate-200 text-center text-slate-500">18.5 - 24.9 (Normal)</td>
                      <td className="p-2 text-center">
                        {activeEval.masa_corporal >= 30 ? (
                          <span className="text-rose-600 font-bold">⚠️ Obesidad</span>
                        ) : activeEval.masa_corporal >= 25 ? (
                          <span className="text-amber-600 font-bold">⚠️ Sobrepeso</span>
                        ) : (
                          <span className="text-emerald-600 font-bold">✓ Normal</span>
                        )}
                      </td>
                    </tr>
                    <tr>
                      <td className="p-2 border-r border-slate-200 font-semibold">Proteína C Reactiva (PCR-hs)</td>
                      <td className="p-2 border-r border-slate-200 text-center font-bold">{activeEval.valor_proteinac_reactiva} mg/L</td>
                      <td className="p-2 border-r border-slate-200 text-center text-slate-500">{"< 1.0 mg/L (Bajo Riesgo)"}</td>
                      <td className="p-2 text-center">
                        {activeEval.valor_proteinac_reactiva >= 3.0 ? (
                          <span className="text-rose-600 font-bold">⚠️ Alto Riesgo Inflamatorio</span>
                        ) : activeEval.valor_proteinac_reactiva >= 1.0 ? (
                          <span className="text-amber-600 font-bold">⚠️ Riesgo Moderado</span>
                        ) : (
                          <span className="text-emerald-600 font-bold">✓ Normal</span>
                        )}
                      </td>
                    </tr>
                    <tr>
                      <td className="p-2 border-r border-slate-200 font-semibold">Glucosa en Ayunas</td>
                      <td className="p-2 border-r border-slate-200 text-center font-bold">{activeEval.resultado_glucosa} mg/dL</td>
                      <td className="p-2 border-r border-slate-200 text-center text-slate-500">{"70 - 99 mg/dL (Normal)"}</td>
                      <td className="p-2 text-center">
                        {activeEval.resultado_glucosa >= 126 ? (
                          <span className="text-rose-600 font-bold">⚠️ Hiperglucemia Crítica</span>
                        ) : activeEval.resultado_glucosa >= 100 ? (
                          <span className="text-amber-600 font-bold">⚠️ Prediabetes</span>
                        ) : (
                          <span className="text-emerald-600 font-bold">✓ Normal</span>
                        )}
                      </td>
                    </tr>
                    <tr>
                      <td className="p-2 border-r border-slate-200 font-semibold">Colesterol Total</td>
                      <td className="p-2 border-r border-slate-200 text-center font-bold">{activeEval.valor_colesterol_total} mg/dL</td>
                      <td className="p-2 border-r border-slate-200 text-center text-slate-500">{"< 200 mg/dL (Normal)"}</td>
                      <td className="p-2 text-center">
                        {activeEval.valor_colesterol_total >= 200 ? (
                          <span className="text-rose-600 font-bold">⚠️ Hipercolesterolemia</span>
                        ) : (
                          <span className="text-emerald-600 font-bold">✓ Normal</span>
                        )}
                      </td>
                    </tr>
                    <tr>
                      <td className="p-2 border-r border-slate-200 font-semibold">Cintura / Abdominal</td>
                      <td className="p-2 border-r border-slate-200 text-center font-bold">{activeEval.medida_cintura} cm</td>
                      <td className="p-2 border-r border-slate-200 text-center text-slate-500">Hombre &lt; 90 cm | Mujer &lt; 80 cm</td>
                      <td className="p-2 text-center">
                        {(activeEval.sexo === 'Hombre' && activeEval.medida_cintura >= 90) || (activeEval.sexo === 'Mujer' && activeEval.medida_cintura >= 80) ? (
                          <span className="text-rose-600 font-bold">⚠️ Riesgo Abdominal</span>
                        ) : (
                          <span className="text-emerald-600 font-bold">✓ Normal</span>
                        )}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              {/* Explicación SHAP Narrativa */}
              <div className="space-y-2">
                <h3 className="text-xs font-bold text-slate-850 border-b border-slate-200 pb-1 uppercase tracking-wide">Explicación Clínica y Aporte SHAP</h3>
                <p className="text-slate-700 bg-slate-50 p-3.5 rounded-lg border border-slate-200 leading-relaxed font-mono text-[9.5px]">
                  {activeEval.explicacion_shap}
                </p>
              </div>

              {/* Notas Médicas y Firmas */}
              <div className="grid grid-cols-2 gap-8 pt-8">
                <div className="space-y-4">
                  <h4 className="text-[10px] font-bold text-slate-400 uppercase border-b border-slate-100 pb-1">Observaciones y Tratamiento del Médico</h4>
                  <div className="h-20 border-b border-dashed border-slate-350" />
                  <div className="h-20 border-b border-dashed border-slate-350" />
                </div>

                <div className="flex flex-col justify-end items-center text-center space-y-2">
                  <div className="w-48 border-b border-slate-400 pt-16" />
                  <p className="text-[10px] font-bold text-slate-800">Dr(a). {localStorage.getItem('cdss_doctor_email') || 'Médico Tratante'}</p>
                  <p className="text-[9px] text-slate-400">CardioPredict CDSS • Firma Autorizada</p>
                </div>
              </div>

              <div className="pt-8 text-center text-[9px] text-slate-400 border-t border-slate-100 leading-normal">
                Este reporte fue emitido por el sistema CardioPredict CDSS apoyado por modelos de inteligencia artificial (XGBoost). La predicción no reemplaza el juicio clínico final del especialista de la salud.
              </div>
            </div>
          );
        })()
      )}

      {/* ========================================================================= */}
      {/* VISTA DE IMPRESIÓN: EXPEDIENTE DE EVOLUCIÓN HISTÓRICA (PDF) */}
      {/* ========================================================================= */}
      {printMode === 'history' && (
        <div className="hidden print:block w-full max-w-4xl mx-auto p-8 bg-white text-slate-800 font-sans text-xs space-y-6">
          {/* Cabecera / Membrete */}
          <div className="flex justify-between items-center border-b-2 border-slate-900 pb-4">
            <div>
              <h1 className="text-xl font-bold uppercase tracking-wider text-slate-900">CardioPredict CDSS</h1>
              <p className="text-slate-500 font-semibold text-[10px] uppercase">Expediente de Evolución Histórica de Riesgo Cardiovascular</p>
            </div>
            <div className="text-right text-[10px] text-slate-500 font-semibold">
              <p>Expediente Clínico Consolidado</p>
              <p>Fecha de Impresión: {new Date().toLocaleDateString('es-MX')}</p>
            </div>
          </div>

          {/* Datos Demográficos */}
          <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 grid grid-cols-2 gap-4">
            <div>
              <p className="text-[10px] font-bold text-slate-400 uppercase">Paciente</p>
              <p className="text-sm font-bold text-slate-855">{patient.first_name} {patient.last_name}</p>
            </div>
            <div>
              <p className="text-[10px] font-bold text-slate-400 uppercase">CURP</p>
              <p className="text-xs font-mono font-bold text-slate-700">{patient.curp || 'No Registrado'}</p>
            </div>
            <div>
              <p className="text-[10px] font-bold text-slate-400 uppercase">Fecha de Nacimiento</p>
              <p className="text-xs font-semibold text-slate-700">{patient.fecha_nacimiento} ({edadPaciente} años)</p>
            </div>
            <div>
              <p className="text-[10px] font-bold text-slate-400 uppercase">Médico Tratante</p>
              <p className="text-xs font-semibold text-slate-700">{localStorage.getItem('cdss_doctor_email') || 'Médico Adscrito'}</p>
            </div>
          </div>

          {/* Resumen Histórico */}
          <div className="space-y-4">
            <h3 className="text-xs font-bold text-slate-855 border-b border-slate-200 pb-1 uppercase tracking-wide">Evolución de Evaluaciones Registradas ({evaluations.length})</h3>
            
            <table className="w-full text-left border-collapse border border-slate-200">
              <thead>
                <tr className="bg-slate-50 text-[9px] font-bold text-slate-600 uppercase border-b border-slate-200">
                  <th className="p-2 border-r border-slate-200">Fecha</th>
                  <th className="p-2 border-r border-slate-200 text-center">Riesgo Predicho</th>
                  <th className="p-2 border-r border-slate-200 text-center">Certeza</th>
                  <th className="p-2 border-r border-slate-200 text-center">HbA1c</th>
                  <th className="p-2 border-r border-slate-200 text-center">LDL (mg/dL)</th>
                  <th className="p-2 border-r border-slate-200 text-center">Presión Sist.</th>
                  <th className="p-2 border-r border-slate-200 text-center">IMC</th>
                  <th className="p-2 border-r border-slate-200 text-center">Glucosa</th>
                  <th className="p-2 text-center">Resultado Real</th>
                </tr>
              </thead>
              <tbody className="text-[10px] divide-y divide-slate-150">
                {evaluations.map((ev) => (
                  <tr key={ev.id}>
                    <td className="p-2 border-r border-slate-200 font-semibold">
                      {new Date(ev.fecha_evaluacion).toLocaleDateString('es-MX', { day: '2-digit', month: 'short', year: 'numeric' })}
                    </td>
                    <td className="p-2 border-r border-slate-200 text-center">
                      {ev.nivel_riesgo_predicho === 'Alto' ? (
                        <span className="text-rose-600 font-bold">🔴 Alto</span>
                      ) : ev.nivel_riesgo_predicho === 'Medio' ? (
                        <span className="text-amber-600 font-bold">🟡 Medio</span>
                      ) : (
                        <span className="text-emerald-600 font-bold">🟢 Bajo</span>
                      )}
                    </td>
                    <td className="p-2 border-r border-slate-200 text-center font-bold">{ev.probabilidad_predicha}%</td>
                    <td className="p-2 border-r border-slate-200 text-center">{ev.valor_hemoglobina_glucosilada}%</td>
                    <td className="p-2 border-r border-slate-200 text-center">{ev.valor_colesterol_ldl}</td>
                    <td className="p-2 border-r border-slate-200 text-center">{ev.tension_arterial}</td>
                    <td className="p-2 border-r border-slate-200 text-center">{ev.masa_corporal}</td>
                    <td className="p-2 border-r border-slate-200 text-center">{ev.resultado_glucosa}</td>
                    <td className="p-2 text-center font-semibold text-slate-600">
                      {ev.resultado_real ? `${ev.resultado_real} Confirmado` : 'Sin Confirmar'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Notas Médicas y Firmas */}
          <div className="grid grid-cols-2 gap-8 pt-8">
            <div className="space-y-4">
              <h4 className="text-[10px] font-bold text-slate-400 uppercase border-b border-slate-100 pb-1">Diagnóstico Clínico General e Indicaciones</h4>
              <div className="h-20 border-b border-dashed border-slate-355" />
              <div className="h-20 border-b border-dashed border-slate-355" />
            </div>

            <div className="flex flex-col justify-end items-center text-center space-y-2">
              <div className="w-48 border-b border-slate-400 pt-16" />
              <p className="text-[10px] font-bold text-slate-800">Dr(a). {localStorage.getItem('cdss_doctor_email') || 'Médico Tratante'}</p>
              <p className="text-[9px] text-slate-400">CardioPredict CDSS • Firma Autorizada</p>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
