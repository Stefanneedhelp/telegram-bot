import os
import sys
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
import functools

# Obavezno: svi print-ovi odmah idu u log
print = functools.partial(print, flush=True)

print("🐍 Python je pokrenuo skriptu!")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("🔐 BOT_TOKEN:", BOT_TOKEN)
print("🔐 CHAT_ID:", CHAT_ID)

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("❌ BOT_TOKEN ili CHAT_ID nisu postavljeni!")

bot = Bot(token=BOT_TOKEN)

# Vraćamo se na pravi URL sajta
URL = "https://www.needhelp.com/trouver-un-job"

async def send_notification():
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text="✅ Bot je pokrenut i proverava needhelp.com!"
        )
        print("📨 Test poruka uspešno poslata.")
    except Exception as e:
        print("❌ Greška u slanju test poruke:", e)

async def proveri_poslove():
    print("✅ proveri_poslove() je pokrenut!")

    try:
        print("📥 Pripremam zahtev ka needhelp.com...")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        }

        response = requests.get(URL, headers=headers)
        print("📄 HTML skinut!")

        soup = BeautifulSoup(response.text, "html.parser")
        ponude = soup.find_all("div", class_="jobCard__title___3AzEc")

        print(f"🔍 Pronađeno {len(ponude)} ponuda!")

    except Exception as e:
        print("❌ Greška prilikom zahteva:", e)

    while True:
        print("♻️ Loop aktivna! Čekam 60 sekundi...")
        await asyncio.sleep(60)

async def run_bot():
    await send_notification()
    print("⚙️ Pozivam proveri_poslove()...")
    try:
        await proveri_poslove()
    except Exception as e:
        print("💥 Greška u proveri poslova:", e)

if __name__ == "__main__":
    try:
        print("🔥 Skripta pokrenuta!")
        asyncio.run(run_bot())
    except Exception as e:
        print("❌ Došlo je do greške na glavnom nivou:", e)







