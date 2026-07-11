from dotenv import load_dotenv
import os

from bot.handlers import recibir

from bot.callbacks import seleccionar_categoria

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler,
)

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy tu bot de gastos 💰"
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(

    CallbackQueryHandler(seleccionar_categoria)

)
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir))

print("Bot iniciado...")

app.run_polling()
