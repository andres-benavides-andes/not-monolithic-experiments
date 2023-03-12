from __future__ import annotations
from dataclasses import dataclass, field
from ordenes.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime
import uuid
from typing import List

class EventoOrden(EventoDominio):
    ...

@dataclass
class OrdenCreada(EventoOrden):
    guid: str = None
    fecha_creacion: str = None
    items: List[OrdenCreadaItems] = None


@dataclass
class OrdenCreadaItems:
    guid: str = None
    direccion_recogida: str = None
    direccion_entrega: str = None
    tamanio: str = None
    telefono: str = None