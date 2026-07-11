from telegram import Update

from telegram.ext import ContextTypes

from services.sheets import sheets
from services.categorias import CATEGORIAS


async def seleccionar_categoria(update: Update,
                    context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    indice = int(query.data.replace("cat_", ""))

    categoria = CATEGORIAS[indice]

    pendiente = context.user_data.get("pendiente")

    if pendiente is None:

        await query.edit_message_text(

            "No hay ningún gasto pendiente."

        )

        return

    sheets.agregar_movimiento(
        "Gasto",
        categoria,
        pendiente["monto"],
        pendiente["descripcion"],
        update.effective_user.id,
    )

    sheets.guardar_categoria(
        pendiente["descripcion"],
        categoria,
    )