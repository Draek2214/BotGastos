import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from config import CREDENTIALS_FILE

class SheetsService:

    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self, spreadsheet_id):

        self.credenciales = Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=self.SCOPES,
    )

        self.cliente = gspread.authorize(self.credenciales)

        self.spreadsheet = self.cliente.open_by_key(
        spreadsheet_id
    )

        self.movimientos = self.spreadsheet.worksheet("Movimientos")
        self.categorias = self.spreadsheet.worksheet("Categorias")

        # Caché en memoria
        self.cache_categorias = {}

        self._cargar_categorias()

    # --------------------------------------------------

    def _cargar_categorias(self):

        self.cache_categorias.clear()

        datos = self.categorias.get_all_records()

        for fila in datos:

            texto = fila["Texto"].strip().lower()

            categoria = fila["Categoría"]

            self.cache_categorias[texto] = categoria

    # --------------------------------------------------

    def agregar_movimiento(
        self,
        tipo,
        categoria,
        monto,
        descripcion,
        medio_pago,
        usuario,
    ):

        ahora = datetime.now()

        self.movimientos.append_row(
            [
                "",
                ahora.strftime("%d/%m/%Y"),
                ahora.strftime("%H:%M"),
                tipo,
                categoria,
                monto,
                descripcion,
                medio_pago,
                usuario,
            ]
        )

    # --------------------------------------------------

    def buscar_categoria(self, descripcion):

        descripcion = descripcion.lower()

        for texto, categoria in self.cache_categorias.items():

            if texto in descripcion:

                return categoria

        return None

    # --------------------------------------------------

    def guardar_categoria(self, texto, categoria):

        texto = texto.strip()

        if texto.lower() in self.cache_categorias:
            return

        self.categorias.append_row(
            [
                texto,
                categoria,
            ]
        )

        # Actualizar la caché sin volver a leer la hoja
        self.cache_categorias[texto.lower()] = categoria

    # --------------------------------------------------

    def obtener_movimientos(self):

        datos = self.movimientos.get_all_records()

        movimientos = []

        for numero_fila, fila in enumerate(datos, start=2):

            fila["_fila"] = numero_fila

            try:

                fila["Monto"] = float(str(fila["Monto"]).replace(",", "."))

            except:

                fila["Monto"] = 0

            movimientos.append(fila)

        return movimientos
    # --------------------------------------------------

    def obtener_ultimo_movimiento(self):

        movimientos = self.obtener_movimientos()
        
        

        if not movimientos:
            return None

        return movimientos[-1]
    
    def eliminar_movimiento(self, fila):

        self.movimientos.delete_rows(fila)
