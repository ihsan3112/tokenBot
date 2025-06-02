import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("✅ DEBUG TOKEN:", TELEGRAM_BOT_TOKEN)
print("✅ DEBUG CHAT_ID:", TELEGRAM_CHAT_ID)

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        response = requests.post(url, data=payload)
        print("📤 Telegram status:", response.status_code, response.text)
    except Exception as e:
        print("❌ Telegram error:", e)

def get_token_list():
    try:
        res = requests.get("https://pump.fun/api/token/list?sort=recent")
        return res.json()
    except:
        return []

print("🔍 Mengambil token dari Pump.fun (sinkron dengan Memory 3)...")

tokens = get_token_list()
print(f"📦 Token ditemukan: {len(tokens)}")

tokens = tokens[:3]  # Ambil 3 token pertama

for token in tokens:
    name = token["metadata"]["name"]
    token_id = token["id"]
    buyer_count = token["buyerCount"]
    volume_sol = token["volume"] / 1e9

    message = f"""
🔔 *Token Terbaru Sinkron Memory 3*

Nama: *${name}*
Buyer: {buyer_count}
Volume: {volume_sol:.2f} SOL
URL: [Lihat Token](https://pump.fun/{token_id})
"""
    send_telegram_message(message.strip())

print("✅ Selesai. Bot berhenti.")
