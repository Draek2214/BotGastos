from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from services.sheets import sheets


async def hoy(update: Update, context: ContextTypes.DEFAULT_TYPE):

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

    mensaje = "📅 **Movimientos de hoy**\n\n"

    total = 0
    print(movimientos_hoy)
    for movimiento in movimientos_hoy:

        monto = float(movimiento["Monto"])
        total += monto

        mensaje += (
            f"{movimiento['Categoria']} "
            f"{movimiento['Descripcion']} "
            f"$ {monto:,.0f}\n"
        )

    mensaje += (
        f"\n──────────────\n"
        f"💰 Total: $ {total:,.0f}"
    )

    await update.message.reply_text(mensaje)