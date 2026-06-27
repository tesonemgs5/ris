// ── AI Service ────────────────────────────────────────────────────────────────
// Gestisce: trascrizione voce → compilazione campi + lettura foto documenti

const CLAUDE_API = 'https://api.anthropic.com/v1/messages'

// Dizionario dei campi con descrizioni per l'AI
// (subset compatto - l'AI usa le descrizioni per mappare)
const FIELD_DESCRIPTIONS = {
  // Intestazione
  ris_numero: 'Numero RIS del rapporto',
  prot_numero: 'Numero di protocollo',
  uo: 'Unità operativa',
  data_gg: 'Giorno dell\'incidente (solo numero, es: 17)',
  data_mm: 'Mese dell\'incidente (solo numero, es: 06)',
  data_aa: 'Anno dell\'incidente (4 cifre, es: 2026)',
  ora_hh: 'Ora dell\'incidente (solo ore, es: 15)',
  ora_mm: 'Minuti dell\'incidente (solo minuti, es: 30)',
  luogo: 'Via/Piazza/Corso dove è avvenuto l\'incidente',
  civico: 'Numero civico',
  intersezione: 'Strada all\'intersezione con',
  // Tipologia
  tip_solo_danni: 'true se sinistro con soli danni a cose',
  tip_feriti: 'true se sinistro con feriti',
  tip_mortale: 'true se sinistro mortale',
  tip_omissione: 'true se omissione di soccorso',
  // Attività
  att_rilievi_desc: 'true se effettuati rilievi descrittivi',
  att_rilievi_plan: 'true se effettuati rilievi planimetrici',
  att_rilievi_foto: 'true se effettuati rilievi fotografici',
  // Intervento
  effettuato_in: 'Via in cui è stato effettuato l\'intervento',
  segnalato_da: 'Chi ha segnalato l\'intervento (es: Centrale Operativa)',
  ora_segn_hhmm: 'Ora e minuti segnalazione in formato HH:MM',
  data_segn: 'Data segnalazione in formato GG/MM/AAAA',
  ora_arrivo_hhmm: 'Ora e minuti arrivo sul posto in formato HH:MM',
  data_arrivo: 'Data arrivo sul posto in formato GG/MM/AAAA',
  ora_inc_hhmm: 'Ora presunta dell\'incidente in formato HH:MM',
  // Strada
  meteo: 'Condizioni meteorologiche (es: sereno, pioggia...)',
  pavimentazione: 'Tipo pavimentazione (es: asfaltata, dissestata...)',
  segnaletica: 'Descrizione segnaletica presente',
  // Dinamica
  dinamica: 'Descrizione completa della dinamica dell\'incidente',
  // Natura
  natura: 'Tipo di incidente (es: tamponamento, scontro frontale, investimento pedone...)',
}

// ── Compila campi da testo/voce ───────────────────────────────────────────────
export async function fillFromText(text, currentData = {}, targetPage = null) {
  const pageHint = targetPage !== null
    ? `ATTENZIONE: l'utente ha specificato di compilare SOLO i campi della pagina ${targetPage}.`
    : 'Compila TUTTI i campi possibili in tutto il documento.'

  const prompt = `Sei un assistente per la Polizia Locale di Napoli che compila il Rapporto Incidente Stradale (RIS).

${pageHint}

Analizza il testo seguente e restituisci SOLO un oggetto JSON (senza backtick, senza commenti) con i campi che riesci a estrarre.

CAMPI DISPONIBILI e loro significato:
${Object.entries(FIELD_DESCRIPTIONS).map(([k, v]) => `- "${k}": ${v}`).join('\n')}

Per i veicoli usa questo formato nell'array "veicoli":
[{
  "label": "A",
  "targa": "", "marca": "", "modello": "", "colore": "", "anno_imm": "",
  "telaio": "", "alimentazione": "", "cilindrata": "",
  "prop_cognome": "", "prop_nome": "", "prop_residenza": "",
  "cond_cognome": "", "cond_nome": "", "cond_nato": "", "cond_residenza": "",
  "patente_n": "", "patente_cat": "", "patente_scad": "",
  "assicurazione": "", "polizza": "", "valida_dal": "", "valida_al": ""
}]

Per gli infortunati usa questo formato nell'array "infortunati":
[{
  "ruolo": "conducente|passeggero|pedone",
  "veicolo": "A",
  "cognome": "", "nome": "", "nato": "", "nato_a": "", "residenza": "",
  "cf": "", "recapito": "",
  "ospedale": "", "referto": "", "prognosi": "", "diagnosi": ""
}]

Per gli agenti usa questo formato nell'array "agenti":
[{ "grado": "", "cognome": "", "nome": "", "matricola": "" }]

Restituisci SOLO i campi che hai trovato nel testo, non inventare dati.
Se l'utente dice "solo feriti" imposta tip_feriti: true.
Se l'utente dice "tamponamento" imposta natura: ["Tamponamento multiplo"].

TESTO DA ANALIZZARE:
"""${text}"""

JSON:`

  const res = await fetch(CLAUDE_API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'claude-sonnet-4-6',
      max_tokens: 1500,
      messages: [{ role: 'user', content: prompt }]
    })
  })

  const data = await res.json()
  const raw = data.content?.map(b => b.text || '').join('') || '{}'
  const clean = raw.replace(/```json|```/g, '').trim()

  try {
    const parsed = JSON.parse(clean)
    // Merge con dati esistenti, array si concatenano
    return mergeFormData(currentData, parsed)
  } catch {
    throw new Error('Errore parsing risposta AI')
  }
}

// ── Legge foto documento e compila ───────────────────────────────────────────
export async function fillFromPhoto(base64Image, mediaType = 'image/jpeg', tipo = 'veicolo', vehicleLabel = 'A') {
  const tipoPrompt = tipo === 'veicolo'
    ? `Stai leggendo un documento del VEICOLO ${vehicleLabel} (libretto di circolazione, assicurazione).
Estrai: targa, marca, modello, colore, anno_imm, telaio, alimentazione, cilindrata,
prop_cognome, prop_nome, prop_residenza (del proprietario),
assicurazione (compagnia), polizza, valida_dal, valida_al.`
    : tipo === 'conducente'
    ? `Stai leggendo una PATENTE DI GUIDA o DOCUMENTO D'IDENTITÀ del conducente del veicolo ${vehicleLabel}.
Estrai: cond_cognome, cond_nome, cond_nato (data nascita), cond_nat_a (luogo nascita), cond_residenza,
patente_n, patente_cat, patente_scad, cf.`
    : `Stai leggendo un REFERTO MEDICO o DOCUMENTO D'IDENTITÀ di un infortunato.
Estrai: cognome, nome, nato, nato_a, residenza, cf,
ospedale, referto, prognosi, diagnosi.`

  const prompt = `${tipoPrompt}

Restituisci SOLO un oggetto JSON (senza backtick) con i campi leggibili.
Stringa vuota per i campi non visibili o illeggibili.
Non inventare dati.

JSON:`

  const res = await fetch(CLAUDE_API, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'claude-sonnet-4-6',
      max_tokens: 800,
      messages: [{
        role: 'user',
        content: [
          { type: 'image', source: { type: 'base64', media_type: mediaType, data: base64Image } },
          { type: 'text', text: prompt }
        ]
      }]
    })
  })

  const data = await res.json()
  const raw = data.content?.map(b => b.text || '').join('') || '{}'
  const clean = raw.replace(/```json|```/g, '').trim()

  try {
    return JSON.parse(clean)
  } catch {
    throw new Error('Errore lettura documento')
  }
}

// ── Template predefiniti ──────────────────────────────────────────────────────
export const TEMPLATES = {
  tamponamento: {
    nome: 'Tamponamento',
    emoji: '🚗💥🚗',
    testo: `Il giorno [DATA] alle ore [ORA] in [VIA] al civico [CIVICO] si verificava un tamponamento tra il veicolo A [MARCA_A] targa [TARGA_A] condotto da [CONDUCENTE_A] e il veicolo B [MARCA_B] targa [TARGA_B] condotto da [CONDUCENTE_B] che procedeva nella stessa direzione di marcia. Il conducente [CONDUCENTE_B] riportava [LESIONI] e veniva trasportato presso [OSPEDALE] con prognosi di [PROGNOSI].`,
    campi: ['DATA', 'ORA', 'VIA', 'CIVICO', 'MARCA_A', 'TARGA_A', 'CONDUCENTE_A', 'MARCA_B', 'TARGA_B', 'CONDUCENTE_B', 'LESIONI', 'OSPEDALE', 'PROGNOSI']
  },
  scontro_frontale: {
    nome: 'Scontro frontale',
    emoji: '🚗💥🚗',
    testo: `Il giorno [DATA] alle ore [ORA] in [VIA] si verificava uno scontro frontale/laterale tra il veicolo A [MARCA_A] targa [TARGA_A] condotto da [CONDUCENTE_A] proveniente da [DIREZIONE_A] e il veicolo B [MARCA_B] targa [TARGA_B] condotto da [CONDUCENTE_B] proveniente da [DIREZIONE_B].`,
    campi: ['DATA', 'ORA', 'VIA', 'MARCA_A', 'TARGA_A', 'CONDUCENTE_A', 'DIREZIONE_A', 'MARCA_B', 'TARGA_B', 'CONDUCENTE_B', 'DIREZIONE_B']
  },
  investimento: {
    nome: 'Investimento pedone',
    emoji: '🚗💥🚶',
    testo: `Il giorno [DATA] alle ore [ORA] in [VIA] al civico [CIVICO] il veicolo [MARCA_A] targa [TARGA_A] condotto da [CONDUCENTE_A] investiva il pedone [PEDONE] che stava [AZIONE_PEDONE]. Il pedone riportava [LESIONI] e veniva trasportato presso [OSPEDALE] con prognosi di [PROGNOSI].`,
    campi: ['DATA', 'ORA', 'VIA', 'CIVICO', 'MARCA_A', 'TARGA_A', 'CONDUCENTE_A', 'PEDONE', 'AZIONE_PEDONE', 'LESIONI', 'OSPEDALE', 'PROGNOSI']
  },
  solo_danni: {
    nome: 'Solo danni a cose',
    emoji: '🚗💥🚧',
    testo: `Il giorno [DATA] alle ore [ORA] in [VIA] al civico [CIVICO] si verificava un sinistro con soli danni a cose tra il veicolo A [MARCA_A] targa [TARGA_A] condotto da [CONDUCENTE_A] e il veicolo B [MARCA_B] targa [TARGA_B] condotto da [CONDUCENTE_B].`,
    campi: ['DATA', 'ORA', 'VIA', 'CIVICO', 'MARCA_A', 'TARGA_A', 'CONDUCENTE_A', 'MARCA_B', 'TARGA_B', 'CONDUCENTE_B']
  }
}

// ── Compila template con valori ───────────────────────────────────────────────
export async function fillFromTemplate(templateKey, values) {
  const tmpl = TEMPLATES[templateKey]
  if (!tmpl) throw new Error('Template non trovato')

  let testo = tmpl.testo
  for (const [key, val] of Object.entries(values)) {
    testo = testo.replace(new RegExp(`\\[${key}\\]`, 'g'), val)
  }

  return fillFromText(testo)
}

// ── Merge intelligente dati form ──────────────────────────────────────────────
function mergeFormData(existing, incoming) {
  const result = { ...existing }

  for (const [key, val] of Object.entries(incoming)) {
    if (val === '' || val === null || val === undefined) continue

    if (key === 'veicoli' && Array.isArray(val)) {
      const currentVeicoli = existing.veicoli || []
      val.forEach(newV => {
        const idx = currentVeicoli.findIndex(v => v.label === newV.label)
        if (idx >= 0) {
          currentVeicoli[idx] = { ...currentVeicoli[idx], ...filterEmpty(newV) }
        } else {
          currentVeicoli.push(newV)
        }
      })
      result.veicoli = currentVeicoli
    } else if (key === 'infortunati' && Array.isArray(val)) {
      result.infortunati = [...(existing.infortunati || []), ...val]
    } else if (key === 'agenti' && Array.isArray(val)) {
      result.agenti = val
    } else {
      result[key] = val
    }
  }

  return result
}

function filterEmpty(obj) {
  return Object.fromEntries(Object.entries(obj).filter(([, v]) => v !== '' && v !== null))
}

// ── File to base64 ────────────────────────────────────────────────────────────
export function fileToBase64(file) {
  return new Promise((res, rej) => {
    const r = new FileReader()
    r.onload = () => res(r.result.split(',')[1])
    r.onerror = rej
    r.readAsDataURL(file)
  })
}
