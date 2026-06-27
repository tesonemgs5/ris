// ── Storage locale (localStorage) ──────────────────────────────────────────────
// Sostituto temporaneo di Supabase per lavorare in locale sul PC, senza account
// cloud. Stessa interfaccia delle funzioni Supabase, così il resto del codice
// (Dashboard, Rapporto, Anteprima) non deve cambiare quando passerai al cloud.
//
// Tutti i rapporti sono salvati sotto la chiave "ris_rapporti" come array JSON
// nel localStorage del browser. I dati restano solo su QUESTO browser/PC.

const STORAGE_KEY = 'ris_rapporti'

function uid() {
  return 'r_' + Math.random().toString(36).slice(2, 10) + Date.now().toString(36)
}

function readAll() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function writeAll(list) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(list))
}

// ── Lista rapporti (ordinati dal più recente) ──────────────────────────────────
export async function getRapporti() {
  const list = readAll().sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  return { data: list, error: null }
}

// ── Singolo rapporto ──────────────────────────────────────────────────────────
export async function getRapporto(id) {
  const list = readAll()
  const found = list.find(r => r.id === id)
  return { data: found || null, error: found ? null : new Error('Rapporto non trovato') }
}

// ── Crea nuovo rapporto ────────────────────────────────────────────────────────
export async function createRapporto(data) {
  const list = readAll()
  const now = new Date().toISOString()
  const newReport = {
    id: uid(),
    created_at: now,
    updated_at: now,
    created_by: 'locale',
    ...data,
  }
  list.push(newReport)
  writeAll(list)
  return { data: newReport, error: null }
}

// ── Aggiorna rapporto esistente ────────────────────────────────────────────────
const READONLY_FIELDS = ['id', 'created_at', 'created_by']

export async function updateRapporto(id, data) {
  const list = readAll()
  const idx = list.findIndex(r => r.id === id)
  if (idx === -1) return { data: null, error: new Error('Rapporto non trovato') }

  const clean = { ...data }
  READONLY_FIELDS.forEach(f => delete clean[f])

  list[idx] = { ...list[idx], ...clean, updated_at: new Date().toISOString() }
  writeAll(list)
  return { data: list[idx], error: null }
}

// ── Elimina rapporto ───────────────────────────────────────────────────────────
export async function deleteRapporto(id) {
  const list = readAll().filter(r => r.id !== id)
  writeAll(list)
  return { data: null, error: null }
}

// ── Esporta tutti i rapporti (backup manuale) ──────────────────────────────────
export function exportBackup() {
  const list = readAll()
  const blob = new Blob([JSON.stringify(list, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `RIS_backup_${new Date().toISOString().slice(0, 10)}.json`
  a.click()
  URL.revokeObjectURL(url)
}

// ── Importa backup (ripristino) ────────────────────────────────────────────────
export async function importBackup(file) {
  const text = await file.text()
  const imported = JSON.parse(text)
  if (!Array.isArray(imported)) throw new Error('File di backup non valido')
  const existing = readAll()
  const existingIds = new Set(existing.map(r => r.id))
  const merged = [...existing, ...imported.filter(r => !existingIds.has(r.id))]
  writeAll(merged)
  return merged.length
}

// ── Stub di autenticazione (non serve in locale, ma manteniamo l'interfaccia) ──
export async function signIn() {
  return { error: null }
}
export async function signOut() {
  return { error: null }
}
export async function getUser() {
  return { id: 'locale', email: 'agente@locale' }
}

// Stub oggetto "supabase" per compatibilità con eventuali chiamate dirette
// (es. supabase.auth.getSession() in App.jsx)
export const supabase = {
  auth: {
    getSession: async () => ({ data: { session: { user: { id: 'locale', email: 'agente@locale' } } } }),
    onAuthStateChange: (callback) => {
      // Simula sessione sempre attiva in locale
      setTimeout(() => callback('SIGNED_IN', { user: { id: 'locale', email: 'agente@locale' } }), 0)
      return { data: { subscription: { unsubscribe: () => {} } } }
    },
    signInWithPassword: async () => ({ error: null }),
    signOut: async () => ({ error: null }),
  },
}

// ── Realtime stub (no-op in locale, niente collaborazione multi-utente offline) ──
export function subscribeToRapporto() {
  return { unsubscribe: () => {} }
}
