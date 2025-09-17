# import requests
# import json
# import time

# # Pas d'authentification requise pour Yugipedia
# # Mais recommandé d'ajouter un User-Agent descriptif
# headers = {
#     'User-Agent': 'Yugi''llection/1.0 (g.petta69@gmail.com; pour projet personnel de rendu de master 2)'
# }

# # Récupération d'une carte spécifique
# def get_card_info(card_name): 
#     params = {
#         'action': 'query',
#         'format': 'json',
#         'titles': card_name,
#         'prop': 'revisions|pageprops',
#         'rvprop': 'content',
#         'rvslots': 'main'
#     }
    
#     url = 'https://yugipedia.com/api.php'
#     response = requests.get(url, params=params, headers=headers)
    
#     return response.json()

# # Test avec "Dark Magician"
# card_data = get_card_info("Dark Magician")

# # Affichage des données de la carte
# if 'query' in card_data and 'pages' in card_data['query']:
#     pages = card_data['query']['pages']
#     for page_id, page_info in pages.items():
#         if 'revisions' in page_info:
#             revision = page_info['revisions'][0]
#             content = revision['*']
#             print(f"Card Name: {page_info.get('title', 'Unknown')}")
#             print(f"Content: {content[:500]}...")  # Affiche les 500 premiers caractères
#         else:
#             print(f"No revisions found for page ID {page_id}.")
# else:
#     print("No card data found or an error occurred.")
# # Pause pour éviter de surcharger le serveur
# time.sleep(1)  # Pause de 1 seconde pour éviter de surcharger le serveur


import requests

# # URL brute du fichier YAML sur GitHub (adapte si l'URL change, regarde le repo)
# yaml_url = "https://github.com/DawnbrandBots/yaml-yugipedia/tree/68a62d0475ab0a4b854c707146d3271ac3f92b34/wikitext/Duel_Monsters_cards"
# # Ou le chemin exact si le fichier s'appelle différemment
# local_filename = "cards.yaml"

# response = requests.get(yaml_url)
# if response.status_code == 200:
#     with open(local_filename, "wb") as f:
#         f.write(response.content)
#     print(f"Téléchargement OK : {local_filename}")
# else:
#     print(f"Erreur téléchargement : {response.status_code}")


# import yaml
# import pandas as pd

# # Charger le fichier YAML des cartes
# with open("./data/cards.yaml", "r", encoding="utf-8") as f:
#     raw_cards = yaml.safe_load(f)

# # Gérer le format du dataset
# if isinstance(raw_cards, dict) and "data" in raw_cards:
#     cards = raw_cards["data"]
# else:
#     cards = raw_cards

# # Champs en accord avec la base de données
# csv_rows = []
# for card in cards:
#     row = {
#         "card_name": card.get("name", ""),
#         "card_type": card.get("type", ""),
#         "attribute": card.get("attribute", ""),
#         "monster_type": card.get("race", ""),
#         "level": card.get("level", ""),
#         "atk": card.get("atk", ""),
#         "def": card.get("def", ""),
#         "description": card.get("desc", ""),
#         "max_copies": 3  # valeur par défaut, à adapter si actualisation via banlist
#     }
#     csv_rows.append(row)

# # Transformation en DataFrame et export
# df = pd.DataFrame(csv_rows)
# df.to_csv("./data/yugipedia_cards_for_db.csv",sep=';', index=False)
# print("Export vers yugipedia_cards_for_db.csv terminé.")

import requests
import pandas as pd
import csv

resp = requests.get("https://db.ygoprodeck.com/api/v7/cardinfo.php")
cards_data = resp.json()["data"]

card_rows = []
for c in cards_data:
    card_rows.append({
        "card_id": c.get("id", ""),
        "passcode": c.get("passcode", ""),
        "card_name": c.get("name", ""),
        "card_type": c.get("type", ""),
        "attribute": c.get("attribute", ""),
        "monster_type": c.get("race", ""),
        "level": c.get("level", ""),
        "atk": c.get("atk", ""),
        "def": c.get("def", ""),
        "description": c.get("desc", ""),
        "archetype": c.get("archetype", ""),
        "ban_status": c.get("banlist_info", {}).get("ban_tcg", ""),
        "max_copies": 3  # Valeur par défaut; peut être actualisée via la banlist
    })
df_cards = pd.DataFrame(card_rows)
df_cards.to_csv("./data/table_card.csv", sep=';', index=False, quotechar='"', quoting=csv.QUOTE_MINIMAL)
print("Export CSV terminé : table_card.csv")

set_rows = []
sets_seen = set()
for c in cards_data:
    for s in c.get("card_sets", []) or []:
        key = (s["set_code"], s["set_name"])
        if key not in sets_seen:
            set_rows.append({
                "set_code": s.get("set_code"),
                "set_name": s.get("set_name"),
                "set_rarity": s.get("set_rarity", ""),
                "set_price": s.get("set_price", ""),
                "release_date": s.get("set_release_date", ""),
                "region": s.get("set_region", ""),
                "language": s.get("set_language", "")
            })
            sets_seen.add(key)
df_sets = pd.DataFrame(set_rows)
df_sets.to_csv("./data/table_card_set.csv", sep=';', index=False, quotechar='"', quoting=csv.QUOTE_MINIMAL)


printing_rows = []
for c in cards_data:
    for s in c.get("card_sets", []) or []:
        printing_rows.append({
            "card_name": c.get("name", ""),
            "set_code": s.get("set_code", ""),
            "rarity": s.get("set_rarity", ""),
            "image_url": c.get("card_images", [{}])[0].get("image_url", ""),
            "is_promo": s.get("is_promo", False),
            "edition": s.get("set_edition", "")
        })
df_printing = pd.DataFrame(printing_rows)
df_printing.to_csv("./data/table_card_printing.csv", sep=';', index=False, quotechar='"', quoting=csv.QUOTE_MINIMAL)
