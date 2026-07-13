from datetime import datetime
from collections import defaultdict

from telegram import Update
from telegram.ext import ContextTypes

from services.sheets_manager import obtener_sheets
from bot.keyboards import teclado_ultimo
from services.auth import requiere_autorizacion

@requiere_autorizacion
async def hoy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sheets = obtener_sheets(update.effective_user.id)
    usuario = update.effective_user.id

    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    movimientos = sheets.obtener_movimientos()

    movimientos_hoy = [
        m for m in movimientos
        if m["Fecha"] == fecha_hoy
        and str(m["Usuario"]) == str(usuario)
    ]

    if not movimientos_hoy:
        await update.message.reply_text(
            "📅 Hoy no registraste movimientos."
        )
        return

    mensaje = "📅 Movimientos de hoy\n\n"

    total = 0

    for movimiento in movimientos_hoy:

        monto = float(movimiento["Monto"])
        total += monto

        mensaje += (
            f"{movimiento['Categoria']} "
            f"{movimiento['Descripcion']} "
            f"$ {monto:,.0f}\n"
            f"💳 {movimiento['MedioPago']}\n"
        )

    mensaje += (
        f"\n────────────────\n"
        f"💰 Total: $ {total:,.0f}"
    )

    await update.message.reply_text(mensaje)

@requiere_autorizacion
async def mes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sheets = obtener_sheets(update.effective_user.id)
    usuario = update.effective_user.id

    hoy = datetime.now()

    movimientos = sheets.obtener_movimientos()

    totales = defaultdict(float)

    for movimiento in movimientos:

        if str(movimiento["Usuario"]) != str(usuario):
            continue

        fecha = datetime.strptime(
            movimiento["Fecha"],
            "%d/%m/%Y"
        )

        if fecha.month != hoy.month or fecha.year != hoy.year:
            continue

        totales[movimiento["Categoria"]] += float(
            movimiento["Monto"]
        )

    if not totales:

        await update.message.reply_text(
            "📅 Este mes no registraste movimientos."
        )

        return

    mensaje = f"📅 Resumen de {hoy.strftime('%B %Y')}\n\n"

    total = 0

    for categoria, monto in sorted(
        totales.items(),
        key=lambda x: x[1],
        reverse=True,
    ):

        total += monto

        mensaje += (
            f"{categoria:<18}"
            f"$ {monto:,.0f}\n"
            f"💳 {movimiento['MedioPago']}\n"
        )

    mensaje += (
        f"\n────────────────\n"
        f"💰 Total: $ {total:,.0f}"
    )

    await update.message.reply_text(mensaje)

@requiere_autorizacion    
async def ultimo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sheets = obtener_sheets(update.effective_user.id)
    movimiento = sheets.obtener_ultimo_movimiento(
        update.effective_user.id
    )

    if movimiento is None:

        await update.message.reply_text(
            "Todavía no registraste movimientos."
        )

        return

    mensaje = (
        "📝 Último movimiento\n\n"
        f"📅 {movimiento['Fecha']} {movimiento['Hora']}\n\n"
        f"📂 {movimiento['Categoria']}\n"
        f"📝 {movimiento['Descripcion']}\n"
        f"💳 {movimiento['MedioPago']}\n"
        f"💰 $ {float(movimiento['Monto']):,.0f}"
)

    await update.message.reply_text(
    mensaje,
    reply_markup=teclado_ultimo(
    movimiento["_fila"]
    )
)
    
def mensaje_ayuda():

    return """
👋 ¡Bienvenido a Bot Gastos!

Con este bot podés registrar tus gastos de forma rápida.

💵 Ejemplos:

3500 café
25000 YPF
18000 Carrefour

📅 Comandos disponibles

/hoy - Muestra los movimientos de hoy.

/mes - Muestra los movimientos del mes.

/ultimo - Muestra el último movimiento registrado.

/ayuda - Muestra esta ayuda.
"""


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        mensaje_ayuda()
    )