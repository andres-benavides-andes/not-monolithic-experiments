from __future__ import annotations
from dataclasses import dataclass, field
from ordenes.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime
import uuid
from typing import List


class EventoEntrega(EventoDominio):
    ...

@dataclass
class OrdenEntregada(EventoEntrega):
    guid: str = None
    fecha_creacion: str = None
    items: List[EntregarOrdenItems] = None

@dataclass
class CancelarOrden(EventoEntrega):
    guid: str = None
    fecha_actualizacion: datetime = None

@dataclass
class EntregarOrdenItems:
    guid: str = None
    fecha_entrega: str = None
    direccion_entrega: str = None
    persona_recibe: str = None
    mecanismo_entrega: str = None