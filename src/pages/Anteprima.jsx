import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getRapporto } from '../lib/storage'

const C = { header: '#1E3A5F', accent: '#2563EB', muted: '#64748B', border: '#E2E8F0' }

export default function Anteprima() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getRapporto(id).then(({ data: r }) => {
      setData(r)
      setLoading(false)
    })
  }, [id])

  if (loading) return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: C.muted }}>
      Caricamento anteprima...
    </div>
  )

  if (!data) return (
    <div style={{ padding: 40, textAlign: 'center', color: '#DC2626' }}>Rapporto non trovato</div>
  )

  return (
    <div style={{ minHeight: '100vh', background: '#374151', fontFamily: "'Inter', system-ui, sans-serif" }}>

      {/* Header */}
      <div style={{
        background: C.header, padding: '12px 16px', display: 'flex',
        alignItems: 'center', gap: 12, position: 'sticky', top: 0, zIndex: 100,
        boxShadow: '0 2px 8px rgba(0,0,0,0.3)'
      }}>
        <button onClick={() => navigate(`/rapporto/${id}`)} style={{
          background: 'none', border: 'none', color: '#93C5FD', fontSize: 22, cursor: 'pointer'
        }}>←</button>
        <div style={{ flex: 1, color: '#fff', fontWeight: 700, fontSize: 14 }}>
          Anteprima PDF
        </div>
        <button onClick={() => window.print()} style={{
          background: '#16A34A', color: '#fff', border: 'none', borderRadius: 8,
          padding: '8px 16px', fontWeight: 700, fontSize: 13, cursor: 'pointer'
        }}>
          🖨 Stampa
        </button>
      </div>

      {/* Info */}
      <div style={{
        background: '#1E40AF', color: '#BFDBFE', fontSize: 12,
        padding: '10px 16px', textAlign: 'center'
      }}>
        Questa è l'anteprima del modulo compilato. Verifica i dati prima di stampare.
      </div>

      {/* PDF viewer con overlay dati */}
      <div style={{ padding: 16 }}>
        <div style={{
          background: '#fff', borderRadius: 8, padding: 20,
          boxShadow: '0 4px 20px rgba(0,0,0,0.4)', maxWidth: 700, margin: '0 auto'
        }}>
          {/* Messaggio temporaneo - verrà sostituito con PDF reale */}
          <div style={{ textAlign: 'center', padding: '40px 20px', color: C.muted }}>
            <div style={{ fontSize: 48, marginBottom: 16 }}>📄</div>
            <div style={{ fontWeight: 700, fontSize: 16, color: '#1E293B', marginBottom: 8 }}>
              Anteprima PDF in costruzione
            </div>
            <div style={{ fontSize: 13, marginBottom: 24 }}>
              Il PDF del modulo RIS con i dati compilati verrà mostrato qui.<br/>
              Per ora puoi vedere il riepilogo dei dati inseriti.
            </div>

            {/* Riepilogo dati */}
            <div style={{ textAlign: 'left', background: '#F8FAFC', borderRadius: 10, padding: 16 }}>
              <div style={{ fontWeight: 700, fontSize: 14, color: '#1E293B', marginBottom: 12 }}>
                📋 Dati inseriti
              </div>
              {[
                ['RIS N°', data.ris_numero],
                ['Data', data.data_gg && `${data.data_gg}/${data.data_mm}/${data.data_aa}`],
                ['Ora', data.ora_hh && `${data.ora_hh}:${data.ora_mm}`],
                ['Luogo', data.luogo],
                ['Tipologia', [
                  data.tip_solo_danni && 'Solo danni',
                  data.tip_feriti && 'Con feriti',
                  data.tip_mortale && 'Mortale',
                ].filter(Boolean).join(', ')],
                ['Veicoli', (data.veicoli || []).filter(v => v.targa).map(v => `${v.label}: ${v.targa}`).join(', ')],
                ['Infortunati', (data.infortunati || []).length > 0 ? `${data.infortunati.length} persona/e` : null],
                ['Natura', (data.natura || []).slice(0, 2).join(', ')],
              ].filter(([, v]) => v).map(([k, v]) => (
                <div key={k} style={{ display: 'flex', gap: 10, padding: '8px 0', borderBottom: `1px solid ${C.border}` }}>
                  <span style={{ fontSize: 12, color: C.muted, fontWeight: 600, minWidth: 100 }}>{k}</span>
                  <span style={{ fontSize: 13, color: '#1E293B' }}>{v}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <style>{`
        @media print {
          body { margin: 0; background: white; }
          button { display: none !important; }
        }
      `}</style>
    </div>
  )
}
