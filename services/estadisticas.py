import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

credenciales = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES,
)

cliente = gspread.authorize(credenciales)

# CAMBIAR POR EL NOMBRE DE TU DOCUMENTO
SHEET_NAME = "Gastos Mensuales"

hoja = cliente.open(SHEET_NAME).sheet1


def agregar_gasto(monto, descripcion):
    ahora = datetime.now()

    hoja.append_row([
        ahora.strftime("%d/%m/%Y"),
        ahora.strftime("%H:%M"),
        monto,
        descripcion
    ])

    print("Fila agregada correctamente.")