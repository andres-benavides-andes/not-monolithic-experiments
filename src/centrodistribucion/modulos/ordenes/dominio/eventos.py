from __future__ import annotations
from dataclasses import dataclass, field
from centrodistribucion.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime
import uuid
from typing import List

class EventoOrden(EventoDominio):
    ...

@dataclass
class OrdenAlistada(EventoOrden):
    guid: str = None
    fecha_creacion: str = None
    items: List[AlistarOrdenItems] = None


@dataclass
class AlistarOrdenItems:
    guid: str = None
    direccion_centro_distribucion: str = None
    direccion_entrega: str = None
    tamanio: str = None
    telefono: str = None

# TODO-SAGA crear OrdenDesAlistada
@dataclass
class OrdenDesAlistada(EventoOrden):
    id_orden: uuid.UUID = None
    fecha_actualizacion: datetime = None
