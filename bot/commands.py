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

    # Totales
    total_ingresos = 0
    total_gastos = 0

    # Gastos por categoría
    totales = defaultdict(float)

    # Gastos por medio de pago
    totales_pago = defaultdict(float)

    for movimiento in movimientos:

        fecha = datetime.strptime(
            movimiento["Fecha"],
            "%d/%m/%Y"
        )

        # Solo movimientos del mes actual
        if fecha.month != mes_actual or fecha.year != año_actual:
            continue

        monto = float(movimiento["Monto"])

        tipo = movimiento.get("Tipo", "").strip().lower()

        # -------------------------
        # INGRESOS
        # -------------------------

        if tipo == "ingreso":

            total_ingresos += monto

            continue

        # -------------------------
        # GASTOS
        # -------------------------

        if tipo == "gasto":

            total_gastos += monto

            # Acumular por categoría
            categoria = movimiento.get(
                "Categoria",
                "Sin categoría"
            )

            totales[categoria] += monto

            # Acumular por medio de pago
            medio_pago = movimiento.get(
                "MedioPago",
                ""
            ).strip()

            if medio_pago:
                totales_pago[medio_pago] += monto

    # Si no hubo ni ingresos ni gastos
    if total_ingresos == 0 and total_gastos == 0:

        await update.message.reply_text(
            "📅 Este mes no registraste movimientos."
        )

        return

    # -------------------------
    # NOMBRES DE LOS MESES
    # -------------------------

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
    # INGRESOS
    # -------------------------

    mensaje += (
        f"💰 Ingresos: $ {total_ingresos:,.0f}\n\n"
    )

    # -------------------------
    # GASTOS POR CATEGORÍA
    # -------------------------

    if totales:

        mensaje += "💸 Gastos por categoría\n\n"

        for categoria, monto in sorted(
            totales.items(),
            key=lambda x: x[1],
            reverse=True,
        ):

            mensaje += (
                f"{categoria:<18}"
                f"$ {monto:,.0f}\n"
            )

    # -------------------------
    # TOTAL Y DISPONIBLE
    # -------------------------

    disponible = total_ingresos - total_gastos

    mensaje += (
        f"\n────────────────\n"
        f"💸 Total gastos: $ {total_gastos:,.0f}\n"
        f"💵 Disponible:   $ {disponible:,.0f}\n"
    )

    # -------------------------
    # MEDIO DE PAGO
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

@requiere_autorizacion
async def ingreso(update: Update, context: ContextTypes.DEFAULT_TYPE):

    sheets = obtener_sheets(update.effective_user.id)

    # Verificar que se haya ingresado un monto
    if not context.args:

        await update.message.reply_text(
            "💰 Indicá el monto del ingreso.\n\n"
            "Ejemplo:\n"
            "/ingreso 750000"
        )

        return

    try:

        monto = float(
            context.args[0]
            .replace(".", "")
            .replace(",", ".")
        )

    except ValueError:

        await update.message.reply_text(
            "⚠️ El monto ingresado no es válido.\n\n"
            "Ejemplo:\n"
            "/ingreso 750000"
        )

        return

    if monto <= 0:

        await update.message.reply_text(
            "⚠️ El monto debe ser mayor a cero."
        )

        return

    # Guardar ingreso
    sheets.agregar_movimiento(
        tipo="Ingreso",
        categoria="Ingreso",
        monto=monto,
        descripcion="Ingreso",
        medio_pago="",
        usuario=update.effective_user.id,
    )

    await update.message.reply_text(
        f"💰 Ingreso registrado\n\n"
        f"💵 $ {monto:,.0f}"
    )
