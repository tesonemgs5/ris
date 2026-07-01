output = """import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getRapporto } from '../lib/storage'

const S = {
  page: { background: '#fff', width: '210mm', margin: '0 auto', padding: '12mm 14mm', boxSizing: 'border-box', fontFamily: 'Arial, sans-serif', fontSize: 11, color: '#000', pageBreakAfter: 'always', breakAfter: 'page', position: 'relative' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8, borderBottom: '2px solid #000', paddingBottom: 6 },
  title: { fontSize: 18, fontWeight: 'bold', textAlign: 'center', border: '2px solid #000', padding: '6px 20px', marginBottom: 10 },
  label: { fontSize: 9, fontWeight: 'bold', textTransform: 'uppercase', color: '#333' },
  line: { borderBottom: '1px solid #000', minHeight: 16, marginBottom: 2, paddingLeft: 2 },
  box: { border: '1px solid #000', padding: '4px 6px', marginBottom: 6 },
  table: { width: '100%', borderCollapse: 'collapse', marginBottom: 8, breakInside: 'avoid' },
  td: { border: '1px solid #000', padding: '3px 5px', fontSize: 10 },
  th: { border: '1px solid #000', padding: '3px 5px', fontSize: 10, fontWeight: 'bold', background: '#f0f0f0', textAlign: 'center' },
  chk: (v) => ({ display: 'inline-block', width: 10, height: 10, border: '1px solid #000', background: v ? '#000' : '#fff', marginRight: 3, verticalAlign: 'middle', flexShrink: 0 }),
  sez: { fontWeight: 'bold', fontSize: 11, borderBottom: '1px solid #000', marginBottom: 6, marginTop: 10, textTransform: 'uppercase' },
  row: { display: 'flex', gap: 8, marginBottom: 4 },
  firma: { marginTop: 16, textAlign: 'right', fontSize: 10 },
}

function Chk({ v }) { return <span style={S.chk(v)} /> }
function Ln({ label, value, flex }) { return <div style={{ flex: flex || 1 }}><div style={S.label}>{label}</div><div style={S.line}>{value || ''}</div></div> }
function PageNum({ n, tot, ris }) {
  return <div style={{ fontSize: 9, textAlign: 'right', color: '#555', marginBottom: 4 }}>
    RIS n. {ris || '___'} &nbsp; pag. {n} di {tot} &nbsp; ver.1124.1
  </div>
}
function Firme() {
  return <div style={S.firma}>
    Uff./Ag. di P.G.<br />
    ………………………………..<br />
    ………………………………..<br />
    ………………………………..<br />
    ………………………………..
  </div>
}

const TUTTE_LE_PAGINE = [
  { id: 'p1', label: 'Pag. 1 — Intestazione' },
  { id: 'p2', label: 'Pag. 2 — Intervento' },
  { id: 'p3', label: 'Pag. 3 — Natura' },
  { id: 'p4', label: 'Pag. 4 — Decessi / Psico' },
  { id: 'p5', label: 'Pag. 5 — Strada' },
  { id: 'veicoli', label: 'Veicoli (una per veicolo)' },
  { id: 'infortunati', label: 'Infortunati' },
  { id: 'testimoni', label: 'Testimoni' },
  { id: 'dinamica', label: 'Dinamica' },
  { id: 'infrazioni', label: 'Infrazioni' },
  { id: 'chiusura', label: 'Chiusura' },
]

export default function Anteprima() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [d, setD] = useState(null)
  const [loading, setLoading] = useState(true)
  const [pagineAttive, setPagineAttive] = useState(() => {
    const tutte = {}
    TUTTE_LE_PAGINE.forEach(p => { tutte[p.id] = true })
    return tutte
  })
  const [panelOpen, setPanelOpen] = useState(false)

  useEffect(() => {
    getRapporto(id).then(({ data: r }) => { setD(r); setLoading(false) })
  }, [id])

  if (loading) return <div style={{ padding: 40, textAlign: 'center' }}>Caricamento...</div>
  if (!d) return <div style={{ padding: 40, color: 'red' }}>Rapporto non trovato</div>

  const veicoli = d.veicoli || []
  const infortunati = d.infortunati || []
  const testimoni = d.testimoni || []
  const natura = d.natura || []
  const infrazioni = d.infrazioni || []
  const psico = d.psico || {}

  const pagineTotali = TUTTE_LE_PAGINE.filter(p => pagineAttive[p.id]).length
    + (pagineAttive['veicoli'] ? Math.max(0, veicoli.length - 1) : 0)

  function togglePagina(id) {
    setPagineAttive(prev => ({ ...prev, [id]: !prev[id] }))
  }

  return (
    <div style={{ background: '#374151', minHeight: '100vh', fontFamily: 'Arial, sans-serif' }}>

      {/* Toolbar */}
      <div className="no-print" style={{ background: '#1E3A5F', padding: '12px 16px', display: 'flex', alignItems: 'center', gap: 12, position: 'sticky', top: 0, zIndex: 100 }}>
        <button onClick={() => navigate(`/rapporto/${id}`)} style={{ background: 'none', border: 'none', color: '#93C5FD', fontSize: 22, cursor: 'pointer' }}>←</button>
        <div style={{ flex: 1, color: '#fff', fontWeight: 700, fontSize: 14 }}>Anteprima — RIS N° {d.ris_numero}</div>
        <button onClick={() => setPanelOpen(o => !o)} style={{ background: '#fff2', border: '1px solid #ffffff40', color: '#fff', borderRadius: 8, padding: '6px 12px', fontWeight: 600, fontSize: 12, cursor: 'pointer' }}>📄 Pagine</button>
        <button onClick={() => window.print()} style={{ background: '#16A34A', color: '#fff', border: 'none', borderRadius: 8, padding: '8px 18px', fontWeight: 700, fontSize: 13, cursor: 'pointer' }}>🖨 Stampa</button>
      </div>

      {/* Pannello selezione pagine */}
      {panelOpen && (
        <div className="no-print" style={{ background: '#1e293b', padding: '14px 16px', borderBottom: '1px solid #334155' }}>
          <div style={{ color: '#93C5FD', fontWeight: 700, fontSize: 12, marginBottom: 10 }}>SELEZIONA PAGINE DA STAMPARE</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: 8 }}>
            {TUTTE_LE_PAGINE.map(p => (
              <label key={p.id} style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer', color: pagineAttive[p.id] ? '#fff' : '#64748b', fontSize: 12 }}>
                <input type="checkbox" checked={!!pagineAttive[p.id]} onChange={() => togglePagina(p.id)} style={{ accentColor: '#2563EB' }} />
                {p.label}
              </label>
            ))}
          </div>
          <div style={{ marginTop: 10, display: 'flex', gap: 8 }}>
            <button onClick={() => { const t = {}; TUTTE_LE_PAGINE.forEach(p => { t[p.id] = true }); setPagineAttive(t) }} style={{ fontSize: 11, color: '#93C5FD', background: 'none', border: '1px solid #93C5FD', borderRadius: 6, padding: '4px 10px', cursor: 'pointer' }}>Tutte</button>
            <button onClick={() => { const t = {}; TUTTE_LE_PAGINE.forEach(p => { t[p.id] = false }); setPagineAttive(t) }} style={{ fontSize: 11, color: '#f87171', background: 'none', border: '1px solid #f87171', borderRadius: 6, padding: '4px 10px', cursor: 'pointer' }}>Nessuna</button>
          </div>
        </div>
      )}

      <div id="print-wrap" className="print-wrap-outer" style={{ padding: 16 }}>

        {/* PAG 1 */}
        {pagineAttive['p1'] && (
          <div style={S.page}>
            <PageNum n={1} tot={pagineTotali} ris={d.ris_numero} />
            <div style={S.header}>
              <div>
                <div style={{ fontWeight: 'bold', fontSize: 11 }}>COMUNE DI NAPOLI</div>
                <div style={{ fontWeight: 'bold' }}>AREA SICUREZZA POLIZIA LOCALE</div>
                <div style={{ fontWeight: 'bold' }}>SERVIZIO COORDINAMENTO STRATEGICO OPERATIVO</div>
              </div>
              <div style={{ border: '2px solid #000', padding: '4px 12px', minWidth: 200 }}>
                <div style={{ fontWeight: 'bold', fontSize: 14 }}>RIS <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 120 }}>{d.ris_numero}</span></div>
                <div style={{ marginTop: 4 }}>PROT. N° <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 120 }}>{d.prot_numero}</span></div>
              </div>
            </div>
            <div style={{ marginBottom: 6 }}>U.O. <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 200 }}>{d.uo}</span></div>
            <div style={S.title}>RAPPORTO INCIDENTE STRADALE</div>
            <div style={{ marginBottom: 8 }}>
              del <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 30 }}>{d.data_gg}</span> /
              <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 30 }}>{d.data_mm}</span> /
              <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 50 }}>{d.data_aa}</span>
              &nbsp;- ore <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 25 }}>{d.ora_hh}</span>:<span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 25 }}>{d.ora_mm}</span>
              &nbsp;- avvenuto in Napoli
            </div>
            <div style={{ ...S.line, marginBottom: 8, minHeight: 20 }}>{d.luogo}</div>
            <div style={{ textAlign: 'center', fontWeight: 'bold', marginBottom: 6 }}>(SPECIFICARE LA PRIMA LOCALITÀ)</div>
            <div style={{ marginBottom: 4 }}><Chk v={!!d.civico} /> in prossimità &nbsp;<Chk v={!!d.civico} /> del civico <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 30 }}>{d.civico}</span></div>
            <div style={{ marginBottom: 4 }}><Chk v={!!d.intersezione} /> all'intersezione con <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 300 }}>{d.intersezione}</span></div>
            <div style={{ marginBottom: 8 }}>□ in corrispondenza <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 320 }}>{d.corrispondenza}</span></div>
            <div style={S.row}>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 'bold', marginBottom: 4 }}>TIPOLOGIA SINISTRO</div>
                <div><Chk v={d.tip_solo_danni} /> solo danni a cose</div>
                <div><Chk v={d.tip_feriti} /> con feriti</div>
                <div><Chk v={d.tip_mortale} /> mortale</div>
                <div><Chk v={d.tip_omissione} /> omissione di soccorso</div>
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontWeight: 'bold', marginBottom: 4 }}>RIEPILOGO ATTIVITA'</div>
                <div><Chk v={d.att_rilievi_desc} /> rilievi descrittivi</div>
                <div><Chk v={d.att_rilievi_plan} /> rilievi planimetrici</div>
                <div><Chk v={d.att_rilievi_foto} /> rilievi fotografici</div>
                <div><Chk v={d.att_seq_penale || d.att_seq_amm} /> sequestro <Chk v={d.att_seq_penale} /> penale <Chk v={d.att_seq_amm} /> amm.vo</div>
              </div>
            </div>
            <table style={S.table}>
              <thead><tr><th style={S.th}>VEICOLI</th><th style={S.th}>CONDUCENTE</th><th style={S.th}>PEDONE</th><th style={S.th}>TARGA</th></tr></thead>
              <tbody>
                {['A','B','C','D'].map((l, i) => {
                  const vA = veicoli.find(v => v.label === l)
                  return <tr key={l}><td style={S.td}><Chk v={!!vA} /> {l}</td><td style={S.td}>{vA?.cond_nome || ''}</td><td style={S.td}></td><td style={S.td}>{vA?.targa || ''}</td></tr>
                })}
              </tbody>
            </table>
            <div style={{ fontWeight: 'bold', textAlign: 'center', marginBottom: 4 }}>AGENTI ACCERTATORI</div>
            <table style={S.table}>
              <thead><tr><th style={S.th}>GRADO</th><th style={S.th}>COGNOME</th><th style={S.th}>NOME</th><th style={S.th}>MATRICOLA</th></tr></thead>
              <tbody>
                {[0,1,2,3].map(i => { const ag = (d.agenti || [])[i] || {}; return <tr key={i}><td style={S.td}>{ag.grado || ''}</td><td style={S.td}>{ag.cognome || ''}</td><td style={S.td}>{ag.nome || ''}</td><td style={S.td}>{ag.matricola || ''}</td></tr> })}
              </tbody>
            </table>
            <Firme />
          </div>
        )}

        {/* PAG 2 */}
        {pagineAttive['p2'] && (
          <div style={S.page}>
            <PageNum n={2} tot={pagineTotali} ris={d.ris_numero} />
            <div style={{ marginBottom: 6 }}>Data: <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 120 }}>{d.p2_data}</span> &nbsp; giorno: <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 80 }}>{d.p2_giorno}</span> &nbsp; ore: <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 50 }}>{d.p2_ore}</span> &nbsp; <Chk v={d.p2_festivo} /> festivo; <Chk v={!d.p2_festivo} /> non festivo</div>
            <div style={{ marginBottom: 6 }}>Ufficiali/Agenti di P.G. rilevatori: <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 300 }}>{d.p2_agenti_rilevatori}</span></div>
            <div style={S.sez}>NOTIZIE INTERVENTO</div>
            <div style={{ marginBottom: 6 }}>Effettuato in Via <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 350 }}>{d.effettuato_in}</span></div>
            <div style={{ marginBottom: 6 }}>IMPIANTO SEMAFORICO &nbsp;<Chk v={d.semaforico === 'Funzionante'} /> Funzionante &nbsp;<Chk v={d.semaforico === 'Giallo intermittente'} /> Giallo intermittente &nbsp;<Chk v={d.semaforico === 'Spento'} /> Spento</div>
            <div style={{ marginBottom: 8 }}>Anomalie: <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 250 }}>{d.semaforico_anomalie}</span></div>
            <div style={{ marginBottom: 6 }}>Intervento segnalato da <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 300 }}>{d.segnalato_da}</span></div>
            <div style={{ marginBottom: 4 }}>Orario segnalazione/chiamata: alle ore <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 40 }}>{d.ora_segn_hhmm}</span> del <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 80 }}>{d.data_segn}</span></div>
            <div style={{ marginBottom: 4 }}>Orario arrivo sul posto: alle ore <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 40 }}>{d.ora_arrivo_hhmm}</span> del <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 80 }}>{d.data_arrivo}</span></div>
            <div style={{ marginBottom: 8 }}>Orario presunto dell'incidente: alle ore <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 40 }}>{d.ora_inc_hhmm}</span> del <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 80 }}>{d.data_inc}</span></div>
            <div style={{ marginBottom: 8 }}>Note: <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 380 }}>{d.note_intervento}</span></div>
            <div style={{ marginBottom: 6, fontSize: 10 }}>Sul luogo del sinistro, il primo intervento veniva effettuato da:</div>
            {[{k:'pi_ambulanza',l:'Ambulanza 118',pk:'pi_ambulanza_post',pl:'Postazione',tk:'pi_ambulanza_targa'},{k:'pi_medico',l:'Medico Legale',pk:'pi_medico_uff',pl:'Ufficio',tk:'pi_medico_targa'},{k:'pi_pol_locale',l:'Polizia Locale',pk:'pi_pol_locale_uo',pl:'U.O.',tk:'pi_pol_locale_targa'},{k:'pi_pol_stato',l:'Polizia di Stato',pk:'pi_pol_stato_uff',pl:'Ufficio',tk:'pi_pol_stato_targa'},{k:'pi_carabinieri',l:'Carabinieri',pk:'pi_carabinieri_uff',pl:'Ufficio',tk:'pi_carabinieri_targa'}].map(item=>(
              <div key={item.k} style={{ marginBottom: 3 }}><Chk v={d[item.k]} /> {item.l} &nbsp; {item.pl} <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 120 }}>{d[item.pk]}</span> &nbsp; targa <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 80 }}>{d[item.tk]}</span></div>
            ))}
            <div style={{ marginTop: 8 }}>Successivamente intervenivano: <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 300 }}>{d.succ_intervenivano}</span></div>
            <Firme />
          </div>
        )}

        {/* PAG 3 — NATURA */}
        {pagineAttive['p3'] && (
          <div style={S.page}>
            <PageNum n={3} tot={pagineTotali} ris={d.ris_numero} />
            <div style={S.sez}>NATURA DELL'INCIDENTE</div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2px 16px', marginBottom: 8 }}>
              {['Scontro frontale tra veicoli in marcia','Veicolo in marcia contro veicolo fermo','Scontro frontale/laterale Dx tra veicoli in marcia','Veicolo in marcia contro veicolo in sosta','Scontro frontale/laterale Sx tra veicoli in marcia','Veicolo in marcia contro ostacolo fisso','Scontro laterale tra veicoli in marcia','Veicolo in marcia contro ostacolo accidentale','Tamponamento multiplo','Fuoriuscita dalla sede stradale','Investimento di pedone','Ribaltamento senza urto','Scontro con velocipede','Infortunio per frenata improvvisa','Veicolo in marcia contro veicolo in arresto','Infortunio per caduta dal veicolo','Veicolo in fuga',''].map((opt,i)=>opt?<div key={i}><Chk v={natura.includes(opt)} /> {opt}</div>:<div key={i}/>)}
            </div>
            <div style={{ marginBottom: 10 }}>Altro: <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 350 }}>{d.natura_altro}</span></div>
            <div style={S.sez}>LOCALIZZAZIONE DEL PUNTO D'URTO</div>
            <div style={{ minHeight: 80, borderBottom: '1px solid #000', marginBottom: 4, whiteSpace: 'pre-wrap' }}>{d.pos_urto_descr}</div>
            <div style={S.sez}>POSIZIONE STATICA DEI VEICOLI</div>
            <div style={{ minHeight: 80, borderBottom: '1px solid #000', marginBottom: 4, whiteSpace: 'pre-wrap' }}>{d.pos_statica_descr}</div>
            <Firme />
          </div>
        )}

        {/* PAG 4 — DECESSI + PSICO */}
        {pagineAttive['p4'] && (
          <div style={S.page}>
            <PageNum n={4} tot={pagineTotali} ris={d.ris_numero} />
            <div style={S.sez}>DECESSI</div>
            <div style={{ marginBottom: 6 }}><Chk v={d.decessi} /> Sì &nbsp; <Chk v={!d.decessi} /> No &nbsp; Persone decedute n. <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 30 }}>{d.num_decedute}</span></div>
            <div style={{ marginBottom: 10 }}>Notiziato il P.M. di turno <Chk v={d.pm_notiziato} /> Sì <Chk v={!d.pm_notiziato} /> No &nbsp; <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 200 }}>{d.pm_nome}</span></div>
            <div style={S.sez}>ACCERTAMENTI STATO PSICO/FISICO CONDUCENTI</div>
            {['A','B','C','D'].map((k,i)=>{const p=psico[k]||{};return(
              <div key={k} style={{ marginBottom: 10 }}>
                <div style={{ fontWeight: 'bold', marginBottom: 3 }}>Veicolo {k}</div>
                <div style={{ marginBottom: 2 }}>Etilometro <Chk v={p.etil==='Sì'}/> Sì <Chk v={p.etil==='No'}/> No &nbsp; esito <Chk v={p.etil_esito==='Positivo'}/> Positivo <Chk v={p.etil_esito==='Negativo'}/> Negativo <Chk v={p.etil==='Rifiuto'}/> Rifiuto</div>
                <div>Narcotest <Chk v={p.narco==='Sì'}/> Sì <Chk v={p.narco==='No'}/> No &nbsp; esito <Chk v={p.narco_esito==='Positivo'}/> Positivo <Chk v={p.narco_esito==='Negativo'}/> Negativo <Chk v={p.narco==='Rifiuto'}/> Rifiuto</div>
              </div>
            )})}
            <div style={S.sez}>OSSERVAZIONI E NOTE</div>
            <div style={{ minHeight: 80, borderBottom: '1px solid #000', whiteSpace: 'pre-wrap' }}>{d.osservazioni}</div>
            <Firme />
          </div>
        )}

        {/* PAG 5 — STRADA */}
        {pagineAttive['p5'] && (
          <div style={S.page}>
            <PageNum n={5} tot={pagineTotali} ris={d.ris_numero} />
            <div style={S.sez}>DESCRIZIONE DELLA STRADA</div>
            <div style={{ marginBottom: 4 }}>Direzione da <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 150 }}>{d.direzione_da}</span> &nbsp; a <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 150 }}>{d.direzione_a}</span></div>
            <div style={{ marginBottom: 6 }}>
              <div style={{ fontWeight: 'bold', marginBottom: 3 }}>1. Localizzazione:</div>
              {['Strada urbana','Strada extraurbana principale','Strada extraurbana secondaria','Itinerario ciclopedonale'].map(opt=><span key={opt}><Chk v={d.strada_localiz===opt}/> {opt} &nbsp;</span>)}
            </div>
            <div style={{ marginBottom: 6 }}>
              <div style={{ fontWeight: 'bold', marginBottom: 3 }}>2. Carreggiata:</div>
              {['Una carreggiata senso unico','Una carreggiata doppio senso','Due carreggiate','Più di due carreggiate'].map(opt=><span key={opt}><Chk v={d.strada_senso===opt}/> {opt} &nbsp;</span>)}
            </div>
            <div style={{ marginBottom: 6 }}>
              <div style={{ fontWeight: 'bold', marginBottom: 3 }}>3. Pavimentazione:</div>
              {['Asfaltata','Lastricata','In conglomerato cementizio','Acciottolata','In cubetti di porfido','Sterrata','Dissestata'].map(opt=><span key={opt}><Chk v={d.strada_pav===opt}/> {opt} &nbsp;</span>)}
            </div>
            <div style={{ marginBottom: 6 }}>
              <div style={{ fontWeight: 'bold', marginBottom: 3 }}>4. Condizioni meteorologiche:</div>
              {['Sereno','Nuvoloso','Nebbia','Pioggia in atto','Grandine','Nevicata','Vento forte','Sole radente'].map(opt=><span key={opt}><Chk v={d.meteo===opt}/> {opt} &nbsp;</span>)}
            </div>
            <div style={{ marginBottom: 6 }}>Visibilità: <Chk v={d.visibilita==='Buona'}/> Buona <Chk v={d.visibilita==='Sufficiente'}/> Sufficiente <Chk v={d.visibilita==='Insufficiente'}/> Insufficiente &nbsp;&nbsp; Illuminazione: <Chk v={d.illuminazione==='Ore diurne'}/> Ore diurne <Chk v={d.illuminazione?.includes('con illuminazione')}/> Notturne con illuminazione <Chk v={d.illuminazione?.includes('senza')}/> Notturne senza illuminazione</div>
            <div style={{ marginBottom: 6 }}>5. Traffico: <Chk v={d.traffico==='Intenso'}/> Intenso <Chk v={d.traffico==='Normale'}/> Normale <Chk v={d.traffico==='Scarso'}/> Scarso</div>
            <div style={{ marginBottom: 6 }}><div style={{ fontWeight: 'bold', marginBottom: 2 }}>6. Segnaletica:</div><div style={{ minHeight: 40, borderBottom: '1px solid #000', whiteSpace: 'pre-wrap' }}>{d.segnaletica}</div></div>
            <div><div style={{ fontWeight: 'bold', marginBottom: 2 }}>Descrizione analitica della località:</div><div style={{ minHeight: 60, borderBottom: '1px solid #000', whiteSpace: 'pre-wrap' }}>{d.descr_localita}</div></div>
            <Firme />
          </div>
        )}

        {/* VEICOLI */}
        {pagineAttive['veicoli'] && veicoli.map((v, vi) => (
          <div key={vi} style={S.page}>
            <PageNum n={6 + vi} tot={pagineTotali} ris={d.ris_numero} />
            <div style={S.sez}>DATI DEL VEICOLO {v.label}</div>
            <div style={{ marginBottom: 4 }}><Chk v={v.stato==='IN MARCIA'}/> IN MARCIA &nbsp;<Chk v={v.stato==='IN SOSTA'}/> IN SOSTA &nbsp;<Chk v={v.stato==='ALLONTANATOSI'}/> ALLONTANATOSI</div>
            <div style={S.row}><Ln label="Marca" value={v.marca}/><Ln label="Modello" value={v.modello}/><Ln label="Targa" value={v.targa}/></div>
            <div style={S.row}><Ln label="Telaio" value={v.telaio}/><Ln label="Alimentazione" value={v.alimentazione}/><Ln label="Cilindrata" value={v.cilindrata}/></div>
            <div style={S.row}><Ln label="Anno 1ª Imm." value={v.anno_imm}/><Ln label="Colore" value={v.colore}/></div>
            <div style={{ fontWeight: 'bold', marginTop: 6, marginBottom: 2 }}>Proprietà veicolo:</div>
            <div style={S.row}><Ln label="Cognome e Nome" value={v.prop_nome} flex={3}/><Ln label="Nato a" value={v.prop_nat_a}/><Ln label="Il" value={v.prop_nato}/></div>
            <Ln label="Residenza" value={v.prop_res}/>
            <div style={{ fontWeight: 'bold', marginTop: 6, marginBottom: 2 }}>Conducente:</div>
            <div style={S.row}><Ln label="Cognome e Nome" value={v.cond_nome} flex={3}/><Ln label="Nato a" value={v.cond_nat_a}/><Ln label="Il" value={v.cond_nato}/></div>
            <Ln label="Residenza" value={v.cond_res}/>
            <div style={S.row}><Ln label="Patente n°" value={v.pat_n}/><Ln label="Categoria" value={v.pat_cat}/><Ln label="Scadenza" value={v.pat_scad}/></div>
            <div style={S.row}><Ln label="Codice Fiscale" value={v.cf}/><Ln label="Recapito" value={v.recapito}/></div>
            <div style={{ marginTop: 6, marginBottom: 4 }}>Copertura assicurativa RC auto <Chk v={v.assic_si}/> sì <Chk v={!v.assic_si}/> no</div>
            {v.assic_si&&<><div style={S.row}><Ln label="Compagnia" value={v.compagnia}/><Ln label="Polizza n°" value={v.polizza}/><Ln label="Agenzia" value={v.agenzia}/></div><div style={S.row}><Ln label="Valida dal" value={v.val_dal}/><Ln label="Valida al" value={v.val_al}/></div></>}
            <div style={{ marginTop: 6 }}>Localizzazione danni: <Chk v={v.danni_ant}/> anteriore <Chk v={v.danni_post}/> posteriore <Chk v={v.danni_dx}/> laterale dx <Chk v={v.danni_sx}/> laterale sx</div>
            <div style={{ marginTop: 4 }}><div style={S.label}>Danni constatati:</div><div style={{ minHeight: 50, borderBottom: '1px solid #000', whiteSpace: 'pre-wrap' }}>{v.danni_descr}</div></div>
            <div style={{ marginTop: 6 }}>Destinazione: <Chk v={v.sequestrato==='Sequestrato'}/> Sequestrato <Chk v={v.sequestrato==='Ritirato dal conducente'}/> Ritirato dal conducente <Chk v={v.sequestrato==='Affidato a terzi'}/> Affidato a terzi</div>
            <Firme />
          </div>
        ))}

        {/* INFORTUNATI */}
        {pagineAttive['infortunati'] && infortunati.length > 0 && (
          <div style={S.page}>
            <PageNum n={6 + (pagineAttive['veicoli'] ? veicoli.length : 0)} tot={pagineTotali} ris={d.ris_numero} />
            <div style={S.sez}>INFORTUNATI</div>
            {infortunati.map((inf, i) => (
              <div key={i} style={{ marginBottom: 14, borderBottom: '1px solid #ccc', paddingBottom: 8 }}>
                <div style={{ marginBottom: 4 }}><Chk v={inf.ruolo==='conducente'}/> conducente &nbsp;<Chk v={inf.ruolo==='passeggero'}/> passeggero veicolo <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 20 }}>{inf.veicolo}</span> &nbsp;<Chk v={inf.ruolo==='pedone'}/> pedone &nbsp;<Chk v={inf.deceduto}/> deceduto &nbsp;<Chk v={inf.prog_riservata}/> Prognosi riservata</div>
                <div style={S.row}><Ln label="Cognome e Nome" value={[inf.cognome,inf.nome].filter(Boolean).join(' ')} flex={3}/><Ln label="Nato il" value={inf.nato}/><Ln label="Nato a" value={inf.nat_a}/></div>
                <Ln label="Residenza" value={inf.res}/>
                <div style={S.row}><Ln label="Codice Fiscale" value={inf.cf}/><Ln label="Recapito" value={inf.recapito}/></div>
                <div style={S.row}><Ln label="Ospedale" value={inf.ospedale}/><Ln label="Referto n°" value={inf.referto}/><Ln label="Prognosi" value={inf.prognosi}/></div>
                <Ln label="Diagnosi" value={inf.diagnosi}/>
              </div>
            ))}
            <Firme />
          </div>
        )}

        {/* TESTIMONI */}
        {pagineAttive['testimoni'] && testimoni.length > 0 && (
          <div style={S.page}>
            <div style={S.sez}>TESTIMONI</div>
            {testimoni.map((t, i) => (
              <div key={i} style={{ marginBottom: 10, borderBottom: '1px solid #ccc', paddingBottom: 6 }}>
                <div style={S.row}><Ln label="Cognome e Nome" value={[t.cognome,t.nome].filter(Boolean).join(' ')} flex={3}/><Ln label="Nato il" value={t.nato}/></div>
                <Ln label="Residenza" value={t.res}/>
                <div style={S.row}><Ln label="Codice Fiscale" value={t.cf}/><Ln label="Recapito" value={t.recapito}/></div>
              </div>
            ))}
            <Firme />
          </div>
        )}

        {/* DINAMICA */}
        {pagineAttive['dinamica'] && (
          <div style={S.page}>
            <div style={S.sez}>DINAMICA</div>
            <div style={{ minHeight: 200, whiteSpace: 'pre-wrap', borderBottom: '1px solid #000', marginBottom: 16 }}>{d.dinamica}</div>
            <div style={S.sez}>DANNI A COSE</div>
            <div style={{ minHeight: 60, whiteSpace: 'pre-wrap', borderBottom: '1px solid #000', marginBottom: 16 }}>{d.danni_cose}</div>
            <div style={S.sez}>ALTRE NOTE</div>
            <div style={{ minHeight: 60, whiteSpace: 'pre-wrap', borderBottom: '1px solid #000' }}>{d.altre_note}</div>
            <Firme />
          </div>
        )}

        {/* INFRAZIONI */}
        {pagineAttive['infrazioni'] && (
          <div style={S.page}>
            <div style={S.sez}>INFRAZIONI CONTESTATE E SEGNALAZIONI</div>
            <table style={S.table}>
              <thead><tr><th style={S.th}>Veicolo</th><th style={S.th}>Articolo</th><th style={S.th}>Numero</th><th style={S.th}>Data</th><th style={S.th}>Atti trasmessi a</th></tr></thead>
              <tbody>
                {infrazioni.map((inf, i) => <tr key={i}><td style={S.td}>{inf.veicolo}</td><td style={S.td}>{inf.articolo}</td><td style={S.td}>{inf.numero}</td><td style={S.td}>{inf.data}</td><td style={S.td}>{inf.atti_a}</td></tr>)}
                {infrazioni.length === 0 && <tr><td colSpan={5} style={{ ...S.td, textAlign: 'center', color: '#999' }}>—</td></tr>}
              </tbody>
            </table>
            <Firme />
          </div>
        )}

        {/* CHIUSURA */}
        {pagineAttive['chiusura'] && (
          <div style={S.page}>
            <div style={S.sez}>CHIUSURA OPERAZIONI</div>
            <div style={{ marginBottom: 8 }}>Operazioni terminate il <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 30 }}>{d.op_fine_gg}</span>/<span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 30 }}>{d.op_fine_mm}</span>/<span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 50 }}>{d.op_fine_aa}</span> &nbsp; alle ore <span style={{ borderBottom: '1px solid #000', display: 'inline-block', minWidth: 40 }}>{d.op_fine_hh && d.op_fine_mm2 ? `${d.op_fine_hh}:${d.op_fine_mm2}` : ''}</span></div>
            <div style={{ marginBottom: 16 }}>R.I.S. consegnato all'ufficio &nbsp;<Chk v={d.consegnato_a==='P.G.'}/> P.G. &nbsp;<Chk v={d.consegnato_a==='Sviluppo Planimetrie'}/> Sviluppo Planimetrie &nbsp;<Chk v={d.consegnato_a==='Altro'}/> Altro</div>
            <div style={{ marginTop: 40, display: 'flex', justifyContent: 'space-around', textAlign: 'center' }}>
              <div><div style={{ borderTop: '1px solid #000', paddingTop: 4, minWidth: 160 }}>Ufficiali ed Agenti rilevatori</div>{(d.agenti||[]).filter(a=>a.cognome).map((a,i)=><div key={i} style={{ fontSize: 10 }}>{a.grado} {a.cognome} {a.nome}</div>)}</div>
            </div>
          </div>
        )}

      </div>

      <style>{`
        @media print {
          html, body { margin: 0; padding: 0; background: white; }
          .no-print { display: none !important; }
          @page { size: A4 portrait; margin: 0; }
          .print-wrap-outer { padding: 0 !important; }
          #print-wrap > div { page-break-after: always; break-after: page; }
        }
      `}</style>
    </div>
  )
}
"""

import os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dest = os.path.join(BASE, "src/pages/Anteprima.jsx")
os.makedirs(os.path.dirname(dest), exist_ok=True)
with open(dest, "w", encoding="utf-8") as f:
    f.write(output.strip())

print("✅ src/pages/Anteprima.jsx scritto in " + dest)
