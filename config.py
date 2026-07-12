from pathlib import Path

# ==========================================================
# Rutas
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

CREDENTIALS_FILE = BASE_DIR / "credentials.json"

# ==========================================================
# Google Sheets
# ==========================================================

SPREADSHEET_NAME = "Gastos Mensuales"

MOVIMIENTOS_SHEET = "Movimientos"
CATEGORIAS_SHEET = "Categorias"

# ==========================================================
# Encabezados de la hoja Movimientos
# ==========================================================

COL_ID = "ID"
COL_FECHA = "Fecha"
COL_HORA = "Hora"
COL_TIPO = "Tipo"
COL_CATEGORIA = "Categoria"
COL_MONTO = "Monto"
COL_DESCRIPCION = "Descripcion"
COL_USUARIO = "Usuario"

# ==========================================================
# Encabezados de la hoja Categorias
# ==========================================================

COL_TEXTO = "Texto"
COL_CATEGORIA_NOMBRE = "Categoría"

# ==========================================================
# Bot
# ==========================================================

BOT_NAME = "Bot Gastos"

DATE_FORMAT = "%d/%m/%Y"
TIME_FORMAT = "%H:%M"