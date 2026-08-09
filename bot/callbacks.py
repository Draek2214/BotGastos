from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from services.sheets_manager import obtener_sheets
from services.categorias import CATEGORIAS
from services.medios_pago import MEDIOS_PAGO

from bot.keyboards import teclado_medios_pago


async def seleccionar_categoria(
        
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    sheets = obtener_sheets(update.effective_user.id)
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
    sheets = obtener_sheets(update.effective_user.id)
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

    # Guardar el gasto
    sheets.agregar_movimiento(
        "Gasto",
        pendiente["categoria"],
        pendiente["monto"],
        pendiente["descripcion"],
        medio,
        update.effective_user.id,
    )

    # --------------------------------------------------
    # CALCULAR DISPONIBLE DEL MES
    # --------------------------------------------------

    ahora = datetime.now()

    mes_actual = ahora.month
    año_actual = ahora.year

    movimientos = sheets.obtener_movimientos()

    total_ingresos = 0
    total_gastos = 0

    for movimiento in movimientos:

        fecha = datetime.strptime(
            movimiento["Fecha"],
            "%d/%m/%Y"
        )

        # Solo movimientos del mes actual
        if (
            fecha.month != mes_actual
            or fecha.year != año_actual
        ):
            continue

        monto = float(movimiento["Monto"])

        tipo = movimiento.get(
            "Tipo",
            ""
        ).strip().lower()

        if tipo == "ingreso":

            total_ingresos += monto

        elif tipo == "gasto":

            total_gastos += monto

    disponible = total_ingresos - total_gastos

    # --------------------------------------------------
    # LIMPIAR GASTO PENDIENTE
    # --------------------------------------------------

    context.user_data.pop("pendiente", None)

    # --------------------------------------------------
    # RESPUESTA
    # --------------------------------------------------

    await query.edit_message_text(
        f"""✅ Registrado

💲 ${pendiente['monto']:,.0f}

📂 {pendiente['categoria']}

💳 {medio}

📝 {pendiente['descripcion']}

────────────────
💵 Disponible este mes: $ {disponible:,.0f}"""
    )
    

async def eliminar_movimiento(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    sheets = obtener_sheets(update.effective_user.id)
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