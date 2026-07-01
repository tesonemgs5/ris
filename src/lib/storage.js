// src/lib/storage.js
// Sostituisce supabase.js — salvataggio locale con localStorage

function genId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2)
}

const KEY = 'ris_rapporti'

function load() {
  try { return JSON.parse(localStorage.getItem(KEY) || '[]') } catch { return [] }
}
function save(data) {
  localStorage.setItem(KEY, JSON.stringify(data))
}

export async function getRapporti() {
  const data = load().sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  return { data, error: null }
}

export async function getRapporto(id) {
  const data = load().find(r => r.id === id) || null
  return { data, error: null }
}

export async function createRapporto(fields) {
  const list = load()
  const record = { ...fields, id: genId(), created_at: new Date().toISOString() }
  list.unshift(record)
  save(list)
  return { data: record, error: null }
}

export async function updateRapporto(id, fields) {
  const list = load()
  const idx = list.findIndex(r => r.id === id)
  if (idx === -1) return { data: null, error: 'not found' }
  list[idx] = { ...list[idx], ...fields, id, created_at: list[idx].created_at }
  save(list)
  return { data: list[idx], error: null }
}

export async function deleteRapporto(id) {
  save(load().filter(r => r.id !== id))
  return { error: null }
}

export function exportBackup() {
  const blob = new Blob([JSON.stringify(load(), null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'RIS_backup_' + new Date().toISOString().slice(0, 10) + '.json'
  a.click()
  URL.revokeObjectURL(url)
}

export async function importBackup(file) {
  const text = await file.text()
  const imported = JSON.parse(text)
  if (!Array.isArray(imported)) throw new Error('File non valido')
  const existing = load()
  const merged = [...imported]
  existing.forEach(r => { if (!merged.find(m => m.id === r.id)) merged.push(r) })
  save(merged)
  return merged.length
}
