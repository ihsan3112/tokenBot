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

def get_new_tokens():
    try:
        response = requests.get(PUMPFUN_URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        token_links = soup.find_all("a", href=lambda href: href and href.startswith("/coin/"))
        token_urls = [PUMPFUN_URL + link["href"] for link in token_links]
        return token_urls[:10]  # Ambil 10 token terbaru
    except Exception as e:
        print(f"[ERROR] Gagal scraping Pump.fun: {e}")
        return []

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "disable_web_page_preview": True}
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print("✅ Pesan terkirim ke Telegram")
        else:
            print(f"❌ Gagal kirim ke Telegram: {res.text}")
    except Exception as e:
        print(f"[ERROR] Telegram error: {e}")

if __name__ == "__main__":
    print("🔍 Memulai scraping token real-time dari Pump.fun...")
    tokens = get_new_tokens()
    if tokens:
        for url in tokens:
            send_telegram_message(f"🔗 Token baru: {url}")
    else:
        print("ℹ️ Tidak ada token ditemukan.")
    print("✅ Bot selesai.")
