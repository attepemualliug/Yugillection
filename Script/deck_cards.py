import requests
import time
import json

def get_card_info(card_name):
    # Prépare l'URL d'interrogation de l'API, avec remplacement des espaces
    url = f"https://db.ygoprodeck.com/api/v7/cardinfo.php?name={card_name.replace(' ', '%20')}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "data" in data:
            return data["data"][0]  # Prend la première carte trouvée
    return None

def main():
    # Charge les noms des cartes depuis le fichier
    with open("cards.txt", "r", encoding="utf-8") as f:
        cards = [line.strip() for line in f if line.strip()]

    all_cards_info = []
    for card in cards:
        info = get_card_info(card)
        if info:
            print(f"Récupéré info pour : {card}")
            all_cards_info.append(info)
        else:
            print(f"Carte non trouvée : {card}")
        time.sleep(0.3)  # Pause pour limiter la charge API

    # Enregistre les infos des cartes dans un fichier JSON
    with open("deck_cards_info.json", "w", encoding="utf-8") as f:
        json.dump(all_cards_info, f, indent=2, ensure_ascii=False)

    print(f"\nInfos de {len(all_cards_info)} cartes enregistrées dans 'deck_cards_info.json'.")

if __name__ == "__main__":
    main()