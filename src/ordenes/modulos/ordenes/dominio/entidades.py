"""Entidades del dominio de ordenes

"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List

from ordenes.modulos.ordenes.dominio.eventos import OrdenCreada
from ordenes.seedwork.dominio.entidades import AgregacionRaiz, Entidad


@dataclass
class OrdenItems(Entidad):
    guid: str = None
    direccion_recogida: str = None
    direccion_entrega: str = None
    tamanio: str = None
    telefono: str = None


@dataclass
class Orden(AgregacionRaiz):
    guid: str = None
    fecha_creacion: str = None
    items: List[OrdenItems] = None

    def crear_orden(self, orden: Orden):
        self.guid = orden.guid
        self.fecha_creacion = orden.fecha_creacion
        self.items = orden.items

        self.agregar_evento(OrdenCreada(
            fecha_creacion=self.fecha_creacion,
            guid=self.guid,
            items=self.items,
        ))