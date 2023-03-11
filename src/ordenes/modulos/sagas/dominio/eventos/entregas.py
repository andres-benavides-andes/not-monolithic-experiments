from __future__ import annotations
from dataclasses import dataclass, field
from aeroalpes.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoEntrega(EventoDominio):
    ...

@dataclass
class OrdenEntregada(EventoEntrega):
    id_reserva: uuid.UUID = None
    id_correlacion: str = None
    fecha_actualizacion: datetime = None

@dataclass
class CancelarOrden(EventoEntrega):
    id_reserva: uuid.UUID = None
    id_correlacion: str = None
    fecha_actualizacion: datetime = None