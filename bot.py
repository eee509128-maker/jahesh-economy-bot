import os
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

response = requests.get(url)
print("--- TELEGRAM DATA START ---")
print(response.text)
print("--- TELEGRAM DATA END ---")
