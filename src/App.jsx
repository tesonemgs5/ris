import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { supabase } from './lib/storage'
import Dashboard from './pages/Dashboard'
import Rapporto from './pages/Rapporto'
import Anteprima from './pages/Anteprima'

export default function App() {
  const [ready, setReady] = useState(false)

  useEffect(() => {
    // In modalità locale la sessione è sempre attiva, aspettiamo solo il mount
    supabase.auth.getSession().then(() => setReady(true))
  }, [])

  if (!ready) return <Splash />

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/rapporto/:id" element={<Rapporto />} />
        <Route path="/rapporto/:id/anteprima" element={<Anteprima />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}

function Splash() {
  return (
    <div style={{
      minHeight: '100vh', display: 'flex', flexDirection: 'column',
      alignItems: 'center', justifyContent: 'center',
      background: '#1E3A5F', gap: 16
    }}>
      <div style={{ fontSize: 48 }}>🚔</div>
      <div style={{ color: '#fff', fontWeight: 700, fontSize: 18 }}>RIS Napoli</div>
      <div style={{ color: '#93C5FD', fontSize: 13 }}>Caricamento...</div>
    </div>
  )
}
