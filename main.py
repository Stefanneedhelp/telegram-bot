
import os
import sys
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
import functools

print = functools.partial(print, flush=True)

print("🐍 Python je pokrenuo skriptu!")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")  # Dodaj ovo u Render env

if not BOT_TOKEN or not CHAT_ID or not SCRAPER_API_KEY:
    raise ValueError("❌ BOT_TOKEN, CHAT_ID ili SCRAPER_API_KEY nisu postavljeni!")

bot = Bot(token=BOT_TOKEN)

URL = "https://www.needhelp.com/trouver-un-job"
SCRAPER_URL = f"http://api.scraperapi.com?api_key={SCRAPER_API_KEY}&url={URL}"

async def send_notification():
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text="✅ Bot koristi ScraperAPI i proverava ponude!"
        )
        print("📨 Test poruka uspešno poslata.")
    except Exception as e:
        print("❌ Greška u slanju test poruke:", e)

async def proveri_poslove():
    print("✅ proveri_poslove() je pokrenut!")

    try:
        print("🌐 Slanje zahteva preko ScraperAPI...")

        response = requests.get(SCRAPER_URL)
        print("📄 HTML renderovan!")

        with open("html_debug.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("📝 HTML sačuvan u 'html_debug.txt'")

        soup = BeautifulSoup(response.text, "html.parser")
        # Ovde ćemo kasnije prilagoditi selektor ako se vidi pravi sadržaj
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






