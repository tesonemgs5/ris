import { createClient } from '@supabase/supabase-js'

const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY)

// ── Auth helpers ──────────────────────────────────────────────────────────────
export async function signIn(email, password) {
  return supabase.auth.signInWithPassword({ email, password })
}

export async function signOut() {
  return supabase.auth.signOut()
}

export async function getUser() {
  const { data: { user } } = await supabase.auth.getUser()
  return user
}

// ── Rapporti CRUD ─────────────────────────────────────────────────────────────
export async function getRapporti() {
  return supabase
    .from('rapporti')
    .select('*')
    .order('created_at', { ascending: false })
}

export async function getRapporto(id) {
  return supabase
    .from('rapporti')
    .select('*')
    .eq('id', id)
    .single()
}

export async function createRapporto(data) {
  const user = await getUser()
  return supabase
    .from('rapporti')
    .insert({ ...data, created_by: user?.id })
    .select()
    .single()
}

const READONLY_FIELDS = ['id', 'created_at', 'created_by']

export async function updateRapporto(id, data) {
  const clean = { ...data }
  READONLY_FIELDS.forEach(f => delete clean[f])
  return supabase
    .from('rapporti')
    .update(clean)
    .eq('id', id)
    .select()
    .single()
}

export async function deleteRapporto(id) {
  return supabase.from('rapporti').delete().eq('id', id)
}

// ── Realtime subscription ─────────────────────────────────────────────────────
export function subscribeToRapporto(id, callback) {
  return supabase
    .channel(`rapporto:${id}`)
    .on('postgres_changes', {
      event: 'UPDATE',
      schema: 'public',
      table: 'rapporti',
      filter: `id=eq.${id}`
    }, callback)
    .subscribe()
}

// ── Backup helpers ────────────────────────────────────────────────────────────
export function exportBackup() {
  supabase.from('rapporti').select('*').then(({ data }) => {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `RIS_backup_${new Date().toISOString().slice(0, 10)}.json`
    a.click()
    URL.revokeObjectURL(url)
  })
}

export async function importBackup(file) {
  const text = await file.text()
  const imported = JSON.parse(text)
  if (!Array.isArray(imported)) throw new Error('File di backup non valido')
  const { error } = await supabase.from('rapporti').upsert(imported)
  if (error) throw error
  return imported.length
}
