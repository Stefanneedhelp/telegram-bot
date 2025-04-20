from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot je startovao!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("✅ Bot je pokrenut. Čeka komande...")
    app.run_polling()
