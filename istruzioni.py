#!/usr/bin/env python3
"""
LAUNCHER - istruzioni.py
Esegue uno script Python, controlla i file, poi chiede commit/push.
Tutto si ferma finché non premi S.

Uso: python istruzioni.py
"""

import os
import sys
import subprocess

# ═══════════════════════════════════════════════════════════════
# CONFIGURAZIONE - modifica qui se necessario
# ═══════════════════════════════════════════════════════════════

# Coppie (file_output, file_finale) da controllare/rinominare dopo lo script
FILES = [
    ("App_updated.jsx", "App.jsx"),
]

# ═══════════════════════════════════════════════════════════════

def separatore():
    print("=" * 70)

def run_git(cmd, descrizione, root):
    print(f"\n  ▶ {descrizione}...")
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True, cwd=root)
    if result.stdout.strip():
        print(f"    {result.stdout.strip()}")
    if result.returncode != 0:
        print(f"\n  ❌ ERRORE git: {result.stderr.strip()}")
        return False
    print(f"  ✓ OK")
    return True

def scegli_script():
    scripts = [f for f in os.listdir(".") if f.endswith(".py") and f != "istruzioni.py"]
    if not scripts:
        print("❌ Nessuno script .py trovato in questa cartella!")
        sys.exit(1)
    print("\n📋 SCRIPT DISPONIBILI:")
    print()
    for i, s in enumerate(scripts):
        print(f"  [{i+1}] {s}")
    print()
    while True:
        scelta = input("Scegli il numero dello script da eseguire: ").strip()
        if scelta.isdigit() and 1 <= int(scelta) <= len(scripts):
            return scripts[int(scelta) - 1]
        print("  ❌ Numero non valido, riprova.")

def esegui_script(nome_script):
    print(f"\n▶ Esecuzione di: {nome_script}")
    separatore()
    result = subprocess.run([sys.executable, nome_script], text=True)
    separatore()
    return result.returncode == 0

def controlla_file():
    """Controlla quali file di output sono stati creati. Non salva/rinomina nulla."""
    print()
    separatore()
    print(" 📊 SCHEMA FILE")
    separatore()
    print()
    ok = []
    falliti = []
    for output, finale in FILES:
        if os.path.exists(output):
            print(f"  ✅ OK       {output}  →  {finale}")
            ok.append((output, finale))
        else:
            print(f"  ❌ FALLITO  {output}  (atteso, non trovato)")
            falliti.append((output, finale))
    print()
    print(f"  Totale: {len(ok)} OK, {len(falliti)} falliti")
    return ok, falliti

def chiedi_messaggio_commit():
    print()
    separatore()
    print(" ✏️  MESSAGGIO COMMIT")
    separatore()
    print()
    while True:
        msg = input("Scrivi il messaggio di commit: ").strip()
        if msg:
            return msg
        print("  ❌ Il messaggio non può essere vuoto, riprova.")

def chiedi_conferma_finale(commit_msg, ok_list):
    print()
    separatore()
    print(" 🔐 CONFERMA OPERAZIONI FINALI")
    separatore()
    print()
    print("  Dopo aver premuto S verranno eseguite queste operazioni:")
    print()
    if ok_list:
        for output, finale in ok_list:
            print(f"  - Rename:  {output}  →  {finale}  (sovrascrive, nessun backup locale)")
    else:
        print("  (nessun rename — nessun file OK)")
    print(f"  - git add .")
    print(f"  - git commit -m \"{commit_msg}\"")
    print(f"  - git push   (Vercel farà il deploy automaticamente)")
    print()
    while True:
        risposta = input("Salvare tutto? (S/N): ").strip().upper()
        if risposta == "S":
            return True
        elif risposta == "N":
            print("\n❌ Annullato. Nessun file modificato, nessun git.")
            return False
        else:
            print("  ❌ Scrivi S o N")

def fai_rename(ok_list):
    print("\n📁 RENAME FILE:")
    for output, finale in ok_list:
        if os.path.exists(finale):
            os.remove(finale)
        os.rename(output, finale)
        print(f"  ✓ {output} → {finale}")

def fai_git(commit_msg, root):
    print("\n🔧 GIT:")
    ok = run_git("git add .", "git add .", root)
    if not ok:
        print("\n  ⚠️  git add fallito. Continuo comunque...")

    ok = run_git(f'git commit -m "{commit_msg}"', f'git commit -m "{commit_msg}"', root)
    if not ok:
        print("\n  ⚠️  git commit fallito (forse niente da committare?)")
        return False

    ok = run_git("git push", "git push", root)
    if not ok:
        print()
        print("  ❌ git push fallito. Controlla connessione o fai 'git pull'.")
        print("  Poi esegui manualmente:  git push")
        return False

    return True

def main():
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 22 + "🚀 LAUNCHER SCRIPT" + " " * 28 + "║")
    print("╚" + "═" * 68 + "╝")

    separatore()
    print(" STEP 1: Scegli lo script da eseguire")
    separatore()
    nome_script = scegli_script()

    separatore()
    print(f" STEP 2: Esecuzione {nome_script}")
    separatore()
    successo = esegui_script(nome_script)

    if not successo:
        print(f"\n⚠️  Lo script {nome_script} è uscito con errore.")
        r = input("   Vuoi procedere comunque al controllo file? (S/N): ").strip().upper()
        if r != "S":
            print("❌ Operazioni annullate.")
            sys.exit(0)

    # STEP 3: schema OK/falliti, ancora nessun salvataggio
    ok_list, falliti_list = controlla_file()

    # STEP 4: messaggio commit (chiesto subito, prima del salvataggio)
    commit_msg = chiedi_messaggio_commit()

    # STEP 5: conferma finale S/N
    if not chiedi_conferma_finale(commit_msg, ok_list):
        sys.exit(0)

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    fai_rename(ok_list)
    fai_git(commit_msg, root)

    print()
    separatore()
    print(" ✅ TUTTO COMPLETATO!")
    separatore()
    print()
    print(f"  ✓ Script eseguito:  {nome_script}")
    print(f"  ✓ File OK:          {len(ok_list)}")
    print(f"  ✓ File falliti:     {len(falliti_list)}")
    print(f"  ✓ Commit:           \"{commit_msg}\"")
    print(f"  ✓ Git push:         fatto (Vercel deploy automatico)")
    print()

if __name__ == "__main__":
    main()