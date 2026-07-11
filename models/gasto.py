from dataclasses import dataclass
from datetime import datetime


@dataclass
class Gasto:

    fecha: datetime
    monto: float
    descripcion: str
    categoria: str = ""
    tipo: str = "Gasto"
    usuario: int = 0