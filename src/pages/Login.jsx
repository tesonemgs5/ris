import { useState } from 'react'
import { signIn } from '../lib/storage'

const C = { bg: '#1E3A5F', accent: '#2563EB', error: '#DC2626' }

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleLogin() {
    if (!email || !password) { setError('Inserisci email e password'); return }
    setLoading(true); setError('')
    const { error: err } = await signIn(email, password)
    if (err) setError('Credenziali non valide')
    setLoading(false)
  }

  return (
    <div style={{
      minHeight: '100vh', background: C.bg,
      display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      padding: 24, fontFamily: "'Inter', system-ui, sans-serif"
    }}>
      <div style={{ fontSize: 56, marginBottom: 12 }}>🚔</div>
      <div style={{ color: '#fff', fontWeight: 800, fontSize: 22, marginBottom: 4 }}>
        Polizia Locale Napoli
      </div>
      <div style={{ color: '#93C5FD', fontSize: 13, marginBottom: 40 }}>
        Rapporto Incidente Stradale
      </div>

      <div style={{
        background: '#fff', borderRadius: 16, padding: 28,
        width: '100%', maxWidth: 360, boxShadow: '0 8px 32px rgba(0,0,0,0.3)'
      }}>
        <div style={{ fontSize: 16, fontWeight: 700, color: C.bg, marginBottom: 20 }}>
          Accesso
        </div>

        <div style={{ marginBottom: 14 }}>
          <label style={{ fontSize: 12, fontWeight: 600, color: '#64748B', display: 'block', marginBottom: 6 }}>
            EMAIL
          </label>
          <input
            type="email" value={email}
            onChange={e => setEmail(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleLogin()}
            placeholder="agente@polizialocale.napoli.it"
            style={{
              width: '100%', border: '1.5px solid #CBD5E1', borderRadius: 8,
              padding: '12px 14px', fontSize: 14, boxSizing: 'border-box', outline: 'none'
            }}
          />
        </div>

        <div style={{ marginBottom: 20 }}>
          <label style={{ fontSize: 12, fontWeight: 600, color: '#64748B', display: 'block', marginBottom: 6 }}>
            PASSWORD
          </label>
          <input
            type="password" value={password}
            onChange={e => setPassword(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleLogin()}
            placeholder="••••••••"
            style={{
              width: '100%', border: '1.5px solid #CBD5E1', borderRadius: 8,
              padding: '12px 14px', fontSize: 14, boxSizing: 'border-box', outline: 'none'
            }}
          />
        </div>

        {error && (
          <div style={{
            background: '#FEF2F2', color: C.error, borderRadius: 8,
            padding: '10px 14px', fontSize: 13, marginBottom: 16
          }}>{error}</div>
        )}

        <button
          onClick={handleLogin} disabled={loading}
          style={{
            width: '100%', background: C.bg, color: '#fff', border: 'none',
            borderRadius: 10, padding: '14px', fontWeight: 700, fontSize: 15,
            cursor: loading ? 'default' : 'pointer', opacity: loading ? 0.7 : 1
          }}
        >
          {loading ? 'Accesso in corso...' : 'Accedi'}
        </button>
      </div>

      <div style={{ color: '#475569', fontSize: 12, marginTop: 32, textAlign: 'center' }}>
        Uso riservato al personale autorizzato<br />
        Polizia Locale — Comune di Napoli
      </div>
    </div>
  )
}
