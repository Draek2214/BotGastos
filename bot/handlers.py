from telegram import Update
from telegram.ext import ContextTypes

from services.parser import interpretar
from bot.keyboards import teclado_categorias
from services.sheets import sheets


async def recibir(update: Update, context: ContextTypes.DEFAULT_TYPE):

    datos = interpretar(update.message.text)

    if datos is None:
        await update.message.reply_text(
            "Formato incorrecto.\n\nEjemplo:\n3500 café"
        )
        return

    monto, descripcion = datos

    # Buscar si ya conocemos la categoría
    categoria = sheets.buscar_categoria(descripcion)

    if categoria:

        sheets.agregar_movimiento(
            "Gasto",
            categoria,
            monto,
            descripcion,
            update.effective_user.id,
        )

        await update.message.reply_text(
            f"""✅ Registrado automáticamente

💲 ${monto:,.0f}

📂 {categoria}

📝 {descripcion}"""
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