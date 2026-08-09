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

    fecha_hoy = datetime.now().strftime("%d/%m/%Y")

    movimientos = sheets.obtener_movimientos()

    movimientos_hoy = [
        m for m in movimientos
        if m["Fecha"] == fecha_hoy
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
async def ultimo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sheets = obtener_sheets(update.effective_user.id)
    movimiento = sheets.obtener_ultimo_movimiento()

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
y seguir los pasos de las respuestas del bot.

📅 Comandos disponibles

/hoy - Muestra los movimientos de hoy.

/mes - Muestra los movimientos del mes.

/mesanterior - Muestra los movimientos del mes anterior.

/ultimo - Muestra el último movimiento registrado.

/ayuda - Muestra esta ayuda.
"""


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        mensaje_ayuda()
    )

@requiere_autorizacion
async def mes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sheets = obtener_sheets(update.effective_user.id)

    hoy = datetime.now()

    # Mes y año en curso
    mes_actual = hoy.month
    año_actual = hoy.year

    movimientos = sheets.obtener_movimientos()

    # Totales por categoría
    totales = defaultdict(float)

    # Totales por medio de pago
    totales_pago = defaultdict(float)

    for movimiento in movimientos:

        fecha = datetime.strptime(
            movimiento["Fecha"],
            "%d/%m/%Y"
        )

        # Solo movimientos del mes en curso
        if fecha.month != mes_actual or fecha.year != año_actual:
            continue

        monto = float(movimiento["Monto"])

        # Acumular por categoría
        totales[movimiento["Categoria"]] += monto

        # Acumular por medio de pago
        medio_pago = movimiento.get("MedioPago", "").strip()

        if medio_pago:
            totales_pago[medio_pago] += monto

    if not totales:

        await update.message.reply_text(
            "📅 Este mes no registraste movimientos."
        )

        return

    # Nombres de los meses
    nombres_meses = [
        "",
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre"
    ]

    nombre_mes = nombres_meses[mes_actual]

    mensaje = (
        f"📅 Resumen de {nombre_mes} {año_actual}\n\n"
    )

    # -------------------------
    # RESUMEN POR CATEGORÍA
    # -------------------------

    for categoria, monto in sorted(
        totales.items(),
        key=lambda x: x[1],
        reverse=True,
    ):

        mensaje += (
            f"{categoria:<18}"
            f"$ {monto:,.0f}\n"
        )

    total = sum(totales.values())

    mensaje += (
        f"\n────────────────\n"
        f"💰 Total: $ {total:,.0f}\n"
    )

    # -------------------------
    # RESUMEN POR MEDIO DE PAGO
    # -------------------------

    if totales_pago:

        mensaje += "\n💳 Por medio de pago\n\n"

        for medio_pago, monto in sorted(
            totales_pago.items(),
            key=lambda x: x[1],
            reverse=True,
        ):

            mensaje += (
                f"{medio_pago:<18}"
                f"$ {monto:,.0f}\n"
            )

        mensaje += (
            f"\n────────────────\n"
            f"💰 Total: $ {sum(totales_pago.values()):,.0f}"
        )

    await update.message.reply_text(mensaje)

@requiere_autorizacion
async def mesanterior(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sheets = obtener_sheets(update.effective_user.id)

    hoy = datetime.now()

    # Calcular mes anterior
    if hoy.month == 1:
        mes_anterior = 12
        año_anterior = hoy.year - 1
    else:
        mes_anterior = hoy.month - 1
        año_anterior = hoy.year

    movimientos = sheets.obtener_movimientos()

    # Totales por categoría
    totales = defaultdict(float)

    # Totales por medio de pago
    totales_pago = defaultdict(float)

    for movimiento in movimientos:

        fecha = datetime.strptime(
            movimiento["Fecha"],
            "%d/%m/%Y"
        )

        if fecha.month != mes_anterior or fecha.year != año_anterior:
            continue

        monto = float(movimiento["Monto"])

        # Acumular por categoría
        totales[movimiento["Categoria"]] += monto

        # Acumular por medio de pago
        medio_pago = movimiento.get("MedioPago", "").strip()

        if medio_pago:
            totales_pago[medio_pago] += monto

    if not totales:

        await update.message.reply_text(
            "📅 El mes anterior no registraste movimientos."
        )

        return

    # Nombres de los meses
    nombres_meses = [
        "",
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre"
    ]

    nombre_mes = nombres_meses[mes_anterior]

    mensaje = (
        f"📅 Resumen de {nombre_mes} {año_anterior}\n\n"
    )

    # -------------------------
    # RESUMEN POR CATEGORÍA
    # -------------------------

    for categoria, monto in sorted(
        totales.items(),
        key=lambda x: x[1],
        reverse=True,
    ):

        mensaje += (
            f"{categoria:<18}"
            f"$ {monto:,.0f}\n"
        )

    mensaje += "\n────────────────\n"

    total = sum(totales.values())

    mensaje += f"💰 Total: $ {total:,.0f}\n"

    # -------------------------
    # RESUMEN POR MEDIO DE PAGO
    # -------------------------

    if totales_pago:

        mensaje += "\n💳 Por medio de pago\n\n"

        for medio_pago, monto in sorted(
            totales_pago.items(),
            key=lambda x: x[1],
            reverse=True,
        ):

            mensaje += (
                f"{medio_pago:<18}"
                f"$ {monto:,.0f}\n"
            )

        mensaje += (
            f"\n────────────────\n"
            f"💰 Total: $ {sum(totales_pago.values()):,.0f}"
        )

    await update.message.reply_text(mensaje)