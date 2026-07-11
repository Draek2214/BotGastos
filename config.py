from pathlib import Path

# Carpeta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Google
SPREADSHEET_NAME = "Gastos Mensuales"

MOVIMIENTOS_SHEET = "Movimientos"
CATEGORIAS_SHEET = "Categorias"

CREDENTIALS_FILE = BASE_DIR / "credentials.json"

# Bot
BOT_NAME = "Bot Gastos"