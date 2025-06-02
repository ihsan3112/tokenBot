import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SENT_TOKENS = {}
PUMPFUN_URL = "https://pump.fun"

def get_new_tokens():
    try:
        response = requests.get(PUMPFUN_URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        token_links = soup.find_all("a", href=lambda href: href and href.startswith("/coin/"))
        token_urls = [PUMPFUN_URL + link['href'] for link in token_links]
        return token_urls[:10]  # ambil 10 token terbaru
    except Exception as e:
        print(f"[ERROR] Gagal scraping Pump.fun: {e}")
        return []

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "disable_web_page_preview": True}
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print("[✅] Terkirim ke Telegram")
        else:
            print(f"[❌] Gagal kirim Telegram: {res.text}")
    except Exception as e:
        print(f"[ERROR] Telegram Error: {e}")

def main():
    print("Bot Pump.fun Logika3 Realtime Scanner dimulai...")
    while True:
        tokens = get_new_tokens()
        now = datetime.utcnow()

        for token_url in tokens:
            if token_url not in SENT_TOKENS:
                SENT_TOKENS[token_url] = now
                message = f"🚀 Token Baru Terdeteksi:\n{token_url}"
                send_telegram_message(message)
            else:
                # Token sudah dikirim lebih dari 5 menit lalu? Reset
                if now - SENT_TOKENS[token_url] > timedelta(minutes=5):
                    del SENT_TOKENS[token_url]

        time.sleep(5)

if __name__ == "__main__":
    main()
