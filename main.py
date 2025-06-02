import requests
import os
import time
import json
from datetime import datetime, timedelta

import logging
logging.basicConfig(level=logging.INFO)

# Telegram Setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        logging.info(f"[TELEGRAM] {response.text}")
    except Exception as e:
        logging.error(f"[ERROR] Gagal kirim ke Telegram: {e}")


def get_recent_tokens():
    try:
        url = "https://pump.fun/api/market"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }
        resp = requests.get(url, headers=headers)
        data = resp.json()

        now = datetime.utcnow()
        threshold = now - timedelta(minutes=5)  # Token < 5 menit

        found = []
        for item in data.get("coins", []):
            timestamp = datetime.utcfromtimestamp(item.get("launched_at", 0))
            if timestamp > threshold:
                token_address = item.get("address")
                name = item.get("name", "-")
                buyers = item.get("buyer_count", 0)
                url = f"https://pump.fun/coin/{token_address}"
                found.append((name, buyers, url))

        return found
    except Exception as e:
        logging.error(f"[ERROR] Gagal ambil data JSON Pump.fun: {e}")
        return []


if __name__ == "__main__":
    logging.info("[BOT] Memulai scanning real-time token dari Pump.fun...\n")
    sent = set()
    while True:
        tokens = get_recent_tokens()
        for name, buyers, url in tokens:
            if url in sent:
                continue
            sent.add(url)
            message = f"<b>🚀 Token Baru Terdeteksi!</b>\n" \
                      f"<b>Nama:</b> {name}\n" \
                      f"<b>Buyers:</b> {buyers}\n" \
                      f"<b>Link:</b> {url}"
            send_telegram(message)

        time.sleep(20)
