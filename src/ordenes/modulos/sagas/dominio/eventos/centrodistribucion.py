from __future__ import annotations
from dataclasses import dataclass, field
from aeroalpes.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoCentrodistribucion(EventoDominio):
    ...


@dataclass
class OrdenAlistada(EventoCentrodistribucion):
    id_reserva: uuid.UUID = None
    id_cliente: uuid.UUID = None
    estado: str = None
    fecha_creacion: datetime = None
    
@dataclass
class OrdenDesAlistada(EventoCentrodistribucion):
    id_reserva: uuid.UUID = None
    fecha_actualizacion: datetime = None


