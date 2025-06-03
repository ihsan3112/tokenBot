# === main.py (Logika 5: Real-time scraping Pump.fun pakai headers) ===

import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PUMPFUN_URL = "https://pump.fun"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36"
}

sent_tokens = set()


def get_new_tokens():
    try:
        response = requests.get(PUMPFUN_URL, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=lambda href: href and href.startswith('/coin/'))
        token_urls = [PUMPFUN_URL + link['href'] for link in links]
        return token_urls[:5]  # ambil 5 token terbaru
    except Exception as e:
        print(f"[ERROR] Gagal scraping Pump.fun: {e}")
        return []


def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": True
        }
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print("[OK] Terkirim ke Telegram")
        else:
            print(f"[X] Gagal kirim: {res.text}")
    except Exception as e:
        print(f"[X] Telegram error: {e}")


if __name__ == '__main__':
    print("\U0001F50D Memulai scraping token real-time dari Pump.fun...")
    tokens = get_new_tokens()
    if not tokens:
        print("[INFO] Tidak ada token ditemukan.")
    for url in tokens:
        if url not in sent_tokens:
            send_telegram_message(f"Token Baru: {url}")
            sent_tokens.add(url)
    print("\u2705 Bot selesai.")
