from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineKeyboardMarkup

from services.categorias import CATEGORIAS
from services.medios_pago import MEDIOS_PAGO

def teclado_categorias():

    teclado = []

    fila = []

    for i, categoria in enumerate(CATEGORIAS):

        fila.append(
            InlineKeyboardButton(
                categoria,
                callback_data=f"cat_{i}"
            )
        )

        if len(fila) == 2:
            teclado.append(fila)
            fila = []

    if fila:
        teclado.append(fila)

    return InlineKeyboardMarkup(teclado)

def teclado_ultimo(fila):

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🗑️ Eliminar",
                    callback_data=f"eliminar_{fila}"
                )
            ]
        ]
    )
    

def teclado_medios_pago():

    botones = []

    for i, medio in enumerate(MEDIOS_PAGO):
        botones.append([
            InlineKeyboardButton(
                medio,
                callback_data=f"medio_{i}"
            )
        ])

    return InlineKeyboardMarkup(botones)