import os
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot
import unicodedata

print("✅ Script je pokrenut")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("🔐 BOT_TOKEN:", BOT_TOKEN)
print("🔐 CHAT_ID:", CHAT_ID)

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN ili CHAT_ID nisu postavljeni!")
   
    
# 🧠 Normalizacija teksta (uklanja akcente)
def normalize(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()

# 🔍 Ključne reči bez akcenata
INTERESANTNA_ZANIMANJA = [
    "montage", "menuisier", "ebeniste", "electricite", "pose carrelage",
    "percer", "fixer", "enduit", "pose de porte", "portail", "decoupe",
    "pose sanitaire", "pose parquet", "peinture", "poser", "installation", "reparer", "revetements de sol"
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
                naziv_normalizovan = normalize(naziv)

                print("🎯 Ponuda:", naziv_normalizovan)

                link = ponuda.find_parent("a")["href"]

                if naziv_normalizovan not in vec_vidjeni:
                    if any(z in naziv_normalizovan for z in INTERESANTNA_ZANIMANJA):
                        vec_vidjeni.add(naziv_normalizovan)

                        try:
                            await bot.send_message(
                                chat_id=CHAT_ID,
                                text=f"📌 Novi posao: {naziv}\n🔗 https://www.needhelp.com{link}"
                            )
                            print("📤 Poslata ponuda:", naziv)
                        except Exception as e:
                            print("❌ GRESKA PRI SLANJU:", e)

        except Exception as e:
            print("❌ Greška u proveri:", e)

        await asyncio.sleep(60)

if __name__ == "__main__":
    print("🚀 Bot pokrenut...")
    asyncio.run(proveri_poslove())
