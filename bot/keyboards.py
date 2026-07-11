from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup

from services.categorias import CATEGORIAS


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