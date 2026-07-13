from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Estamos en Home Assistant solamente si existe esta variable
HA_ADDON = os.getenv("SUPERVISOR_TOKEN") is not None

if HA_ADDON:
    CONFIG_DIR = Path("/data")
else:
    CONFIG_DIR = BASE_DIR

ENV_FILE = CONFIG_DIR / ".env"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"