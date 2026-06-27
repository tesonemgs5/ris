import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { getRapporti, createRapporto, exportBackup, importBackup, deleteRapporto } from '../lib/supabase'

const C = { bg: '#F1F5F9', header: '#1E3A5F', accent: '#2563EB', muted: '#64748B', border: '#E2E8F0', success: '#16A34A', danger: '#DC2626' }

export default function Dashboard() {
  const [rapporti, setRapporti] = useState([])
  const [loading, setLoading] = useState(true)
  const [msg, setMsg] = useState('')
  const navigate = useNavigate()
  const fileInputRef = useRef(null)

  useEffect(() => {
    loadRapporti()
  }, [])

  async function loadRapporti() {
    setLoading(true)
    const { data } = await getRapporti()
    setRapporti(data || [])
    setLoading(false)
  }

  async function nuovoRapporto() {
    const { data } = await createRapporto({
      stato: 'bozza',
      data_aa: new Date().getFullYear().toString(),
      data_mm: String(new Date().getMonth() + 1).padStart(2, '0'),
      data_gg: String(new Date().getDate()).padStart(2, '0'),
      veicoli: [{ label: 'A' }, { label: 'B' }],
      agenti: [],
      infortunati: [],
      testimoni: [],
      infrazioni: []
    })
    if (data) navigate(`/rapporto/${data.id}`)
  }

  async function handleDelete(e, id) {
    e.stopPropagation()
    if (!confirm('Eliminare questo rapporto? L\'azione non si può annullare.')) return
    await deleteRapporto(id)
    loadRapporti()
  }

  async function handleImport(e) {
    const file = e.target.files[0]
    if (!file) return
    try {
      const count = await importBackup(file)
      setMsg(`✅ Backup ripristinato — ${count} rapporti totali`)
      loadRapporti()
    } catch {
      setMsg('⚠️ File di backup non valido')
    }
    setTimeout(() => setMsg(''), 3000)
    e.target.value = ''
  }

  const statoColor = { bozza: '#F59E0B', completato: '#16A34A', archiviato: '#94A3B8' }
  const statoLabel = { bozza: 'Bozza', completato: 'Completato', archiviato: 'Archiviato' }

  return (
    <div style={{ minHeight: '100vh', background: C.bg, fontFamily: "'Inter', system-ui, sans-serif" }}>
      {/* Header */}
      <div style={{
        background: C.header, padding: '14px 16px',
        display: 'flex', alignItems: 'center', gap: 12,
        boxShadow: '0 2px 8px rgba(0,0,0,0.2)'
      }}>
        <span style={{ fontSize: 22 }}>🚔</span>
        <div style={{ flex: 1 }}>
          <div style={{ color: '#fff', fontWeight: 800, fontSize: 15 }}>RIS Napoli</div>
          <div style={{ color: '#93C5FD', fontSize: 11 }}>💾 Salvataggio locale su questo PC</div>
        </div>
      </div>

      {/* Content */}
      <div style={{ padding: 16, maxWidth: 600, margin: '0 auto' }}>
        {/* Nuovo rapporto */}
        <button onClick={nuovoRapporto} style={{
          width: '100%', background: C.accent, color: '#fff', border: 'none',
          borderRadius: 14, padding: '18px', fontWeight: 700, fontSize: 16,
          cursor: 'pointer', marginBottom: 16,
          display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10,
          boxShadow: '0 4px 12px rgba(37,99,235,0.4)'
        }}>
          <span style={{ fontSize: 22 }}>📋</span>
          Nuovo Rapporto Incidente
        </button>

        {/* Backup / Ripristino */}
        <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
          <button onClick={exportBackup} style={{
            flex: 1, background: '#fff', border: `1.5px solid ${C.border}`, color: '#334155',
            borderRadius: 10, padding: '10px', fontWeight: 600, fontSize: 13, cursor: 'pointer'
          }}>
            💾 Esporta backup
          </button>
          <button onClick={() => fileInputRef.current?.click()} style={{
            flex: 1, background: '#fff', border: `1.5px solid ${C.border}`, color: '#334155',
            borderRadius: 10, padding: '10px', fontWeight: 600, fontSize: 13, cursor: 'pointer'
          }}>
            📥 Importa backup
          </button>
          <input ref={fileInputRef} type="file" accept="application/json" onChange={handleImport} style={{ display: 'none' }} />
        </div>

        {msg && (
          <div style={{
            background: msg.startsWith('✅') ? '#F0FDF4' : '#FEF2F2',
            color: msg.startsWith('✅') ? C.success : C.danger,
            borderRadius: 8, padding: '10px 14px', fontSize: 13, marginBottom: 16
          }}>{msg}</div>
        )}

        {/* Lista rapporti */}
        <div style={{ fontSize: 12, fontWeight: 700, color: C.muted, marginBottom: 10, textTransform: 'uppercase' }}>
          Rapporti recenti
        </div>

        {loading && (
          <div style={{ textAlign: 'center', padding: 40, color: C.muted }}>Caricamento...</div>
        )}

        {!loading && rapporti.length === 0 && (
          <div style={{
            textAlign: 'center', padding: 48, color: C.muted,
            background: '#fff', borderRadius: 14, border: `1px solid ${C.border}`
          }}>
            <div style={{ fontSize: 40, marginBottom: 12 }}>📄</div>
            <div style={{ fontWeight: 600, marginBottom: 6 }}>Nessun rapporto</div>
            <div style={{ fontSize: 13 }}>Premi "Nuovo Rapporto Incidente" per iniziare</div>
          </div>
        )}

        {rapporti.map(r => (
          <div key={r.id}
            onClick={() => navigate(`/rapporto/${r.id}`)}
            style={{
              background: '#fff', borderRadius: 12, padding: '14px 16px',
              marginBottom: 10, cursor: 'pointer', border: `1px solid ${C.border}`,
              display: 'flex', alignItems: 'center', gap: 14,
              boxShadow: '0 1px 4px rgba(0,0,0,0.06)'
            }}>
            <div style={{
              width: 44, height: 44, borderRadius: 10,
              background: '#EFF6FF', display: 'flex', alignItems: 'center',
              justifyContent: 'center', fontSize: 20, flexShrink: 0
            }}>📋</div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontWeight: 700, fontSize: 14, color: '#1E293B' }}>
                {r.ris_numero || 'RIS senza numero'}
              </div>
              <div style={{ fontSize: 12, color: C.muted, marginTop: 2 }}>
                {r.data_gg && r.data_mm && r.data_aa
                  ? `${r.data_gg}/${r.data_mm}/${r.data_aa}`
                  : 'Data non inserita'}
                {r.luogo ? ` · ${r.luogo}` : ''}
              </div>
            </div>
            <div style={{
              fontSize: 11, fontWeight: 700, color: statoColor[r.stato],
              background: `${statoColor[r.stato]}18`,
              padding: '3px 10px', borderRadius: 20
            }}>
              {statoLabel[r.stato]}
            </div>
            <button onClick={(e) => handleDelete(e, r.id)} style={{
              background: 'none', border: 'none', color: C.danger, fontSize: 16,
              cursor: 'pointer', padding: 4, flexShrink: 0
            }}>🗑</button>
          </div>
        ))}
      </div>
    </div>
  )
}
