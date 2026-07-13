from services.sheets import SheetsService

USUARIOS = {
    1324935960: "1OuikAiIxV6PBhxaAjbIlZ1K4yLJDpFIQPy1Um1SJlBc",
    7894192209: "1OuikAiIxV6PBhxaAjbIlZ1K4yLJDpFIQPy1Um1SJlBc",
}

_instancias = {}


def obtener_sheets(usuario):

    if usuario not in USUARIOS:
        raise Exception("Usuario no autorizado.")

    if usuario not in _instancias:
        _instancias[usuario] = SheetsService(
            USUARIOS[usuario]
        )

    return _instancias[usuario]