output = """import { useState, useRef, useCallback, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getRapporto, updateRapporto } from "../lib/storage";

const C = { bg:"#F1F5F9",header:"#1E3A5F",accent:"#2563EB",accentLight:"#EFF6FF",muted:"#64748B",border:"#E2E8F0",success:"#16A34A",danger:"#DC2626",card:"#FFFFFF",sectionBg:"#F8FAFC" };

const INIT = {
  ris_numero:"",prot_numero:"",uo:"",
  data_gg:"",data_mm:"",data_aa:"",ora_hh:"",ora_mm:"",
  luogo:"",civico:"",intersezione:"",corrispondenza:"",
  tip_solo_danni:false,tip_feriti:false,tip_mortale:false,tip_omissione:false,
  att_rilievi_desc:false,att_rilievi_plan:false,att_rilievi_foto:false,att_seq_penale:false,att_seq_amm:false,
  agenti:[{grado:"",cognome:"",nome:"",matricola:""},{grado:"",cognome:"",nome:"",matricola:""}],
  p2_data:"",p2_giorno:"",p2_ore:"",p2_festivo:false,p2_agenti_rilevatori:"",
  effettuato_in:"",semaforico:"",semaforico_anomalie:"",segnalato_da:"",
  ora_segn_hhmm:"",data_segn:"",ora_arrivo_hhmm:"",data_arrivo:"",ora_inc_hhmm:"",data_inc:"",
  note_intervento:"",
  pi_ambulanza:false,pi_ambulanza_post:"",pi_ambulanza_targa:"",
  pi_medico:false,pi_medico_uff:"",pi_medico_targa:"",
  pi_pol_locale:false,pi_pol_locale_uo:"",pi_pol_locale_targa:"",
  pi_pol_stato:false,pi_pol_stato_uff:"",pi_pol_stato_targa:"",
  pi_carabinieri:false,pi_carabinieri_uff:"",pi_carabinieri_targa:"",
  succ_intervenivano:"",
  natura:[],natura_altro:"",
  pos_urto_descr:"",pos_statica_descr:"",
  psico:{A:{etil:"",etil_esito:"",narco:"",narco_esito:""},B:{etil:"",etil_esito:"",narco:"",narco_esito:""},C:{etil:"",etil_esito:"",narco:"",narco_esito:""},D:{etil:"",etil_esito:"",narco:"",narco_esito:""}},
  decessi:false,num_decedute:"",deceduti_dove:"",pm_notiziato:false,pm_nome:"",osservazioni:"",
  strada_localiz:"",strada_senso:"",strada_pav:"",meteo:"",visibilita:"",illuminazione:"",traffico:"",segnaletica:"",descr_localita:"",direzione_da:"",direzione_a:"",
  veicoli:[{label:"A",stato:"IN MARCIA"},{label:"B",stato:"IN MARCIA"}],
  pedoni:[],danni_cose:"",testimoni:[],infortunati:[],
  dinamica:"",altre_note:"",
  infrazioni:[{veicolo:"",articolo:"",numero:"",data:"",atti_a:""}],
  op_fine_gg:"",op_fine_mm:"",op_fine_aa:"",op_fine_hh:"",op_fine_mm2:"",consegnato_a:"",
};

const EV = { label:"",stato:"IN MARCIA",marca:"",modello:"",targa:"",colore:"",anno_imm:"",telaio:"",alimentazione:"",cilindrata:"",prop_nome:"",prop_nato:"",prop_nat_a:"",prop_res:"",cond_nome:"",cond_nato:"",cond_nat_a:"",cond_res:"",pat_n:"",pat_cat:"",pat_scad:"",cf:"",recapito:"",assic_si:true,compagnia:"",polizza:"",agenzia:"",val_dal:"",val_al:"",retrovisore:"",acustici:"",indicatore:"",luci_arresto:"",pneumatici:"",km:"",cinture:"",casco:"",airbag:"",abs:"",tracce_suolo:false,frenata:false,frenata_sx:"",frenata_dx:"",danni_ant:false,danni_post:false,danni_dx:false,danni_sx:false,danni_descr:"",sequestrato:"" };
const EI = { ruolo:"conducente",veicolo:"A",cognome:"",nome:"",nato:"",nat_a:"",res:"",cf:"",recapito:"",ospedale:"",referto:"",prognosi:"",diagnosi:"",deceduto:false,prog_riservata:false };
const ET = { cognome:"",nome:"",nato:"",res:"",cf:"",recapito:"" };

function F({label,value,onChange,multi,ph,small}){
  const Tag=multi?"textarea":"input";
  return <div style={{marginBottom:small?8:12}}>
    {label&&<div style={{fontSize:10,fontWeight:700,color:C.muted,marginBottom:4,textTransform:"uppercase"}}>{label}</div>}
    <Tag value={value||""} onChange={e=>onChange(e.target.value)} placeholder={ph||""} rows={multi?4:undefined}
      style={{width:"100%",border:`1.5px solid ${C.border}`,borderRadius:8,padding:small?"8px 10px":"11px 12px",fontSize:small?13:14,fontFamily:"inherit",background:"#fff",outline:"none",resize:multi?"vertical":undefined,boxSizing:"border-box",minHeight:multi?90:undefined}}/>
  </div>;
}
function Row({children}){return <div style={{display:"flex",gap:10,flexWrap:"wrap",marginBottom:2}}>{children}</div>;}
function Col({children,flex=1}){return <div style={{flex,minWidth:80}}>{children}</div>;}
function Toggle({label,value,onChange}){
  return <label style={{display:"flex",alignItems:"center",gap:10,padding:"9px 0",cursor:"pointer",borderBottom:`1px solid ${C.border}`}}>
    <div onClick={()=>onChange(!value)} style={{width:42,height:24,borderRadius:12,background:value?C.accent:"#CBD5E1",position:"relative",transition:"background 0.2s",flexShrink:0}}>
      <div style={{width:18,height:18,borderRadius:"50%",background:"#fff",position:"absolute",top:3,left:value?21:3,transition:"left 0.2s"}}/>
    </div>
    <span style={{fontSize:13,color:"#334155",fontWeight:value?600:400}}>{label}</span>
  </label>;
}
function Radio({options,value,onChange,cols=2}){
  return <div style={{display:"grid",gridTemplateColumns:`repeat(${cols},1fr)`,gap:"6px 10px",marginBottom:10}}>
    {options.map(o=><label key={o} style={{display:"flex",alignItems:"center",gap:6,cursor:"pointer",fontSize:12}}>
      <input type="radio" checked={value===o} onChange={()=>onChange(o)} style={{accentColor:C.accent}}/>{o}
    </label>)}
  </div>;
}
function Chk({label,value,onChange}){
  return <label style={{display:"flex",alignItems:"center",gap:8,cursor:"pointer",fontSize:13,padding:"4px 0"}}>
    <input type="checkbox" checked={!!value} onChange={e=>onChange(e.target.checked)} style={{accentColor:C.accent,width:16,height:16}}/>{label}
  </label>;
}
function Card({title,icon,children,open:initOpen=true}){
  const[open,setOpen]=useState(initOpen);
  return <div style={{background:C.card,borderRadius:12,marginBottom:12,overflow:"hidden",boxShadow:"0 1px 4px rgba(0,0,0,0.07)"}}>
    <button onClick={()=>setOpen(o=>!o)} style={{width:"100%",display:"flex",alignItems:"center",gap:10,background:C.sectionBg,border:"none",borderBottom:open?`1px solid ${C.border}`:"none",padding:"12px 14px",cursor:"pointer",textAlign:"left"}}>
      <span style={{fontSize:16}}>{icon}</span>
      <span style={{fontWeight:700,fontSize:13,color:C.header,flex:1}}>{title}</span>
      <span style={{color:C.muted}}>{open?"▲":"▼"}</span>
    </button>
    {open&&<div style={{padding:14}}>{children}</div>}
  </div>;
}
function Sep({label}){return <div style={{display:"flex",alignItems:"center",gap:8,margin:"12px 0 8px"}}><div style={{flex:1,height:1,background:C.border}}/>{label&&<span style={{fontSize:10,color:C.muted,fontWeight:700,textTransform:"uppercase"}}>{label}</span>}<div style={{flex:1,height:1,background:C.border}}/></div>;}

const SEZIONI=[
  {id:"rapido",label:"⚡ Rapido",icon:""},
  {id:"intestazione",label:"Intestaz.",icon:"📋"},
  {id:"intervento",label:"Intervento",icon:"🚨"},
  {id:"natura",label:"Natura",icon:"💥"},
  {id:"strada",label:"Strada",icon:"🛣"},
  {id:"veicoli",label:"Veicoli",icon:"🚗"},
  {id:"persone",label:"Persone",icon:"👤"},
  {id:"dinamica",label:"Dinamica",icon:"🔄"},
  {id:"infrazioni",label:"Infrazioni",icon:"📄"},
  {id:"chiusura",label:"Chiusura",icon:"✅"},
];

export default function Rapporto(){
  const { id } = useParams();
  const navigate = useNavigate();
  const[form,setForm]=useState(INIT);
  const[loading,setLoading]=useState(true);
  const[saving,setSaving]=useState(false);
  const[savedMsg,setSavedMsg]=useState("");
  const[sez,setSez]=useState("rapido");
  const saveTimer=useRef(null);

  useEffect(() => {
    getRapporto(id).then(({ data: r }) => {
      if (r) setForm(f => ({ ...f, ...r, natura: r.natura || [] }));
      setLoading(false);
    });
  }, [id]);

  useEffect(() => {
    if (loading) return;
    clearTimeout(saveTimer.current);
    saveTimer.current = setTimeout(async () => {
      setSaving(true);
      await updateRapporto(id, form);
      setSaving(false);
      setSavedMsg("Salvato");
      setTimeout(() => setSavedMsg(""), 2000);
    }, 1200);
    return () => clearTimeout(saveTimer.current);
  }, [form, id, loading]);

  const set=useCallback((k,v)=>setForm(f=>{
    const n={...f,[k]:v};
    if(k==="agenti"){
      const str=v.filter(a=>a.cognome).map(a=>`${a.grado} ${a.cognome} ${a.nome} matr.${a.matricola}`.trim()).join(" - ");
      n.p2_agenti_rilevatori=str;
    }
    return n;
  }),[]);
  const setV=useCallback((vi,k,v)=>setForm(f=>{const a=[...f.veicoli];a[vi]={...a[vi],[k]:v};return{...f,veicoli:a};}),[]);
  const setPsico=useCallback((veic,k,v)=>setForm(f=>({...f,psico:{...f.psico,[veic]:{...f.psico[veic],[k]:v}}})),[]);

  function setP(key,val){
    setForm(f=>{
      const n={...f,[key]:val};
      const gg=key==="data_gg"?val:f.data_gg, mm=key==="data_mm"?val:f.data_mm, aa=key==="data_aa"?val:f.data_aa;
      const hh=key==="ora_hh"?val:f.ora_hh, mi=key==="ora_mm"?val:f.ora_mm;
      const dfmt=gg&&mm&&aa?`${gg.padStart(2,"0")}/${mm.padStart(2,"0")}/${aa}`:f.p2_data;
      const ofmt=hh&&mi?`${hh}:${mi}`:f.p2_ore;
      if(["data_gg","data_mm","data_aa"].includes(key)){n.p2_data=dfmt;n.data_inc=dfmt;n.data_segn=dfmt;n.data_arrivo=dfmt;n.op_fine_gg=key==="data_gg"?val:f.op_fine_gg;n.op_fine_mm=key==="data_mm"?val:f.op_fine_mm;n.op_fine_aa=key==="data_aa"?val:f.op_fine_aa;}
      if(["ora_hh","ora_mm"].includes(key)){n.p2_ore=ofmt;n.ora_inc_hhmm=ofmt;}
      if(key==="luogo"||key==="civico"||key==="intersezione"){
        const luogo=key==="luogo"?val:n.luogo;
        const civico=key==="civico"?val:n.civico;
        const inter=key==="intersezione"?val:n.intersezione;
        n.effettuato_in=[luogo,civico,inter].filter(Boolean).join(" - ");
      }
      return n;
    });
  }

  const v=form.veicoli;

  if (loading) return <div style={{ minHeight:"100vh",display:"flex",alignItems:"center",justifyContent:"center",color:C.muted,fontFamily:"'Inter',system-ui,sans-serif" }}>Caricamento rapporto...</div>;

  return(
    <div style={{minHeight:"100vh",background:C.bg,fontFamily:"'Inter',system-ui,sans-serif",maxWidth:640,margin:"0 auto"}}>

      <div style={{background:C.header,padding:"12px 14px",display:"flex",alignItems:"center",gap:10,position:"sticky",top:0,zIndex:100,boxShadow:"0 2px 8px rgba(0,0,0,0.2)"}}>
        <button onClick={()=>navigate("/")} style={{background:"none",border:"none",color:"#93C5FD",fontSize:20,cursor:"pointer",padding:0}}>←</button>
        <div style={{flex:1}}>
          <div style={{color:"#fff",fontWeight:800,fontSize:14}}>{form.ris_numero?`RIS N° ${form.ris_numero}`:"Nuovo rapporto"}</div>
          <div style={{color:"#93C5FD",fontSize:10}}>
            {saving ? "💾 Salvataggio..." : savedMsg ? `✅ ${savedMsg}` : (form.data_gg?`${form.data_gg}/${form.data_mm}/${form.data_aa}`:"RIS · Polizia Locale Napoli")}
          </div>
        </div>
        <button onClick={()=>navigate(`/rapporto/${id}/anteprima`)} style={{background:"#fff",color:C.header,border:"none",borderRadius:8,padding:"6px 12px",fontSize:12,cursor:"pointer",fontWeight:700}}>👁</button>
      </div>

      <div style={{background:"#fff",borderBottom:`1px solid ${C.border}`,overflowX:"auto",WebkitOverflowScrolling:"touch"}}>
        <div style={{display:"flex",minWidth:"max-content"}}>
          {SEZIONI.map(s=>(
            <button key={s.id} onClick={()=>setSez(s.id)} style={{padding:"10px 12px",border:"none",borderBottom:`3px solid ${sez===s.id?C.accent:"transparent"}`,background:"none",color:sez===s.id?C.accent:C.muted,fontWeight:sez===s.id?700:400,fontSize:11,cursor:"pointer",whiteSpace:"nowrap"}}>
              {s.icon} {s.label}
            </button>
          ))}
        </div>
      </div>

      <div style={{padding:"14px 12px 120px"}}>

        {sez==="rapido"&&<>
          <div style={{background:C.header,borderRadius:14,padding:"16px 14px",marginBottom:14}}>
            <div style={{color:"#fff",fontWeight:800,fontSize:16,marginBottom:4}}>⚡ Inserimento Rapido</div>
            <div style={{color:"#93C5FD",fontSize:12}}>Compila questi campi — si propagano automaticamente in tutto il documento</div>
          </div>
          <Card title="Identificazione RIS" icon="🔢">
            <Row><Col><F label="RIS N°" value={form.ris_numero} onChange={v=>set("ris_numero",v)} ph="S5466"/></Col>
            <Col><F label="Prot. N°" value={form.prot_numero} onChange={v=>set("prot_numero",v)}/></Col></Row>
            <F label="U.O." value={form.uo} onChange={v=>set("uo",v)} ph="U.O. Stella"/>
          </Card>
          <Card title="📅 Data e Ora Incidente" icon="">
            <Row>
              <Col><F small label="GG" value={form.data_gg} onChange={v=>setP("data_gg",v)} ph="17"/></Col>
              <Col><F small label="MM" value={form.data_mm} onChange={v=>setP("data_mm",v)} ph="06"/></Col>
              <Col flex={2}><F small label="AAAA" value={form.data_aa} onChange={v=>setP("data_aa",v)} ph="2026"/></Col>
              <Col><F small label="Ore" value={form.ora_hh} onChange={v=>setP("ora_hh",v)} ph="15"/></Col>
              <Col><F small label="Min" value={form.ora_mm} onChange={v=>setP("ora_mm",v)} ph="30"/></Col>
            </Row>
          </Card>
          <Card title="📞 Orari Chiamata e Arrivo" icon="">
            <Row>
              <Col><F small label="🔔 Ora chiamata" value={form.ora_segn_hhmm} onChange={v=>set("ora_segn_hhmm",v)} ph="15:20"/></Col>
              <Col><F small label="Data chiamata" value={form.data_segn} onChange={v=>set("data_segn",v)} ph="17/06/2026"/></Col>
            </Row>
            <Row>
              <Col><F small label="🚔 Ora arrivo" value={form.ora_arrivo_hhmm} onChange={v=>set("ora_arrivo_hhmm",v)} ph="15:35"/></Col>
              <Col><F small label="Data arrivo" value={form.data_arrivo} onChange={v=>set("data_arrivo",v)} ph="17/06/2026"/></Col>
            </Row>
            <Row>
              <Col><F small label="⚠️ Ora incidente" value={form.ora_inc_hhmm} onChange={v=>set("ora_inc_hhmm",v)} ph="15:30"/></Col>
              <Col><F small label="Data incidente" value={form.data_inc} onChange={v=>set("data_inc",v)} ph="17/06/2026"/></Col>
            </Row>
            <F small label="Segnalato da" value={form.segnalato_da} onChange={v=>set("segnalato_da",v)} ph="Centrale Operativa"/>
          </Card>
          <Card title="📍 Luogo dell'Incidente" icon="">
            <F label="Via / Piazza / Corso" value={form.luogo} onChange={v=>setP("luogo",v)} ph="Via Toledo"/>
            <Row>
              <Col><F small label="Civico" value={form.civico} onChange={v=>setP("civico",v)}/></Col>
              <Col flex={2}><F small label="Intersezione con" value={form.intersezione} onChange={v=>setP("intersezione",v)}/></Col>
            </Row>
          </Card>
          <Card title="⚠️ Tipologia Sinistro" icon="">
            <Toggle label="Solo danni a cose" value={form.tip_solo_danni} onChange={v=>set("tip_solo_danni",v)}/>
            <Toggle label="Con feriti" value={form.tip_feriti} onChange={v=>set("tip_feriti",v)}/>
            <Toggle label="Mortale" value={form.tip_mortale} onChange={v=>set("tip_mortale",v)}/>
            <Toggle label="Omissione di soccorso" value={form.tip_omissione} onChange={v=>set("tip_omissione",v)}/>
          </Card>
          <Card title="👮 Agenti Accertatori" icon="">
            {form.agenti.map((ag,i)=>(
              <div key={i} style={{background:C.sectionBg,borderRadius:8,padding:10,marginBottom:8}}>
                <Row>
                  <Col><F small label="Grado" value={ag.grado} onChange={v=>{const a=[...form.agenti];a[i]={...a[i],grado:v};set("agenti",a);}} ph="Ag."/></Col>
                  <Col flex={2}><F small label="Cognome" value={ag.cognome} onChange={v=>{const a=[...form.agenti];a[i]={...a[i],cognome:v};set("agenti",a);}}/></Col>
                  <Col flex={2}><F small label="Nome" value={ag.nome} onChange={v=>{const a=[...form.agenti];a[i]={...a[i],nome:v};set("agenti",a);}}/></Col>
                  <Col><F small label="Matr." value={ag.matricola} onChange={v=>{const a=[...form.agenti];a[i]={...a[i],matricola:v};set("agenti",a);}}/></Col>
                </Row>
              </div>
            ))}
            <button onClick={()=>set("agenti",[...form.agenti,{grado:"",cognome:"",nome:"",matricola:""}])} style={{fontSize:12,color:C.accent,background:"none",border:`1px dashed ${C.accent}`,borderRadius:6,padding:"6px 12px",cursor:"pointer"}}>+ Aggiungi agente</button>
          </Card>
          <div style={{background:"#F0FDF4",border:"1px solid #86EFAC",borderRadius:12,padding:14}}>
            <div style={{fontWeight:700,fontSize:13,color:"#15803D",marginBottom:10}}>✅ Campi propagati nel documento</div>
            {[["Data incidente",form.data_gg?`${form.data_gg}/${form.data_mm}/${form.data_aa}`:null],["Ora incidente",form.ora_hh?`${form.ora_hh}:${form.ora_mm}`:null],["Ora chiamata",form.ora_segn_hhmm||null],["Ora arrivo",form.ora_arrivo_hhmm||null],["Luogo",form.luogo||null],["Via intervento (pag.2)",form.effettuato_in||null],["Data su pag.2",form.p2_data||null],["Ora su pag.2",form.p2_ore||null]].map(([k,v])=>(
              <div key={k} style={{display:"flex",justifyContent:"space-between",padding:"5px 0",borderBottom:"1px solid #BBF7D0",fontSize:12}}>
                <span style={{color:"#64748B"}}>{k}</span>
                <span style={{fontWeight:600,color:v?"#15803D":"#94A3B8"}}>{v||"— non inserito"}</span>
              </div>
            ))}
          </div>
        </>}

        {sez==="intestazione"&&<>
          <Card title="Identificazione RIS" icon="🔢">
            <Row><Col><F label="RIS N°" value={form.ris_numero} onChange={v=>set("ris_numero",v)}/></Col><Col><F label="Prot. N°" value={form.prot_numero} onChange={v=>set("prot_numero",v)}/></Col></Row>
            <F label="U.O." value={form.uo} onChange={v=>set("uo",v)}/>
          </Card>
          <Card title="Data, Ora e Luogo" icon="📍">
            <Row><Col><F small label="GG" value={form.data_gg} onChange={v=>setP("data_gg",v)} ph="17"/></Col><Col><F small label="MM" value={form.data_mm} onChange={v=>setP("data_mm",v)} ph="06"/></Col><Col flex={2}><F small label="AAAA" value={form.data_aa} onChange={v=>setP("data_aa",v)} ph="2026"/></Col><Col><F small label="Ore" value={form.ora_hh} onChange={v=>setP("ora_hh",v)} ph="15"/></Col><Col><F small label="Min" value={form.ora_mm} onChange={v=>setP("ora_mm",v)} ph="30"/></Col></Row>
            <F label="Via / Piazza" value={form.luogo} onChange={v=>setP("luogo",v)} ph="Via Toledo"/>
            <Row><Col><F small label="Civico" value={form.civico} onChange={v=>set("civico",v)}/></Col><Col flex={2}><F small label="Intersezione con" value={form.intersezione} onChange={v=>set("intersezione",v)}/></Col></Row>
            <F label="In corrispondenza di" value={form.corrispondenza} onChange={v=>set("corrispondenza",v)}/>
          </Card>
          <Card title="Tipologia Sinistro" icon="⚠️">
            <Toggle label="Solo danni a cose" value={form.tip_solo_danni} onChange={v=>set("tip_solo_danni",v)}/>
            <Toggle label="Con feriti" value={form.tip_feriti} onChange={v=>set("tip_feriti",v)}/>
            <Toggle label="Mortale" value={form.tip_mortale} onChange={v=>set("tip_mortale",v)}/>
            <Toggle label="Omissione di soccorso" value={form.tip_omissione} onChange={v=>set("tip_omissione",v)}/>
          </Card>
          <Card title="Riepilogo Attività" icon="📝">
            <Toggle label="Rilievi descrittivi" value={form.att_rilievi_desc} onChange={v=>set("att_rilievi_desc",v)}/>
            <Toggle label="Rilievi planimetrici" value={form.att_rilievi_plan} onChange={v=>set("att_rilievi_plan",v)}/>
            <Toggle label="Rilievi fotografici" value={form.att_rilievi_foto} onChange={v=>set("att_rilievi_foto",v)}/>
            <Toggle label="Sequestro penale" value={form.att_seq_penale} onChange={v=>set("att_seq_penale",v)}/>
            <Toggle label="Sequestro amministrativo" value={form.att_seq_amm} onChange={v=>set("att_seq_amm",v)}/>
          </Card>
          <Card title="Agenti Accertatori" icon="👮">
            {form.agenti.map((ag,i)=>(
              <div key={i} style={{background:C.sectionBg,borderRadius:8,padding:10,marginBottom:8}}>
                <Row><Col><F small label="Grado" value={ag.grado} onChange={v=>{const a=[...form.agenti];a[i]={...a[i],grado:v};set("agenti",a);}}/></Col><Col flex={2}><F small label="Cognome" value={ag.cognome} onChange={v=>{const a=[...form.agenti];a[i]={...a[i],cognome:v};set("agenti",a);}}/></Col><Col flex={2}><F small label="Nome" value={ag.nome} onChange={v=>{const a=[...form.agenti];a[i]={...a[i],nome:v};set("agenti",a);}}/></Col><Col><F small label="Matr." value={ag.matricola} onChange={v=>{const a=[...form.agenti];a[i]={...a[i],matricola:v};set("agenti",a);}}/></Col></Row>
              </div>
            ))}
            <button onClick={()=>set("agenti",[...form.agenti,{grado:"",cognome:"",nome:"",matricola:""}])} style={{fontSize:12,color:C.accent,background:"none",border:`1px dashed ${C.accent}`,borderRadius:6,padding:"6px 12px",cursor:"pointer"}}>+ Aggiungi agente</button>
          </Card>
        </>}

        {sez==="intervento"&&<>
          <Card title="Dati Intervento" icon="🚨">
            <Row><Col flex={2}><F small label="Data (GG/MM/AAAA)" value={form.p2_data} onChange={v=>set("p2_data",v)} ph="17/06/2026"/></Col><Col><F small label="Giorno" value={form.p2_giorno} onChange={v=>set("p2_giorno",v)} ph="Mercoledì"/></Col><Col><F small label="Ore" value={form.p2_ore} onChange={v=>set("p2_ore",v)} ph="15:30"/></Col></Row>
            <Toggle label="Festivo" value={form.p2_festivo} onChange={v=>set("p2_festivo",v)}/>
            <F label="Ufficiali/Agenti rilevatori" value={form.p2_agenti_rilevatori} onChange={v=>set("p2_agenti_rilevatori",v)}/>
            <F label="Effettuato in Via" value={form.effettuato_in} onChange={v=>set("effettuato_in",v)}/>
          </Card>
          <Card title="Impianto Semaforico" icon="🚦">
            <Radio options={["Funzionante","Giallo intermittente","Spento"]} value={form.semaforico} onChange={v=>set("semaforico",v)} cols={3}/>
            <F label="Anomalie" value={form.semaforico_anomalie} onChange={v=>set("semaforico_anomalie",v)}/>
          </Card>
          <Card title="Orari Intervento" icon="⏱">
            <F label="Segnalato da" value={form.segnalato_da} onChange={v=>set("segnalato_da",v)} ph="Centrale Operativa"/>
            <Row><Col><F small label="Ora segnalazione" value={form.ora_segn_hhmm} onChange={v=>set("ora_segn_hhmm",v)} ph="15:20"/></Col><Col><F small label="Data segnalazione" value={form.data_segn} onChange={v=>set("data_segn",v)} ph="17/06/2026"/></Col></Row>
            <Row><Col><F small label="Ora arrivo" value={form.ora_arrivo_hhmm} onChange={v=>set("ora_arrivo_hhmm",v)} ph="15:35"/></Col><Col><F small label="Data arrivo" value={form.data_arrivo} onChange={v=>set("data_arrivo",v)} ph="17/06/2026"/></Col></Row>
            <Row><Col><F small label="Ora incidente (presunta)" value={form.ora_inc_hhmm} onChange={v=>set("ora_inc_hhmm",v)} ph="15:30"/></Col><Col><F small label="Data incidente" value={form.data_inc} onChange={v=>set("data_inc",v)} ph="17/06/2026"/></Col></Row>
            <F label="Note" value={form.note_intervento} onChange={v=>set("note_intervento",v)} multi/>
          </Card>
          <Card title="Primo Intervento" icon="🏥">
            {[{k:"pi_ambulanza",l:"Ambulanza 118",pk:"pi_ambulanza_post",tk:"pi_ambulanza_targa",pl:"Postazione"},{k:"pi_medico",l:"Medico Legale",pk:"pi_medico_uff",tk:"pi_medico_targa",pl:"Ufficio"},{k:"pi_pol_locale",l:"Polizia Locale",pk:"pi_pol_locale_uo",tk:"pi_pol_locale_targa",pl:"U.O."},{k:"pi_pol_stato",l:"Polizia di Stato",pk:"pi_pol_stato_uff",tk:"pi_pol_stato_targa",pl:"Ufficio"},{k:"pi_carabinieri",l:"Carabinieri",pk:"pi_carabinieri_uff",tk:"pi_carabinieri_targa",pl:"Ufficio"}].map(item=>(
              <div key={item.k} style={{marginBottom:6}}>
                <Toggle label={item.l} value={form[item.k]} onChange={v=>set(item.k,v)}/>
                {form[item.k]&&<Row><Col flex={2}><F small label={item.pl} value={form[item.pk]} onChange={v=>set(item.pk,v)}/></Col><Col><F small label="Targa" value={form[item.tk]} onChange={v=>set(item.tk,v)}/></Col></Row>}
              </div>
            ))}
            <F label="Successivamente intervenivano" value={form.succ_intervenivano} onChange={v=>set("succ_intervenivano",v)} multi/>
          </Card>
        </>}

        {sez==="natura"&&<>
          <Card title="Natura dell'Incidente" icon="💥">
            {["Scontro frontale tra veicoli in marcia","Scontro frontale/laterale Dx","Scontro frontale/laterale Sx","Scontro laterale tra veicoli in marcia","Tamponamento multiplo","Investimento di pedone","Scontro con velocipede","Veicolo contro veicolo in arresto","Veicolo contro veicolo fermo","Veicolo contro veicolo in sosta","Veicolo contro ostacolo fisso","Veicolo contro ostacolo accidentale","Fuoriuscita dalla sede stradale","Ribaltamento senza urto","Infortunio per frenata improvvisa","Infortunio per caduta dal veicolo","Veicolo in fuga"].map(opt=>{
              const checked=(form.natura||[]).includes(opt);
              return <label key={opt} style={{display:"flex",alignItems:"flex-start",gap:10,padding:"9px 0",borderBottom:`1px solid ${C.border}`,cursor:"pointer"}}>
                <input type="checkbox" checked={checked} onChange={()=>set("natura",checked?(form.natura||[]).filter(x=>x!==opt):[...(form.natura||[]),opt])} style={{accentColor:C.accent,width:16,height:16,marginTop:2,flexShrink:0}}/>
                <span style={{fontSize:13,color:"#334155"}}>{opt}</span>
              </label>;
            })}
            <div style={{marginTop:10}}><F label="Altro" value={form.natura_altro} onChange={v=>set("natura_altro",v)}/></div>
          </Card>
          <Card title="Punto d'Urto / Investimento" icon="📌" open={false}>
            <F label="Descrizione punto d'urto" value={form.pos_urto_descr} onChange={v=>set("pos_urto_descr",v)} multi/>
          </Card>
          <Card title="Posizione Statica Veicoli" icon="🅿️" open={false}>
            <F label="Posizione terminale veicoli" value={form.pos_statica_descr} onChange={v=>set("pos_statica_descr",v)} multi/>
          </Card>
          <Card title="Accertamenti Psico-Fisici" icon="🧪" open={false}>
            {["A","B","C","D"].map(k=>{const p=(form.psico||{})[k]||{etil:"",etil_esito:"",narco:"",narco_esito:""};return(
              <div key={k} style={{background:C.sectionBg,borderRadius:8,padding:10,marginBottom:10}}>
                <div style={{fontWeight:700,fontSize:12,color:C.header,marginBottom:8}}>Veicolo {k}</div>
                <Row>
                  <Col><div style={{fontSize:10,fontWeight:700,color:C.muted,marginBottom:4}}>ETILOMETRO</div><Radio options={["Sì","No","Rifiuto"]} value={p.etil} onChange={v=>setPsico(k,"etil",v)} cols={3}/></Col>
                  <Col><div style={{fontSize:10,fontWeight:700,color:C.muted,marginBottom:4}}>ESITO</div><Radio options={["Positivo","Negativo"]} value={p.etil_esito} onChange={v=>setPsico(k,"etil_esito",v)} cols={2}/></Col>
                </Row>
                <Row>
                  <Col><div style={{fontSize:10,fontWeight:700,color:C.muted,marginBottom:4}}>NARCOTEST</div><Radio options={["Sì","No","Rifiuto"]} value={p.narco} onChange={v=>setPsico(k,"narco",v)} cols={3}/></Col>
                  <Col><div style={{fontSize:10,fontWeight:700,color:C.muted,marginBottom:4}}>ESITO</div><Radio options={["Positivo","Negativo"]} value={p.narco_esito} onChange={v=>setPsico(k,"narco_esito",v)} cols={2}/></Col>
                </Row>
              </div>
            );})}
          </Card>
          <Card title="Decessi" icon="⚫" open={false}>
            <Toggle label="Presenza decessi" value={form.decessi} onChange={v=>set("decessi",v)}/>
            {form.decessi&&<><F small label="N° deceduti" value={form.num_decedute} onChange={v=>set("num_decedute",v)}/><Radio options={["Sul posto","Durante il trasporto","In ospedale","Successivamente"]} value={form.deceduti_dove} onChange={v=>set("deceduti_dove",v)} cols={2}/><Toggle label="P.M. notiziato" value={form.pm_notiziato} onChange={v=>set("pm_notiziato",v)}/>{form.pm_notiziato&&<F small label="P.M." value={form.pm_nome} onChange={v=>set("pm_nome",v)}/>}</>}
          </Card>
          <Card title="Osservazioni" icon="📌" open={false}>
            <F label="Osservazioni e note" value={form.osservazioni} onChange={v=>set("osservazioni",v)} multi/>
          </Card>
        </>}

        {sez==="strada"&&<>
          <Card title="Classificazione Strada" icon="🛣">
            <F label="Direzione DA" value={form.direzione_da} onChange={v=>set("direzione_da",v)} ph="Via Roma"/>
            <F label="Direzione A" value={form.direzione_a} onChange={v=>set("direzione_a",v)} ph="Piazza Garibaldi"/>
            <Radio options={["Strada urbana","Strada extraurbana principale","Strada extraurbana secondaria","Itinerario ciclopedonale"]} value={form.strada_localiz} onChange={v=>set("strada_localiz",v)} cols={2}/>
          </Card>
          <Card title="Carreggiata" icon="↔️">
            <Radio options={["Una carreggiata senso unico","Una carreggiata doppio senso","Una carreggiata senso alternato","Due carreggiate","Più di due carreggiate"]} value={form.strada_senso} onChange={v=>set("strada_senso",v)} cols={2}/>
          </Card>
          <Card title="Pavimentazione" icon="🪨">
            <Radio options={["Asfaltata","Lastricata","In conglomerato cementizio","Acciottolata","In cubetti di porfido","Sterrata","Dissestata"]} value={form.strada_pav} onChange={v=>set("strada_pav",v)} cols={2}/>
          </Card>
          <Card title="Meteo e Visibilità" icon="🌤">
            <Radio options={["Sereno","Nuvoloso","Nebbia","Pioggia in atto","Grandine","Nevicata","Vento forte","Sole radente"]} value={form.meteo} onChange={v=>set("meteo",v)} cols={2}/>
            <Sep label="Visibilità"/>
            <Radio options={["Buona","Sufficiente","Insufficiente"]} value={form.visibilita} onChange={v=>set("visibilita",v)} cols={3}/>
            <Sep label="Illuminazione"/>
            <Radio options={["Ore diurne","Ore notturne con illuminazione pubblica","Ore notturne senza illuminazione"]} value={form.illuminazione} onChange={v=>set("illuminazione",v)} cols={2}/>
          </Card>
          <Card title="Traffico e Segnaletica" icon="🚦">
            <Radio options={["Intenso","Normale","Scarso"]} value={form.traffico} onChange={v=>set("traffico",v)} cols={3}/>
            <F label="Segnaletica verticale e orizzontale" value={form.segnaletica} onChange={v=>set("segnaletica",v)} multi/>
            <F label="Descrizione analitica della località" value={form.descr_localita} onChange={v=>set("descr_localita",v)} multi/>
          </Card>
        </>}

        {sez==="veicoli"&&<>
          {form.veicoli.map((veh,vi)=>(
            <Card key={vi} title={`Veicolo ${veh.label}`} icon="🚗">
              <Radio options={["IN MARCIA","IN SOSTA","ALLONTANATOSI"]} value={veh.stato} onChange={val=>setV(vi,"stato",val)} cols={3}/>
              <Sep label="Dati veicolo"/>
              <Row><Col flex={2}><F small label="Marca" value={veh.marca} onChange={val=>setV(vi,"marca",val)}/></Col><Col flex={2}><F small label="Modello" value={veh.modello} onChange={val=>setV(vi,"modello",val)}/></Col><Col><F small label="Targa" value={veh.targa} onChange={val=>setV(vi,"targa",val)}/></Col></Row>
              <Row><Col><F small label="Colore" value={veh.colore} onChange={val=>setV(vi,"colore",val)}/></Col><Col><F small label="Anno Imm." value={veh.anno_imm} onChange={val=>setV(vi,"anno_imm",val)}/></Col><Col><F small label="Alimentazione" value={veh.alimentazione} onChange={val=>setV(vi,"alimentazione",val)}/></Col></Row>
              <Row><Col flex={2}><F small label="Telaio" value={veh.telaio} onChange={val=>setV(vi,"telaio",val)}/></Col><Col><F small label="Cilindrata" value={veh.cilindrata} onChange={val=>setV(vi,"cilindrata",val)}/></Col></Row>
              <Sep label="Proprietario"/>
              <Row><Col flex={3}><F small label="Cognome e Nome" value={veh.prop_nome} onChange={val=>setV(vi,"prop_nome",val)}/></Col><Col><F small label="Nato il" value={veh.prop_nato} onChange={val=>setV(vi,"prop_nato",val)}/></Col></Row>
              <F small label="Residenza" value={veh.prop_res} onChange={val=>setV(vi,"prop_res",val)}/>
              <Sep label="Conducente"/>
              <Row><Col flex={3}><F small label="Cognome e Nome" value={veh.cond_nome} onChange={val=>setV(vi,"cond_nome",val)}/></Col><Col><F small label="Nato il" value={veh.cond_nato} onChange={val=>setV(vi,"cond_nato",val)}/></Col></Row>
              <F small label="Residenza" value={veh.cond_res} onChange={val=>setV(vi,"cond_res",val)}/>
              <Row><Col flex={2}><F small label="Patente n°" value={veh.pat_n} onChange={val=>setV(vi,"pat_n",val)}/></Col><Col><F small label="Cat." value={veh.pat_cat} onChange={val=>setV(vi,"pat_cat",val)}/></Col><Col><F small label="Scadenza" value={veh.pat_scad} onChange={val=>setV(vi,"pat_scad",val)}/></Col></Row>
              <Row><Col flex={2}><F small label="Codice Fiscale" value={veh.cf} onChange={val=>setV(vi,"cf",val)}/></Col><Col flex={2}><F small label="Recapito" value={veh.recapito} onChange={val=>setV(vi,"recapito",val)}/></Col></Row>
              <Sep label="Assicurazione RC Auto"/>
              <Toggle label="Assicurazione RC presente" value={veh.assic_si} onChange={val=>setV(vi,"assic_si",val)}/>
              {veh.assic_si&&<><Row><Col flex={2}><F small label="Compagnia" value={veh.compagnia} onChange={val=>setV(vi,"compagnia",val)}/></Col><Col flex={2}><F small label="Polizza n°" value={veh.polizza} onChange={val=>setV(vi,"polizza",val)}/></Col><Col><F small label="Agenzia" value={veh.agenzia} onChange={val=>setV(vi,"agenzia",val)}/></Col></Row>
              <Row><Col><F small label="Valida dal" value={veh.val_dal} onChange={val=>setV(vi,"val_dal",val)}/></Col><Col><F small label="Valida al" value={veh.val_al} onChange={val=>setV(vi,"val_al",val)}/></Col></Row></>}
              <Sep label="Dispositivi"/>
              <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:"4px 10px",marginBottom:10}}>
                {[["retrovisore","Retrovisore"],["acustici","Acustici"],["indicatore","Ind. direzione"],["luci_arresto","Luci arresto"],["pneumatici","Pneumatici"]].map(([k,l])=>(
                  <div key={k}><div style={{fontSize:10,fontWeight:700,color:C.muted,marginBottom:2}}>{l}</div><Radio options={["Eff.","Non eff.","Dann."]} value={veh[k]} onChange={val=>setV(vi,k,val)} cols={3}/></div>
                ))}
              </div>
              <Row>{[["cinture","Cinture"],["casco","Casco"],["airbag","Airbag"],["abs","ABS"]].map(([k,l])=>(
                <Col key={k}><div style={{fontSize:10,fontWeight:700,color:C.muted,marginBottom:2}}>{l}</div><Radio options={["Sì","No"]} value={veh[k]} onChange={val=>setV(vi,k,val)} cols={2}/></Col>
              ))}</Row>
              <Sep label="Danni"/>
              <div style={{display:"flex",gap:12,flexWrap:"wrap",marginBottom:8}}>
                {[["danni_ant","Anteriore"],["danni_post","Posteriore"],["danni_dx","Lat. DX"],["danni_sx","Lat. SX"]].map(([k,l])=><Chk key={k} label={l} value={veh[k]} onChange={val=>setV(vi,k,val)}/>)}
              </div>
              <F label="Descrizione danni" value={veh.danni_descr} onChange={val=>setV(vi,"danni_descr",val)} multi/>
              <Sep label="Destinazione veicolo"/>
              <Radio options={["Ritirato dal conducente","Sequestrato","Affidato a terzi"]} value={veh.sequestrato} onChange={val=>setV(vi,"sequestrato",val)} cols={3}/>
              <div style={{display:"flex",justifyContent:"flex-end",marginTop:8}}>
                <button onClick={()=>set("veicoli",form.veicoli.filter((_,i)=>i!==vi))} style={{fontSize:11,color:C.danger,background:"none",border:`1px solid ${C.danger}`,borderRadius:6,padding:"4px 10px",cursor:"pointer"}}>🗑 Rimuovi</button>
              </div>
            </Card>
          ))}
          <button onClick={()=>{const labels="ABCDEFGH";const next=labels[form.veicoli.length]||`V${form.veicoli.length+1}`;set("veicoli",[...form.veicoli,{...EV,label:next}]);}} style={{width:"100%",background:"none",border:`2px dashed ${C.accent}`,color:C.accent,borderRadius:10,padding:14,fontWeight:700,fontSize:14,cursor:"pointer"}}>+ Aggiungi veicolo</button>
        </>}

        {sez==="persone"&&<>
          <div style={{fontSize:12,fontWeight:700,color:C.muted,marginBottom:8,textTransform:"uppercase"}}>Infortunati</div>
          {form.infortunati.map((inf,ii)=>(
            <Card key={ii} title={`Infortunato ${ii+1}${inf.cognome?` — ${inf.cognome} ${inf.nome}`:""}`} icon="🏥">
              <Row><Col flex={2}><F small label="Ruolo" value={inf.ruolo} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],ruolo:v};set("infortunati",a);}}/></Col><Col><F small label="Veicolo" value={inf.veicolo} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],veicolo:v};set("infortunati",a);}} ph="A"/></Col></Row>
              <Row><Col><F small label="Cognome" value={inf.cognome} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],cognome:v};set("infortunati",a);}}/></Col><Col><F small label="Nome" value={inf.nome} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],nome:v};set("infortunati",a);}}/></Col></Row>
              <Row><Col><F small label="Nato il" value={inf.nato} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],nato:v};set("infortunati",a);}}/></Col><Col><F small label="Nato a" value={inf.nat_a} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],nat_a:v};set("infortunati",a);}}/></Col></Row>
              <F small label="Residenza" value={inf.res} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],res:v};set("infortunati",a);}}/>
              <Row><Col><F small label="C.F." value={inf.cf} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],cf:v};set("infortunati",a);}}/></Col><Col><F small label="Recapito" value={inf.recapito} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],recapito:v};set("infortunati",a);}}/></Col></Row>
              <Sep label="Esito medico"/>
              <Row><Col flex={2}><F small label="Ospedale" value={inf.ospedale} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],ospedale:v};set("infortunati",a);}} ph="Cardarelli"/></Col><Col><F small label="Referto n°" value={inf.referto} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],referto:v};set("infortunati",a);}}/></Col><Col><F small label="Prognosi" value={inf.prognosi} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],prognosi:v};set("infortunati",a);}} ph="30 gg"/></Col></Row>
              <F small label="Diagnosi" value={inf.diagnosi} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],diagnosi:v};set("infortunati",a);}} multi/>
              <Row><Col><Chk label="Deceduto" value={inf.deceduto} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],deceduto:v};set("infortunati",a);}}/></Col><Col><Chk label="Prognosi riservata" value={inf.prog_riservata} onChange={v=>{const a=[...form.infortunati];a[ii]={...a[ii],prog_riservata:v};set("infortunati",a);}}/></Col></Row>
              <button onClick={()=>set("infortunati",form.infortunati.filter((_,i)=>i!==ii))} style={{fontSize:11,color:C.danger,background:"none",border:`1px solid ${C.danger}`,borderRadius:6,padding:"4px 10px",cursor:"pointer",marginTop:8}}>🗑 Rimuovi</button>
            </Card>
          ))}
          <button onClick={()=>set("infortunati",[...form.infortunati,{...EI}])} style={{width:"100%",background:"none",border:`2px dashed ${C.accent}`,color:C.accent,borderRadius:10,padding:12,fontWeight:700,fontSize:13,cursor:"pointer",marginBottom:16}}>+ Aggiungi infortunato</button>

          <div style={{fontSize:12,fontWeight:700,color:C.muted,marginBottom:8,textTransform:"uppercase"}}>Testimoni</div>
          {form.testimoni.map((t,ti)=>(
            <Card key={ti} title={`Testimone ${ti+1}${t.cognome?` — ${t.cognome}`:""}`} icon="👁">
              <Row><Col><F small label="Cognome" value={t.cognome} onChange={v=>{const a=[...form.testimoni];a[ti]={...a[ti],cognome:v};set("testimoni",a);}}/></Col><Col><F small label="Nome" value={t.nome} onChange={v=>{const a=[...form.testimoni];a[ti]={...a[ti],nome:v};set("testimoni",a);}}/></Col></Row>
              <Row><Col flex={2}><F small label="Residenza" value={t.res} onChange={v=>{const a=[...form.testimoni];a[ti]={...a[ti],res:v};set("testimoni",a);}}/></Col><Col><F small label="C.F." value={t.cf} onChange={v=>{const a=[...form.testimoni];a[ti]={...a[ti],cf:v};set("testimoni",a);}}/></Col><Col><F small label="Recapito" value={t.recapito} onChange={v=>{const a=[...form.testimoni];a[ti]={...a[ti],recapito:v};set("testimoni",a);}}/></Col></Row>
              <button onClick={()=>set("testimoni",form.testimoni.filter((_,i)=>i!==ti))} style={{fontSize:11,color:C.danger,background:"none",border:`1px solid ${C.danger}`,borderRadius:6,padding:"4px 10px",cursor:"pointer"}}>🗑 Rimuovi</button>
            </Card>
          ))}
          <button onClick={()=>set("testimoni",[...form.testimoni,{...ET}])} style={{width:"100%",background:"none",border:`2px dashed ${C.accent}`,color:C.accent,borderRadius:10,padding:12,fontWeight:700,fontSize:13,cursor:"pointer",marginBottom:16}}>+ Aggiungi testimone</button>

          <Card title="Danni a Cose" icon="🔧">
            <F label="Descrizione danni a cose" value={form.danni_cose} onChange={v=>set("danni_cose",v)} multi/>
          </Card>
        </>}

        {sez==="dinamica"&&<>
          <Card title="Dinamica dell'Incidente" icon="🔄">
            <F label="Descrizione dinamica completa" value={form.dinamica} onChange={v=>set("dinamica",v)} multi ph="Descrivi la sequenza degli eventi..."/>
          </Card>
          <Card title="Altre Note" icon="📌">
            <F label="Note aggiuntive" value={form.altre_note} onChange={v=>set("altre_note",v)} multi/>
          </Card>
        </>}

        {sez==="infrazioni"&&<>
          {form.infrazioni.map((inf,ii)=>(
            <Card key={ii} title={`Infrazione ${ii+1}`} icon="📄">
              <Row><Col><F small label="Veicolo" value={inf.veicolo} onChange={v=>{const a=[...form.infrazioni];a[ii]={...a[ii],veicolo:v};set("infrazioni",a);}} ph="A"/></Col><Col flex={3}><F small label="Articolo C.d.S." value={inf.articolo} onChange={v=>{const a=[...form.infrazioni];a[ii]={...a[ii],articolo:v};set("infrazioni",a);}} ph="art. 141 C.d.S."/></Col></Row>
              <Row><Col><F small label="N° verbale" value={inf.numero} onChange={v=>{const a=[...form.infrazioni];a[ii]={...a[ii],numero:v};set("infrazioni",a);}}/></Col><Col><F small label="Data" value={inf.data} onChange={v=>{const a=[...form.infrazioni];a[ii]={...a[ii],data:v};set("infrazioni",a);}}/></Col><Col flex={2}><F small label="Atti trasmessi a" value={inf.atti_a} onChange={v=>{const a=[...form.infrazioni];a[ii]={...a[ii],atti_a:v};set("infrazioni",a);}}/></Col></Row>
              <button onClick={()=>set("infrazioni",form.infrazioni.filter((_,i)=>i!==ii))} style={{fontSize:11,color:C.danger,background:"none",border:`1px solid ${C.danger}`,borderRadius:6,padding:"4px 10px",cursor:"pointer"}}>🗑 Rimuovi</button>
            </Card>
          ))}
          <button onClick={()=>set("infrazioni",[...form.infrazioni,{veicolo:"",articolo:"",numero:"",data:"",atti_a:""}])} style={{width:"100%",background:"none",border:`2px dashed ${C.accent}`,color:C.accent,borderRadius:10,padding:12,fontWeight:700,fontSize:13,cursor:"pointer"}}>+ Aggiungi infrazione</button>
        </>}

        {sez==="chiusura"&&<>
          <Card title="Chiusura Operazioni" icon="✅">
            <div style={{fontSize:12,color:C.muted,marginBottom:10}}>Operazioni terminate il</div>
            <Row><Col><F small label="GG" value={form.op_fine_gg} onChange={v=>set("op_fine_gg",v)} ph="17"/></Col><Col><F small label="MM" value={form.op_fine_mm} onChange={v=>set("op_fine_mm",v)} ph="06"/></Col><Col flex={2}><F small label="AAAA" value={form.op_fine_aa} onChange={v=>set("op_fine_aa",v)} ph="2026"/></Col><Col><F small label="Ore" value={form.op_fine_hh} onChange={v=>set("op_fine_hh",v)} ph="18"/></Col><Col><F small label="Min" value={form.op_fine_mm2} onChange={v=>set("op_fine_mm2",v)} ph="00"/></Col></Row>
            <Radio options={["P.G.","Sviluppo Planimetrie","Altro"]} value={form.consegnato_a} onChange={v=>set("consegnato_a",v)} cols={3}/>
          </Card>
          <Card title="Riepilogo Rapporto" icon="📊">
            <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:8}}>
              {[["RIS N°",form.ris_numero||"—"],["Data",form.data_gg?`${form.data_gg}/${form.data_mm}/${form.data_aa}`:"—"],["Ora",form.ora_hh?`${form.ora_hh}:${form.ora_mm}`:"—"],["Luogo",form.luogo||"—"],["Tipologia",[form.tip_solo_danni&&"Danni",form.tip_feriti&&"Feriti",form.tip_mortale&&"Mortale"].filter(Boolean).join(", ")||"—"],["Veicoli",form.veicoli.filter(v=>v.targa).map(v=>`${v.label}:${v.targa}`).join(", ")||"—"],["Infortunati",String(form.infortunati.length)],["Testimoni",String(form.testimoni.length)]].map(([k,v])=>(
                <div key={k} style={{background:C.sectionBg,borderRadius:8,padding:"8px 10px"}}>
                  <div style={{fontSize:10,color:C.muted,fontWeight:700,textTransform:"uppercase"}}>{k}</div>
                  <div style={{fontSize:13,color:C.header,fontWeight:600,marginTop:2}}>{v}</div>
                </div>
              ))}
            </div>
            <button onClick={()=>{const b=new Blob([JSON.stringify(form,null,2)],{type:"application/json"});const u=URL.createObjectURL(b);const a=document.createElement("a");a.href=u;a.download=`RIS_${form.ris_numero||"bozza"}.json`;a.click();}} style={{width:"100%",background:C.accent,color:"#fff",border:"none",borderRadius:10,padding:12,fontWeight:700,fontSize:13,cursor:"pointer",marginTop:14}}>💾 Esporta JSON</button>
          </Card>
        </>}
      </div>
    </div>
  );
}
"""

import os
BASE = os.path.dirname(os.path.abspath(__file__))
dest = os.path.join(BASE, "src/pages/Rapporto.jsx")
os.makedirs(os.path.dirname(dest), exist_ok=True)
with open(dest, "w", encoding="utf-8") as f:
    f.write(output.strip())

print("✅ src/pages/Rapporto.jsx scritto in " + dest)
