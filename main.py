import os
import sys
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
import functools

# Osiguraj da svi print-ovi idu odmah u log (flush=True)
print = functools.partial(print, flush=True)

print("🐍 Python je pokrenuo skriptu!")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("🔐 BOT_TOKEN:", BOT_TOKEN)
print("🔐 CHAT_ID:", CHAT_ID)

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("❌ BOT_TOKEN ili CHAT_ID nisu postavljeni!")

bot = Bot(token=BOT_TOKEN)

# TEST URL — koristi se umesto needhelp dok ne utvrdimo da li je blokiran
URL = "https://example.com"

async def send_notification():
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text="✅ Bot test pokrenut (example.com test)!"
        )
        print("📨 Test poruka uspešno poslata.")
    except Exception as e:
        print("❌ Greška u slanju test poruke:", e)

async def proveri_poslove():
    print("✅ proveri_poslove() je pokrenut!")

    try:
        print("📥 Pripremam zahtev ka example.com...")
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL, headers=headers)
        print("📄 HTML skinut!")

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "Nema title taga"
        print(f"📰 Title stranice: {title}")

    except Exception as e:
        print("❌ Greška pre while petlje:", e)

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







