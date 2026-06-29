import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getRapporto } from '../lib/supabase'

const C = { header: '#1E3A5F', accent: '#2563EB', muted: '#64748B', border: '#E2E8F0' }

function Riga({ label, value }) {
  if (!value && value !== 0) return null
  return (
    <div style={{ display: 'flex', borderBottom: '1px solid #E2E8F0', padding: '4px 0', fontSize: 12 }}>
      <span style={{ minWidth: 160, fontWeight: 600, color: '#64748B', flexShrink: 0 }}>{label}</span>
      <span style={{ color: '#1E293B' }}>{value}</span>
    </div>
  )
}

function Sezione({ title, children }) {
  return (
    <div style={{ marginBottom: 16, breakInside: 'avoid' }}>
      <div style={{ background: '#1E3A5F', color: '#fff', fontWeight: 700, fontSize: 12, padding: '5px 10px', borderRadius: '4px 4px 0 0' }}>
        {title}
      </div>
      <div style={{ border: '1px solid #E2E8F0', borderTop: 'none', padding: '8px 10px', borderRadius: '0 0 4px 4px' }}>
        {children}
      </div>
    </div>
  )
}

export default function Anteprima() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [d, setD] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getRapporto(id).then(({ data: r }) => { setD(r); setLoading(false) })
  }, [id])

  if (loading) return <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: C.muted }}>Caricamento...</div>
  if (!d) return <div style={{ padding: 40, textAlign: 'center', color: '#DC2626' }}>Rapporto non trovato</div>

  const fmt = (gg, mm, aa) => gg && mm && aa ? `${gg}/${mm}/${aa}` : ''

  return (
    <div style={{ minHeight: '100vh', background: '#374151', fontFamily: "'Inter', system-ui, sans-serif" }}>

      {/* Header */}
      <div className="no-print" style={{ background: C.header, padding: '12px 16px', display: 'flex', alignItems: 'center', gap: 12, position: 'sticky', top: 0, zIndex: 100, boxShadow: '0 2px 8px rgba(0,0,0,0.3)' }}>
        <button onClick={() => navigate(`/rapporto/${id}`)} style={{ background: 'none', border: 'none', color: '#93C5FD', fontSize: 22, cursor: 'pointer' }}>←</button>
        <div style={{ flex: 1, color: '#fff', fontWeight: 700, fontSize: 14 }}>Anteprima PDF — RIS N° {d.ris_numero}</div>
        <button onClick={() => window.print()} style={{ background: '#16A34A', color: '#fff', border: 'none', borderRadius: 8, padding: '8px 16px', fontWeight: 700, fontSize: 13, cursor: 'pointer' }}>🖨 Stampa</button>
      </div>

      {/* Documento */}
      <div style={{ padding: 16 }}>
        <div id="print-area" style={{ background: '#fff', borderRadius: 8, padding: '24px 28px', boxShadow: '0 4px 20px rgba(0,0,0,0.4)', maxWidth: 750, margin: '0 auto' }}>

          {/* Intestazione */}
          <div style={{ textAlign: 'center', marginBottom: 20, borderBottom: '2px solid #1E3A5F', paddingBottom: 12 }}>
            <div style={{ fontWeight: 800, fontSize: 16, color: '#1E3A5F' }}>POLIZIA LOCALE — NAPOLI</div>
            <div style={{ fontWeight: 700, fontSize: 14, marginTop: 4 }}>RAPPORTO INCIDENTE STRADALE</div>
            <div style={{ fontSize: 12, color: C.muted, marginTop: 4 }}>
              RIS N° <strong>{d.ris_numero || '—'}</strong> &nbsp;|&nbsp; Prot. N° <strong>{d.prot_numero || '—'}</strong> &nbsp;|&nbsp; U.O. <strong>{d.uo || '—'}</strong>
            </div>
          </div>

          <Sezione title="DATI INCIDENTE">
            <Riga label="Data incidente" value={fmt(d.data_gg, d.data_mm, d.data_aa)} />
            <Riga label="Ora incidente" value={d.ora_hh && `${d.ora_hh}:${d.ora_mm}`} />
            <Riga label="Luogo" value={d.luogo} />
            <Riga label="Civico" value={d.civico} />
            <Riga label="Intersezione con" value={d.intersezione} />
            <Riga label="In corrispondenza di" value={d.corrispondenza} />
            <Riga label="Tipologia" value={[d.tip_solo_danni && 'Solo danni', d.tip_feriti && 'Con feriti', d.tip_mortale && 'Mortale', d.tip_omissione && 'Omissione soccorso'].filter(Boolean).join(', ')} />
          </Sezione>

          <Sezione title="AGENTI ACCERTATORI">
            {(d.agenti || []).map((a, i) => (
              <Riga key={i} label={`Agente ${i + 1}`} value={[a.grado, a.cognome, a.nome, a.matricola ? `matr. ${a.matricola}` : ''].filter(Boolean).join(' ')} />
            ))}
          </Sezione>

          <Sezione title="DATI INTERVENTO (PAG. 2)">
            <Riga label="Data" value={d.p2_data} />
            <Riga label="Giorno" value={d.p2_giorno} />
            <Riga label="Ore" value={d.p2_ore} />
            <Riga label="Festivo" value={d.p2_festivo ? 'Sì' : null} />
            <Riga label="Agenti rilevatori" value={d.p2_agenti_rilevatori} />
            <Riga label="Effettuato in Via" value={d.effettuato_in} />
            <Riga label="Impianto semaforico" value={d.semaforico} />
            <Riga label="Anomalie semaforico" value={d.semaforico_anomalie} />
          </Sezione>

          <Sezione title="ORARI INTERVENTO">
            <Riga label="Segnalato da" value={d.segnalato_da} />
            <Riga label="Ora segnalazione" value={d.ora_segn_hhmm} />
            <Riga label="Data segnalazione" value={d.data_segn} />
            <Riga label="Ora arrivo" value={d.ora_arrivo_hhmm} />
            <Riga label="Data arrivo" value={d.data_arrivo} />
            <Riga label="Ora incidente (presunta)" value={d.ora_inc_hhmm} />
            <Riga label="Data incidente" value={d.data_inc} />
            <Riga label="Note" value={d.note_intervento} />
          </Sezione>

          <Sezione title="PRIMO INTERVENTO">
            {d.pi_ambulanza && <Riga label="Ambulanza 118" value={[d.pi_ambulanza_post, d.pi_ambulanza_targa].filter(Boolean).join(' — ')} />}
            {d.pi_medico && <Riga label="Medico Legale" value={[d.pi_medico_uff, d.pi_medico_targa].filter(Boolean).join(' — ')} />}
            {d.pi_pol_locale && <Riga label="Polizia Locale" value={[d.pi_pol_locale_uo, d.pi_pol_locale_targa].filter(Boolean).join(' — ')} />}
            {d.pi_pol_stato && <Riga label="Polizia di Stato" value={[d.pi_pol_stato_uff, d.pi_pol_stato_targa].filter(Boolean).join(' — ')} />}
            {d.pi_carabinieri && <Riga label="Carabinieri" value={[d.pi_carabinieri_uff, d.pi_carabinieri_targa].filter(Boolean).join(' — ')} />}
            <Riga label="Successivamente" value={d.succ_intervenivano} />
          </Sezione>

          <Sezione title="NATURA DELL'INCIDENTE">
            {(d.natura || []).map((n, i) => <Riga key={i} label={`Natura ${i + 1}`} value={n} />)}
            <Riga label="Altro" value={d.natura_altro} />
            <Riga label="Punto d'urto" value={d.pos_urto_descr} />
            <Riga label="Posizione statica veicoli" value={d.pos_statica_descr} />
          </Sezione>

          <Sezione title="ACCERTAMENTI PSICO-FISICI">
            {['A', 'B', 'C', 'D'].map(k => {
              const p = (d.psico || {})[k] || {}
              if (!p.etil && !p.narco) return null
              return (
                <div key={k}>
                  <Riga label={`Veicolo ${k} — Etilometro`} value={[p.etil, p.etil_esito].filter(Boolean).join(' → ')} />
                  <Riga label={`Veicolo ${k} — Narcotest`} value={[p.narco, p.narco_esito].filter(Boolean).join(' → ')} />
                </div>
              )
            })}
          </Sezione>

          {d.decessi && (
            <Sezione title="DECESSI">
              <Riga label="N° deceduti" value={d.num_decedute} />
              <Riga label="Dove" value={d.deceduti_dove} />
              <Riga label="P.M. notiziato" value={d.pm_notiziato ? 'Sì' : null} />
              <Riga label="P.M." value={d.pm_nome} />
            </Sezione>
          )}

          <Sezione title="STRADA">
            <Riga label="Direzione DA" value={d.direzione_da} />
            <Riga label="Direzione A" value={d.direzione_a} />
            <Riga label="Classificazione" value={d.strada_localiz} />
            <Riga label="Carreggiata" value={d.strada_senso} />
            <Riga label="Pavimentazione" value={d.strada_pav} />
            <Riga label="Meteo" value={d.meteo} />
            <Riga label="Visibilità" value={d.visibilita} />
            <Riga label="Illuminazione" value={d.illuminazione} />
            <Riga label="Traffico" value={d.traffico} />
            <Riga label="Segnaletica" value={d.segnaletica} />
            <Riga label="Descrizione località" value={d.descr_localita} />
          </Sezione>

          {(d.veicoli || []).map((v, i) => (
            <Sezione key={i} title={`VEICOLO ${v.label}`}>
              <Riga label="Stato" value={v.stato} />
              <Riga label="Marca/Modello" value={[v.marca, v.modello].filter(Boolean).join(' ')} />
              <Riga label="Targa" value={v.targa} />
              <Riga label="Colore" value={v.colore} />
              <Riga label="Anno imm." value={v.anno_imm} />
              <Riga label="Alimentazione" value={v.alimentazione} />
              <Riga label="Cilindrata" value={v.cilindrata} />
              <Riga label="Telaio" value={v.telaio} />
              <Riga label="Proprietario" value={v.prop_nome} />
              <Riga label="Prop. nato il" value={v.prop_nato} />
              <Riga label="Prop. residenza" value={v.prop_res} />
              <Riga label="Conducente" value={v.cond_nome} />
              <Riga label="Cond. nato il" value={v.cond_nato} />
              <Riga label="Cond. nat. a" value={v.cond_nat_a} />
              <Riga label="Cond. residenza" value={v.cond_res} />
              <Riga label="Patente n°" value={v.pat_n} />
              <Riga label="Categoria" value={v.pat_cat} />
              <Riga label="Scadenza" value={v.pat_scad} />
              <Riga label="C.F." value={v.cf} />
              <Riga label="Recapito" value={v.recapito} />
              <Riga label="Assicurazione" value={v.assic_si ? 'Presente' : 'Assente'} />
              {v.assic_si && <>
                <Riga label="Compagnia" value={v.compagnia} />
                <Riga label="Polizza n°" value={v.polizza} />
                <Riga label="Agenzia" value={v.agenzia} />
                <Riga label="Validità" value={v.val_dal && `${v.val_dal} — ${v.val_al}`} />
              </>}
              <Riga label="Danni" value={[v.danni_ant && 'Ant.', v.danni_post && 'Post.', v.danni_dx && 'Lat.DX', v.danni_sx && 'Lat.SX'].filter(Boolean).join(', ')} />
              <Riga label="Desc. danni" value={v.danni_descr} />
              <Riga label="Destinazione" value={v.sequestrato} />
            </Sezione>
          ))}

          {(d.infortunati || []).map((inf, i) => (
            <Sezione key={i} title={`INFORTUNATO ${i + 1}`}>
              <Riga label="Ruolo" value={inf.ruolo} />
              <Riga label="Veicolo" value={inf.veicolo} />
              <Riga label="Cognome e Nome" value={[inf.cognome, inf.nome].filter(Boolean).join(' ')} />
              <Riga label="Nato il" value={inf.nato} />
              <Riga label="Nato a" value={inf.nat_a} />
              <Riga label="Residenza" value={inf.res} />
              <Riga label="C.F." value={inf.cf} />
              <Riga label="Recapito" value={inf.recapito} />
              <Riga label="Ospedale" value={inf.ospedale} />
              <Riga label="Referto n°" value={inf.referto} />
              <Riga label="Prognosi" value={inf.prognosi} />
              <Riga label="Diagnosi" value={inf.diagnosi} />
              <Riga label="Deceduto" value={inf.deceduto ? 'Sì' : null} />
              <Riga label="Prognosi riservata" value={inf.prog_riservata ? 'Sì' : null} />
            </Sezione>
          ))}

          {(d.testimoni || []).map((t, i) => (
            <Sezione key={i} title={`TESTIMONE ${i + 1}`}>
              <Riga label="Cognome e Nome" value={[t.cognome, t.nome].filter(Boolean).join(' ')} />
              <Riga label="Nato il" value={t.nato} />
              <Riga label="Residenza" value={t.res} />
              <Riga label="C.F." value={t.cf} />
              <Riga label="Recapito" value={t.recapito} />
            </Sezione>
          ))}

          <Sezione title="DINAMICA">
            <Riga label="Dinamica" value={d.dinamica} />
            <Riga label="Danni a cose" value={d.danni_cose} />
            <Riga label="Note" value={d.altre_note} />
            <Riga label="Osservazioni" value={d.osservazioni} />
          </Sezione>

          {(d.infrazioni || []).filter(i => i.articolo).map((inf, i) => (
            <Sezione key={i} title={`INFRAZIONE ${i + 1}`}>
              <Riga label="Veicolo" value={inf.veicolo} />
              <Riga label="Articolo C.d.S." value={inf.articolo} />
              <Riga label="N° verbale" value={inf.numero} />
              <Riga label="Data" value={inf.data} />
              <Riga label="Atti trasmessi a" value={inf.atti_a} />
            </Sezione>
          ))}

          <Sezione title="CHIUSURA OPERAZIONI">
            <Riga label="Data fine operazioni" value={fmt(d.op_fine_gg, d.op_fine_mm, d.op_fine_aa)} />
            <Riga label="Ora fine" value={d.op_fine_hh && `${d.op_fine_hh}:${d.op_fine_mm2}`} />
            <Riga label="Atti consegnati a" value={d.consegnato_a} />
          </Sezione>

        </div>
      </div>

      <style>{`
        @media print {
          .no-print { display: none !important; }
          body { margin: 0; background: white; }
          #print-area { box-shadow: none !important; border-radius: 0 !important; padding: 10px !important; }
        }
      `}</style>
    </div>
  )
}