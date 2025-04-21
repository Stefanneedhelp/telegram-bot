import os
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN ili CHAT_ID nisu postavljeni! Proveri environment promenljive.")

INTERESANTNA_ZANIMANJA = [
    "Montage de meubles", "Menuisier", "ébéniste", "Électricité", "Pose carrelage",
    "Percer", "fixer", "Enduit", "Pose de porte", "portail", "Découpe",
    "Pose sanitaire", "Pose parquet", "Peinture", "Poser", "Installation", "Reparer", "Réparer", "Revêtements de sol"
]

URL = "https://www.needhelp.com/trouver-un-job"
bot = Bot(token=BOT_TOKEN)
vec_vidjeni = set()

async def proveri_poslove():
    while True:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(URL, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            ponude = soup.find_all("div", class_="jobCard__title___3AzEc")

            print(f"🔍 Pronađeno {len(ponude)} ponuda...")

            for ponuda in ponude:
                naziv = ponuda.get_text(strip=True)
                link = ponuda.find_parent("a")["href"]
                if naziv not in vec_vidjeni:
                    if any(z in naziv for z in INTERESANTNA_ZANIMANJA):
                        vec_vidjeni.add(naziv)
                        print(f"📤 Šaljem ponudu: {naziv}")
                        await bot.send_message(
                            chat_id=CHAT_ID,
                            text=f"📌 Novi posao: {naziv}\n🔗 https://www.needhelp.com{link}"
                        )
        except Exception as e:
            print("❌ Greška:", e)

        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(proveri_poslove())







