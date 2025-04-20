import asyncio
from telegram import Bot
import os


# Postavi svoj token i chat_id
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

# Lista ključnih reči koje te zanimaju
KLJUCNE_RECI = [
    "Montage de meubles", "Menuisier", "ébéniste", "Électricité",
    "Pose carrelage", "Percer", "fixer", "Enduit",
    "Pose de porte", "portail", "Découpe", "Pose sanitaire",
    "Pose parquet", "Peinture"
]

# Čuvanje prethodno pronađenih poslova da se ne ponavljaju
prethodni_poslovi = set()

def procitaj_poslove():
    url = "https://www.needhelp.com/trouver-un-job"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    poslovi = soup.find_all("a", class_="card")  # Klasa može varirati!
    novi = []

    for posao in poslovi:
        tekst = posao.get_text()
        link = "https://www.needhelp.com" + posao.get("href")
        if any(rec in tekst for rec in KLJUCNE_RECI):
            if link not in prethodni_poslovi:
                prethodni_poslovi.add(link)
                novi.append((tekst.strip(), link))

    return novi

async def send_telegram_message(poruka):
    await bot.send_message(chat_id=CHAT_ID, text=poruka)

async def start_bot():
    while True:
        try:
            novi_poslovi = procitaj_poslove()
            for naslov, link in novi_poslovi:
                poruka = f"🔔 Novi posao: {naslov}\n{link}"
                await send_telegram_message(poruka)
        except Exception as e:
            print("Greška:", e)

        time.sleep(300)  # proverava na svakih 5 minuta
        


import asyncio

async def test():
    await send_telegram_message("✅ Ovo je test poruka od bota!")

asyncio.run(test())

BOT_TOKEN = os.getenv("BOT_TOKEN") CHAT_ID = 1601980040 # tvoj chat_id

async def send_test(): bot = Bot(token=BOT_TOKEN) await bot.send_message(chat_id=CHAT_ID, text="✅ Test poruka od bota!")

asyncio.run(send_test())


