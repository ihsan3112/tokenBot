import requests

# ========== KONFIGURASI LANGSUNG (untuk tes saja) ==========
TELEGRAM_BOT_TOKEN = "7304825429:AAFkU5nZ47g1bldCJdTaQFZn0hw3c9JP0Bs"
TELEGRAM_CHAT_ID = "7806614019"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    response = requests.post(url, data=payload)
    print("Telegram response:", response.status_code, response.text)

# Kirim pesan uji coba
send_telegram_message("🧪 *Tes Berhasil!* Bot scanner aktif dan berhasil mengirim pesan.")

