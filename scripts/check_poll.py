import json
import os
from datetime import datetime
from urllib import request

# Charger le sondage
with open("sondage.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Vérifier si déjà envoyé
if data.get("result_sent", False):
    print("Résultat déjà envoyé.")
    raise SystemExit

# Vérifier la date de fin
fin = datetime.strptime(data["fin"], "%Y-%m-%d %H:%M:%S")
now = datetime.utcnow()

if now < fin:
    print("Le sondage n'est pas encore terminé.")
    raise SystemExit

# Récupérer les votes
votes = data["votes"]

v1 = int(votes.get("1", 0))
v2 = int(votes.get("2", 0))
v3 = int(votes.get("3", 0))
v4 = int(votes.get("4", 0))

total = v1 + v2 + v3 + v4

if total == 0:
    total = 1  # éviter division par zéro

# Calcul des pourcentages
p1 = round(v1 * 100 / total)
p2 = round(v2 * 100 / total)
p3 = round(v3 * 100 / total)
p4 = round(v4 * 100 / total)

# Construire le message Discord
embed = {
    "title": "📊 Résultats du sondage",
    "description": data["question"],
    "color": 14159643,
    "fields": [
        {
            "name": data["reponse_un"],
            "value": f"{v1} votes ({p1}%)",
            "inline": False
        },
        {
            "name": data["reponse_deux"],
            "value": f"{v2} votes ({p2}%)",
            "inline": False
        },
        {
            "name": data["reponse_trois"],
            "value": f"{v3} votes ({p3}%)",
            "inline": False
        },
        {
            "name": data["reponse_quatre"],
            "value": f"{v4} votes ({p4}%)",
            "inline": False
        }
    ],
    "footer": {
        "text": f"Total : {v1+v2+v3+v4} votes • Fin : {data['fin']}"
    }
}

payload = json.dumps({
    "username": "BrrApp",
    "embeds": [embed]
}).encode("utf-8")

webhook = os.environ["DISCORD_WEBHOOK"]

req = request.Request(
    webhook,
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST"
)

with request.urlopen(req) as response:
    print("Discord :", response.status)

# Marquer comme envoyé
data["result_sent"] = True

with open("sondage.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Sondage clôturé automatiquement.")
