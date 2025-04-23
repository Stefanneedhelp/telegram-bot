from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Putanja do ChromeDriver-a (lokalno koristi apsolutnu putanju, npr. C:/selenium/chromedriver.exe)
CHROMEDRIVER_PATH = "chromedriver"  # ili "C:/putanja/do/chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

print("✅ Otvaram needhelp.com...")
driver.get("https://www.needhelp.com/trouver-un-job")

# Sačekaj da se stranica učita
time.sleep(6)

# Pronađi ponude
print("🔍 Prikupljam ponude poslova...")
naslovi = driver.find_elements(By.CLASS_NAME, "jobCard__title___3AzEc")

if not naslovi:
    print("❌ Nema ponuda pronađenih.")
else:
    for n in naslovi:
        print("📌", n.text)

driver.quit()
