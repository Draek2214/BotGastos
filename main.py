from dotenv import load_dotenv
import os
import logging
from bot.commands import hoy, mes, ultimo
from bot.handlers import recibir

from bot.callbacks import (
    seleccionar_categoria,
    eliminar_movimiento,
)

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
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy tu bot de gastos 💰"
    )

async def error_handler(update, context):

    logger.exception(
        "Error no controlado",
        exc_info=context.error
    )

    if update and update.effective_message:

        await update.effective_message.reply_text(
            "⚠️ Ocurrió un error al procesar la solicitud."
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_error_handler(error_handler)
app.add_handler(
    CallbackQueryHandler(
        seleccionar_categoria,
        pattern="^cat_",
    )
)

app.add_handler(
    CallbackQueryHandler(
        eliminar_movimiento,
        pattern="^eliminar_",
    )
)
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hoy", hoy))
app.add_handler(CommandHandler("mes", mes))
app.add_handler(CommandHandler("ultimo", ultimo))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir))

logger.info("Bot iniciado")

app.run_polling()
app.add_error_handler(error_handler)
