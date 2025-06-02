import os
import time
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PUMPFUN_URL = "https://pump.fun/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}


def get_tokens_from_html():
    try:
        res = requests.get(PUMPFUN_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        token_links = soup.find_all("a", href=lambda href: href and href.startswith("/coin/"))
        token_urls = [PUMPFUN_URL + link['href'] for link in token_links]
        return token_urls[:10]
    except Exception as e:
        print("[ERROR] Gagal scraping HTML Pump.fun:", e)
        return []


def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": True
        }
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print("[SUKSES] Terkirim ke Telegram")
        else:
            print("[GAGAL] Kirim ke Telegram:", res.text)
    except Exception as e:
        print("[ERROR] Gagal kirim Telegram:", e)


def main():
    print("🔍 Memulai scraping token real-time dari Pump.fun...")
    tokens = get_tokens_from_html()
    if not tokens:
        print("[INFO] Tidak ada token ditemukan.")
        return

    message = "\n".join([f"👉 {url}" for url in tokens])
    send_telegram(f"🆕 Token Baru Pump.fun:\n{message}")


if __name__ == "__main__":
    main()
