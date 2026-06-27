-- ============================================================
-- RIS Napoli - Schema Supabase
-- Incolla questo nel SQL Editor di Supabase e premi RUN
-- ============================================================

-- Tabella rapporti
CREATE TABLE IF NOT EXISTS rapporti (
  id            UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at    TIMESTAMPTZ DEFAULT NOW(),
  updated_at    TIMESTAMPTZ DEFAULT NOW(),
  created_by    UUID REFERENCES auth.users(id),

  -- Identificazione
  ris_numero    TEXT,
  prot_numero   TEXT,
  uo            TEXT,

  -- Data e luogo incidente
  data_gg       TEXT,
  data_mm       TEXT,
  data_aa       TEXT,
  ora_hh        TEXT,
  ora_mm        TEXT,
  luogo         TEXT,
  civico        TEXT,
  palo_illumin  TEXT,
  intersezione  TEXT,
  corrispondenza TEXT,

  -- Tipologia
  tip_solo_danni    BOOLEAN DEFAULT FALSE,
  tip_feriti        BOOLEAN DEFAULT FALSE,
  tip_mortale       BOOLEAN DEFAULT FALSE,
  tip_omissione     BOOLEAN DEFAULT FALSE,

  -- Attività
  att_rilievi_desc  BOOLEAN DEFAULT FALSE,
  att_rilievi_plan  BOOLEAN DEFAULT FALSE,
  att_rilievi_foto  BOOLEAN DEFAULT FALSE,
  att_seq_penale    BOOLEAN DEFAULT FALSE,
  att_seq_amm       BOOLEAN DEFAULT FALSE,

  -- Agenti (array JSON)
  agenti        JSONB DEFAULT '[]',

  -- Intervento
  effettuato_in       TEXT,
  semaforico          TEXT,
  segnalato_da        TEXT,
  ora_segn_hhmm       TEXT,
  data_segn           TEXT,
  ora_arrivo_hhmm     TEXT,
  data_arrivo         TEXT,
  ora_inc_hhmm        TEXT,
  data_inc            TEXT,
  note_intervento     TEXT,
  -- Dati intervento pag.2
  p2_data             TEXT,
  p2_giorno           TEXT,
  p2_ore              TEXT,
  p2_festivo          BOOLEAN DEFAULT FALSE,
  p2_agenti_rilevatori TEXT,

  -- Primo intervento (ambulanza, medico legale, polizia, carabinieri...)
  pi_ambulanza        BOOLEAN DEFAULT FALSE,
  pi_ambulanza_post   TEXT,
  pi_ambulanza_targa  TEXT,
  pi_medico           BOOLEAN DEFAULT FALSE,
  pi_medico_uff       TEXT,
  pi_medico_targa     TEXT,
  pi_pol_locale       BOOLEAN DEFAULT FALSE,
  pi_pol_locale_uo    TEXT,
  pi_pol_locale_targa TEXT,
  pi_pol_stato        BOOLEAN DEFAULT FALSE,
  pi_pol_stato_uff    TEXT,
  pi_pol_stato_targa  TEXT,
  pi_carabinieri      BOOLEAN DEFAULT FALSE,
  pi_carabinieri_uff  TEXT,
  pi_carabinieri_targa TEXT,
  succ_intervenivano  TEXT,

  -- Natura incidente
  natura            TEXT[],
  natura_altro      TEXT,

  -- Veicoli (array JSON, max 8)
  veicoli           JSONB DEFAULT '[]',

  -- Infortunati (array JSON)
  infortunati       JSONB DEFAULT '[]',

  -- Testimoni (array JSON)
  testimoni         JSONB DEFAULT '[]',

  -- Pedoni (array JSON)
  pedoni            JSONB DEFAULT '[]',

  -- Accertamenti psico-fisici (per veicolo A/B/C/D)
  psico             JSONB DEFAULT '{}',

  -- Decessi
  decessi           BOOLEAN DEFAULT FALSE,
  num_decedute      TEXT,
  deceduti_dove     TEXT,
  data_decesso      TEXT,
  pm_notiziato      BOOLEAN DEFAULT FALSE,
  pm_nome           TEXT,
  riconosc_salma    BOOLEAN DEFAULT FALSE,
  cert_decesso      BOOLEAN DEFAULT FALSE,
  cert_decesso_dott TEXT,
  osservazioni      TEXT,

  -- Descrizione strada (pag 9) - colonne dirette
  strada_localiz    TEXT,
  strada_senso      TEXT,
  strada_pav        TEXT,
  meteo             TEXT,
  visibilita        TEXT,
  illuminazione     TEXT,
  traffico          TEXT,
  segnaletica       TEXT,
  descr_localita    TEXT,
  direzione_da      TEXT,
  direzione_a       TEXT,
  semaforico        TEXT,
  semaforico_anomalie TEXT,

  -- Dinamica
  dinamica          TEXT,
  altre_note        TEXT,
  danni_cose        TEXT,

  -- Infrazioni
  infrazioni        JSONB DEFAULT '[]',

  -- Chiusura
  op_fine_gg        TEXT,
  op_fine_mm        TEXT,
  op_fine_aa        TEXT,
  op_fine_hh        TEXT,
  op_fine_mm2       TEXT,
  consegnato_a      TEXT,

  -- Stato rapporto
  stato             TEXT DEFAULT 'bozza' CHECK (stato IN ('bozza', 'completato', 'archiviato')),

  -- Colonna di sicurezza: qualsiasi campo futuro non ancora mappato
  -- viene comunque salvato qui, così nessun dato si perde mai.
  extra             JSONB DEFAULT '{}'
);

-- RLS (Row Level Security) - ogni agente vede solo i propri rapporti
ALTER TABLE rapporti ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Utenti vedono i propri rapporti"
  ON rapporti FOR ALL
  USING (auth.uid() = created_by);

-- Indici
CREATE INDEX idx_rapporti_created_by ON rapporti(created_by);
CREATE INDEX idx_rapporti_created_at ON rapporti(created_at DESC);
CREATE INDEX idx_rapporti_stato ON rapporti(stato);

-- Trigger updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER rapporti_updated_at
  BEFORE UPDATE ON rapporti
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- CONDIVISIONE RAPPORTO tra agenti della stessa pattuglia
-- ============================================================
CREATE TABLE IF NOT EXISTS rapporto_collaboratori (
  id            UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  rapporto_id   UUID REFERENCES rapporti(id) ON DELETE CASCADE,
  user_id       UUID REFERENCES auth.users(id),
  ruolo         TEXT DEFAULT 'editor' CHECK (ruolo IN ('editor', 'viewer')),
  created_at    TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE rapporto_collaboratori ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Collaboratori accedono ai propri rapporti"
  ON rapporto_collaboratori FOR ALL
  USING (auth.uid() = user_id);

-- Policy estesa: i collaboratori vedono anche i rapporti condivisi
CREATE POLICY "Rapporti condivisi visibili ai collaboratori"
  ON rapporti FOR SELECT
  USING (
    auth.uid() = created_by OR
    EXISTS (
      SELECT 1 FROM rapporto_collaboratori
      WHERE rapporto_id = rapporti.id AND user_id = auth.uid()
    )
  );
