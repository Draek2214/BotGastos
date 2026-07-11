import re


def interpretar(texto: str):

    texto = texto.strip()

    patron = r"(\d+(?:[.,]\d+)?)\s+(.+)"

    resultado = re.match(patron, texto)

    if not resultado:
        return None

    monto = float(resultado.group(1).replace(",", "."))

    descripcion = resultado.group(2)

    return monto, descripcion