from telegram import Update
from telegram.ext import ContextTypes

from services.sheets import sheets
from services.categorias import CATEGORIAS
from services.medios_pago import MEDIOS_PAGO

from bot.keyboards import teclado_medios_pago


async def seleccionar_categoria(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

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

    # Guardamos la categoría elegida para usarla después
    pendiente["categoria"] = categoria

    # Aprendemos la categoría
    sheets.guardar_categoria(
        pendiente["descripcion"],
        categoria,
    )

    # Ahora preguntamos el medio de pago
    await query.edit_message_text(
        f"""💲 ${pendiente['monto']:,.0f}

📂 {categoria}

📝 {pendiente['descripcion']}

¿Cómo pagaste?""",
        reply_markup=teclado_medios_pago()
    )


async def seleccionar_medio_pago(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    indice = int(query.data.replace("medio_", ""))

    medio = MEDIOS_PAGO[indice]

    pendiente = context.user_data.get("pendiente")

    if pendiente is None:

        await query.edit_message_text(
            "No hay ningún gasto pendiente."
        )

        return

    sheets.agregar_movimiento(
        "Gasto",
        pendiente["categoria"],
        pendiente["monto"],
        pendiente["descripcion"],
        medio,
        update.effective_user.id,
    )

    context.user_data.pop("pendiente", None)

    await query.edit_message_text(
        f"""✅ Registrado

💲 ${pendiente['monto']:,.0f}

📂 {pendiente['categoria']}

💳 {medio}

📝 {pendiente['descripcion']}"""
    )


async def eliminar_movimiento(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    try:

        fila = int(query.data.replace("eliminar_", ""))

        sheets.eliminar_movimiento(fila)

        await query.edit_message_text(
            "✅ Movimiento eliminado."
        )

    except Exception:

        await query.edit_message_text(
            "❌ No se pudo eliminar el movimiento."
        )

        raise