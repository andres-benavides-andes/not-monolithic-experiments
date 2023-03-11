from __future__ import annotations
from dataclasses import dataclass, field
from ordenes.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoOrden(EventoDominio):
    ...


@dataclass
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
    

# TODO-SAGA mapear evento
@dataclass
class OrdenDesAlistada(EventoOrden):
    id_orden: uuid.UUID = None
    fecha_actualizacion: datetime = None


