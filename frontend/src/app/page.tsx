'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // Redireccionar automáticamente al Login del CDSS al entrar al portal
    router.push('/login');
  }, [router]);

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center font-sans">
      <div className="text-center space-y-3">
        <div className="w-12 h-12 rounded-full border-4 border-slate-900 border-t-transparent animate-spin mx-auto" />
        <p className="text-slate-500 text-sm font-semibold">Redireccionando al portal médico...</p>
      </div>
    </div>
  );
}
