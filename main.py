import os
import time
import asyncio
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import requests

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
PUMPFUN_URL = "https://pump.fun/"

async def get_new_tokens():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(PUMPFUN_URL)
        await page.wait_for_timeout(5000)  # Tunggu 5 detik agar halaman selesai render
        content = await page.content()
        await browser.close()

        soup = BeautifulSoup(content, "html.parser")
        token_links = soup.find_all("a", href=lambda href: href and href.startswith("/coin/"))
        token_urls = [PUMPFUN_URL.rstrip("/") + link['href'] for link in token_links]
        return token_urls[:5]  # Ambil 5 token terbaru

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": True
        }
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print("\u2705 Terkirim ke Telegram")
        else:
            print(f"[X] Gagal kirim Telegram: {res.text}")
    except Exception as e:
        print(f"[X] ERROR Telegram: {e}")

async def main():
    print("\U0001F50D Memulai scraping real-time dari Pump.fun...")
    tokens = await get_new_tokens()
    if tokens:
        for token_url in tokens:
            send_telegram_message(f"\U0001F4C5 Token Baru: {token_url}")
    else:
        print("[INFO] Tidak ada token ditemukan.")

if __name__ == "__main__":
    asyncio.run(main())
