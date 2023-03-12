from __future__ import annotations
from dataclasses import dataclass, field
from entregas.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime
import uuid
from typing import List

class EventoOrden(EventoDominio):
    ...

@dataclass
class OrdenEntregada(EventoOrden):
    guid: str = None
    fecha_creacion: str = None
    items: List[EntregarOrdenItems] = None


@dataclass
class EntregarOrdenItems:
    guid: str = None
    fecha_entrega: str = None
    direccion_entrega: str = None
    persona_recibe: str = None
    mecanismo_entrega: str = None
