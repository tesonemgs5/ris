# RIS — Rapporto Incidente Stradale
## Polizia Locale Napoli

PWA mobile-first per la compilazione del Rapporto Incidente Stradale, con compilazione assistita da AI (voce, testo, foto documenti).

**Modalità attuale: locale.** I rapporti sono salvati nel localStorage del browser sul tuo PC — nessun account cloud richiesto per iniziare. Più sotto trovi come passare a Supabase quando vorrai sincronizzare tra più dispositivi/agenti.

---

## Setup in locale (consigliato per iniziare)

### 1. Installa le dipendenze
```bash
cd ris-pwa
npm install
```

### 2. Configura la chiave AI
```bash
cp .env.example .env
```
Apri `.env` e inserisci solo:
- `VITE_ANTHROPIC_API_KEY` → la tua chiave da console.anthropic.com

### 3. Avvia il progetto
```bash
npm run dev
```
Si apre su `http://localhost:5173` — aprilo con Chrome.

### 4. Installa come PWA sul PC
- Nella barra degli indirizzi di Chrome, clicca l'icona di installazione (⊕ o "Installa app")
- Si apre come finestra a sé, senza barra del browser

### 5. Dati e backup
- Tutti i rapporti restano salvati nel browser di questo PC (localStorage)
- Usa **💾 Esporta backup** nella Dashboard per scaricare un file `.json` con tutti i rapporti
- Usa **📥 Importa backup** per ripristinarli (utile se cambi PC o pulisci il browser)
- ⚠️ Se cancelli i dati di navigazione di Chrome, i rapporti salvati solo in locale vengono persi — esporta backup regolarmente

---

## Passare al cloud (Supabase) — quando sei pronto

Quando vorrai sincronizzare i rapporti tra più agenti/dispositivi:

1. Crea un progetto su supabase.com (se non l'hai già)
2. Esegui `supabase_schema.sql` nello SQL Editor di Supabase
3. Crea gli utenti agenti in Authentication → Users
4. Recupera URL e anon key da Settings → API
5. Negli import dei file `src/App.jsx`, `src/pages/*.jsx`, cambia:
   ```js
   from '../lib/storage'   →   from '../lib/supabase'
   ```
6. Aggiungi le variabili `VITE_SUPABASE_URL` e `VITE_SUPABASE_ANON_KEY` al `.env`
7. Carica su GitHub (repo privato) e collega a Vercel per il deploy online

Il file `src/lib/supabase.js` è già pronto con la stessa interfaccia di `storage.js`, quindi il passaggio richiede solo il cambio import — nessuna riscrittura delle pagine.

---

## Struttura
```
src/
  pages/
    Dashboard.jsx   — Lista rapporti + backup/ripristino
    Rapporto.jsx    — Compilazione: scheda Rapido + tutte le sezioni del modulo
    Anteprima.jsx   — Riepilogo prima della stampa
    Login.jsx       — (usato solo in modalità cloud/Supabase)
  lib/
    storage.js      — Salvataggio locale (localStorage) — modalità attuale
    supabase.js     — Salvataggio cloud (Supabase) — per quando passerai online
    ai.js           — Integrazione Claude API
  hooks/
    useVoice.js     — Web Speech API (riconoscimento vocale)
supabase_schema.sql  — Schema da eseguire solo se/quando passi al cloud
```

---

## Uso
1. Premi **Nuovo Rapporto Incidente**
2. Nella scheda **⚡ Rapido** inserisci data, ora, luogo — si propagano automaticamente in tutto il documento
3. Premi 🎙 per dettare il resto, o usa i **Template predefiniti**
4. Nella sezione Veicoli, carica le foto di **libretto / patente / assicurazione** → l'AI legge e compila
5. Verifica tutto, poi vai su **Anteprima** per il riepilogo finale
6. Ricorda di esportare il backup ogni tanto dalla Dashboard

---

## Sicurezza
- In modalità locale i dati non lasciano mai questo PC
- Le chiavi API non sono mai nel codice, solo nel file `.env` (escluso da Git)
- Quando passerai al cloud: repository privato + Row Level Security su Supabase


