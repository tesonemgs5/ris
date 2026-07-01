import os

BASE = os.path.dirname(os.path.abspath(__file__))
gitignore_path = os.path.join(BASE, ".gitignore")

righe_necessarie = [".env", ".env.local", ".env.*.local", "node_modules/"]

if os.path.exists(gitignore_path):
    with open(gitignore_path, "r", encoding="utf-8") as f:
        contenuto = f.read()
else:
    contenuto = ""

aggiunte = []
for riga in righe_necessarie:
    if riga not in contenuto:
        aggiunte.append(riga)

if aggiunte:
    with open(gitignore_path, "a", encoding="utf-8") as f:
        f.write("\n# Variabili d'ambiente — mai pushare\n")
        for r in aggiunte:
            f.write(r + "\n")
    print("✅ .gitignore aggiornato, aggiunte:")
    for r in aggiunte:
        print(f"   + {r}")
else:
    print("✅ .gitignore già corretto, niente da fare")
