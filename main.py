import time
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ========== KONFIGURASI ==========
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SCAN_INTERVAL = 5
ANALYSIS_DELAY = 90
MIN_BUYERS = 11
MIN_VOLUME_SOL = 3.0
MIN_AVG_PER_WALLET = 0.05

token_cache = {}

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    requests.post(url, data=payload)

def get_token_list():
    try:
        res = requests.get("https://pump.fun/api/tokens")
        return res.json()
    except:
        return []

def analyze_token(token, snapshot_awal, snapshot_akhir):
    buyer_awal = snapshot_awal["buyerCount"]
    buyer_akhir = snapshot_akhir["buyerCount"]
    growth_buyers = buyer_akhir - buyer_awal
    volume_sol = snapshot_akhir["volume"] / 1e9
    avg_per_wallet = volume_sol / buyer_akhir if buyer_akhir > 0 else 0

    if (
        buyer_akhir >= MIN_BUYERS and
        growth_buyers > 0 and
        volume_sol >= MIN_VOLUME_SOL and
        avg_per_wallet >= MIN_AVG_PER_WALLET
    ):
        message = f"""
🟢 *Token Potensial Ditemukan*

Nama: *${token['name']}*
Buyer: {buyer_awal} → {buyer_akhir}
Distinct Wallet (estimasi): {buyer_akhir}
Volume: {volume_sol:.2f} SOL
Rata-rata Buy/Wallet: {avg_per_wallet:.2f} SOL
URL: [Lihat di Pump.fun](https://pump.fun/{token['id']})
"""
        send_telegram_message(message.strip())

# ========== MAIN LOOP ==========

print("⏳ Memulai scanner Pump.fun...")

while True:
    now = datetime.utcnow()
    token_list = get_token_list()

    for token in token_list:
        token_id = token["id"]
        created_time = datetime.fromtimestamp(token["created"])
        age_sec = (now - created_time).total_seconds()

        if age_sec <= 300:
            if token_id not in token_cache:
                token_cache[token_id] = {
                    "token": token,
                    "snapshot_awal": {
                        "buyerCount": token["buyerCount"],
                        "volume": token["volume"]
                    },
                    "timestamp": now
                }

    to_delete = []
    for token_id, entry in token_cache.items():
        elapsed = (now - entry["timestamp"]).total_seconds()
        if elapsed >= ANALYSIS_DELAY:
            token = entry["token"]
            latest_list = get_token_list()
            latest = next((t for t in latest_list if t["id"] == token_id), None)

            if latest:
                snapshot_akhir = {
                    "buyerCount": latest["buyerCount"],
                    "volume": latest["volume"]
                }
                analyze_token(token, entry["snapshot_awal"], snapshot_akhir)

            to_delete.append(token_id)

    for token_id in to_delete:
        del token_cache[token_id]

    time.sleep(SCAN_INTERVAL)
