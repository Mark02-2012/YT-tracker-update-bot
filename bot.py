import requests
import time # Aggiungi questo in alto insieme a import requests
import os

# Configurazione App (Nome: ID App Store)
APPS = {
    "YouTube": "544007664",
    "YouTube Music": "1017492454"
}

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def check_updates():
    for app_name, app_id in APPS.items():
        # Interroga l'App Store italiano con trucco anti-cache
        url = f"https://itunes.apple.com/lookup?id={app_id}&country=it&t={int(time.time())}"
        response = requests.get(url).json()

        
        if response["resultCount"] > 0:
            new_version = response["results"][0]["version"]
            file_name = f"version_{app_id}.txt"
            
            # Leggi la versione precedente
            try:
                with open(file_name, "r") as f:
                    old_version = f.read().strip()
            except FileNotFoundError:
                old_version = ""

            # Se la versione è cambiata, invia il messaggio
            if new_version != old_version:
                msg = f"🚀 Nuova versione di {app_name} disponibile!\n📦 Versione: {new_version}"
                requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
                
                # Salva la nuova versione
                with open(file_name, "w") as f:
                    f.write(new_version)

if __name__ == "__main__":
    check_updates()
