import os
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

INTERESANTNA_ZANIMANJA = [
    "Montage de meubles", "Menuisier", "ébéniste", "Électricité", "Pose carrelage",
    "Percer", "fixer", "Enduit", "Pose de porte", "portail", "Découpe",
    "Pose sanitaire", "Pose parquet", "Peinture"
]

URL = "https://www.needhelp.com/trouver-un-job"
bot = Bot(token=BOT_TOKEN)
vec_vidjeni = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot je startovao!")
    await send_telegram_message("✅ Ovo je test poruka od bota!")

    while True:
        try:
            response = requests.get(URL)
            soup = BeautifulSoup(response.text, "html.parser")
            ponude = soup.find_all("div", class_="jobCard__title___3AzEc")

            for ponuda in ponude:
                naziv = ponuda.get_text(strip=True)
                link = ponuda.find_parent("a")["href"]
                if naziv not in vec_vidjeni:
                    if any(z in naziv for z in INTERESANTNA_ZANIMANJA):
                        vec_vidjeni.add(naziv)
                      await send_telegram_message("🧪 Ovo je test poruka od bota!")
                            chat_id=CHAT_ID,
                            text=f"📌 Novi posao: {naziv}\n🔗 https://www.needhelp.com{link}"
                        )
        except Exception as e:
            print("Greška:", e)
       await asyncio.sleep(10)
if __name__ == "__main__":
    asyncio.run(proveri_poslove())
