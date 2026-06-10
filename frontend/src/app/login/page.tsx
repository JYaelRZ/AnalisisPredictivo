'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { supabase } from '@/lib/supabase';
import { ShieldCheck, Heart, Stethoscope, Lock, Mail, ChevronRight, AlertCircle } from 'lucide-react';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg('');

    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) {
        // En caso de que falle o no esté configurado el URL/Key real de Supabase,
        // permitimos el bypass solo para propósitos de demostración en local
        if (email === 'doctor@cardio.fit' && password === 'clinicalcdss2026') {
          // Guardar una sesión simulada en localStorage
          localStorage.setItem('cdss_simulated_session', 'true');
          localStorage.setItem('cdss_doctor_email', email);
          router.push('/dashboard');
          return;
        }
        throw error;
      }

      if (data.user) {
        localStorage.removeItem('cdss_simulated_session');
        localStorage.setItem('cdss_doctor_email', data.user.email || '');
        router.push('/dashboard');
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Error de credenciales incorrectas. (Prueba con doctor@cardio.fit / clinicalcdss2026 para demostración local)');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-height-screen bg-slate-50 flex items-center justify-center p-4 md:p-8 min-h-screen relative overflow-hidden">
      {/* Círculos decorativos de gradiente clínico */}
      <div className="absolute top-[-20%] left-[-10%] w-[500px] h-[500px] rounded-full bg-blue-100 blur-3xl opacity-60 pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] rounded-full bg-emerald-50 blur-3xl opacity-70 pointer-events-none" />

      <div className="w-full max-w-[1000px] bg-white rounded-2xl shadow-xl border border-slate-100 flex overflow-hidden z-10 glass-panel">
        
        {/* Columna Izquierda: Mensaje y Decorativo */}
        <div className="hidden md:flex md:w-1/2 bg-slate-900 p-12 text-white flex-col justify-between relative">
          <div className="absolute inset-0 bg-gradient-to-tr from-slate-950 to-blue-950 opacity-90" />
          <div className="z-10 flex items-center gap-2 text-blue-400 font-semibold tracking-wide">
            <Heart className="w-6 h-6 fill-current text-rose-500 animate-pulse" />
            <span>CardioPredict CDSS</span>
          </div>

          <div className="z-10 space-y-6">
            <h2 className="text-3xl font-bold font-sans leading-tight">
              Soporte Inteligente para Evaluación de Riesgo Cardiovascular
            </h2>
            <p className="text-slate-300 text-sm leading-relaxed">
              Plataforma clínica avanzada basada en modelos de Machine Learning (XGBoost) para la estratificación de riesgo cardiovascular multiclase en población adulta.
            </p>
            
            <div className="space-y-3 pt-4 border-t border-slate-800 text-xs text-slate-400">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-400" />
                <span>Cumplimiento estricto de seguridad LFPDPPP / HIPAA</span>
              </div>
              <div className="flex items-center gap-2">
                <Stethoscope className="w-4 h-4 text-blue-400" />
                <span>Explicabilidad clínica con valores matemáticos SHAP</span>
              </div>
            </div>
          </div>

          <div className="z-10 text-xs text-slate-500">
            © 2026 Tesis Profesional. Plataforma de Soporte Clínico.
          </div>
        </div>

        {/* Columna Derecha: Formulario */}
        <div className="w-full md:w-1/2 p-8 md:p-12 flex flex-col justify-center">
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-slate-900">Iniciar Sesión Médica</h3>
            <p className="text-slate-500 text-sm mt-1">
              Acceso restringido para profesionales de la salud autorizados
            </p>
          </div>

          {errorMsg && (
            <div className="p-4 mb-6 bg-rose-50 border border-rose-100 text-rose-800 rounded-lg text-xs flex items-start gap-2">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
              <span>{errorMsg}</span>
            </div>
          )}

          <form onSubmit={handleLogin} className="space-y-5">
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">
                Correo Electrónico
              </label>
              <div className="relative">
                <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="email"
                  required
                  placeholder="ejemplo@hospital.com"
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2">
                Contraseña de Acceso
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="password"
                  required
                  placeholder="••••••••••••"
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-600/20 focus:border-blue-600 transition"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 bg-slate-900 text-white rounded-lg text-sm font-semibold hover:bg-slate-800 transition flex items-center justify-center gap-2 cursor-pointer shadow-md disabled:bg-slate-400 disabled:cursor-not-allowed"
            >
              {loading ? 'Validando Credenciales...' : 'Acceder al Sistema'}
              {!loading && <ChevronRight className="w-4 h-4" />}
            </button>
          </form>

          <div className="mt-8 pt-6 border-t border-slate-100 text-center">
            <p className="text-xs text-slate-400">
              ¿Pruebas en local? Usa:<br/>
              <span className="font-semibold text-slate-600">doctor@cardio.fit</span> con contraseña <span className="font-semibold text-slate-600">clinicalcdss2026</span>
            </p>
          </div>
        </div>

      </div>
    </main>
  );
}
