from telegram import Update
from telegram.ext import ContextTypes

from services.parser import interpretar
from bot.keyboards import teclado_categorias
from services.sheets_manager import obtener_sheets
from services.logger import logger
from services.auth import requiere_autorizacion

@requiere_autorizacion
async def recibir(update: Update, context: ContextTypes.DEFAULT_TYPE):

    datos = interpretar(update.message.text)
    sheets = obtener_sheets(update.effective_user.id)
    if datos is None:
        await update.message.reply_text(
            "Formato incorrecto.\n\nEjemplo:\n3500 café"
        )
        return

    monto, descripcion = datos

    # Buscar si ya conocemos la categoría
    categoria = sheets.buscar_categoria(descripcion)

    if categoria:

        context.user_data["pendiente"] = {
            "monto": monto,
            "descripcion": descripcion,
            "categoria": categoria,
        }

        from bot.keyboards import teclado_medios_pago

        await update.message.reply_text(
            f"""💲 ${monto:,.0f}

    📂 {categoria}

    📝 {descripcion}

    ¿Cómo pagaste?""",
            reply_markup=teclado_medios_pago(),
        )

        return

    # Si no la conoce, pedir la categoría
    context.user_data["pendiente"] = {
        "monto": monto,
        "descripcion": descripcion,
    }

    await update.message.reply_text(
        f"""💲 ${monto:,.0f}

📝 {descripcion}

Elegí la categoría""",
        reply_markup=teclado_categorias(),
    )
    logger.info(
    f"Mensaje recibido: {descripcion}"
)