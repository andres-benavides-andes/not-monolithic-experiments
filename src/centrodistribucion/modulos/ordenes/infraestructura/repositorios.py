import datetime
from centrodistribucion.config.db import db, session
from centrodistribucion.modulos.ordenes.dominio.eventos import OrdenAlistada
from centrodistribucion.modulos.ordenes.dominio.repositorios import RepositorioOrdenes, RepositorioEventosOrdenes
from centrodistribucion.modulos.ordenes.dominio.entidades import Orden, OrdenItems
from centrodistribucion.modulos.ordenes.infraestructura.mapeadores import EventoDominioAIntegracion
from centrodistribucion.modulos.ordenes.infraestructura.schema.v1.eventos import EventoOrdenAlistadaItem, EventoOrdenAlistadaPayload, EventoOrdenAlistada
from .dto import Orden as OrdenDTO
from .dto import Paquete as PaqueteDTO
from .dto import EventosOrden
from uuid import UUID
from pulsar.schema import *

from typing import List

class RepositorioOrdenesSQLAlchemy(RepositorioOrdenes):
    def obtener_por_id(self, id: UUID) -> Orden:
        orden_dto = db.session.query(OrdenDTO).filter_by(guid=str(id)).one()
        # TODO
        raise NotImplementedError

    def obtener_todos(self) -> List[Orden]:
        # TODO
        raise NotImplementedError

    def agregar(self, orden: Orden):
        # orden_dto = self.fabrica_vuelos.crear_objeto(orden, Mapeadororden())
        orden_dto = OrdenDTO()
        orden_dto.fecha_creacion = datetime.datetime.fromtimestamp(orden.fecha_creacion)
        orden_dto.guid = orden.guid

        orden_dto.items = []
        for item in orden.items:
            paquete_dto = PaqueteDTO()
            paquete_dto.direccion_centro_distribucion = item.direccion_centro_distribucion
            paquete_dto.direccion_entrega = item.direccion_entrega
            paquete_dto.guid = item.guid
            paquete_dto.orden_guid = orden.guid
            paquete_dto.tamanio = item.tamanio
            paquete_dto.telefono = item.telefono
            orden_dto.items.append(paquete_dto)
        
        session.add(orden_dto)

    def actualizar(self, orden: Orden):
        # TODO
        raise NotImplementedError

    def eliminar(self, orden_id: UUID):
        # TODO
        raise NotImplementedError

class RepositorioEventosOrdenesSQLAlchemy(RepositorioEventosOrdenes):
    def obtener_por_id(self, id: UUID) -> Orden:
        orden_dto = db.session.query(OrdenDTO).filter_by(id=str(id)).one()
        raise NotImplementedError

    def obtener_todos(self) -> List[Orden]:
        raise NotImplementedError

    def agregar(self, evento):
        # De evento de OrdeAlistada a Evento de Integracion
        if (isinstance(evento, OrdenAlistada)):
            evento_dominio: OrdenAlistada = evento
            orden_evento = EventoDominioAIntegracion(evento_dominio)

            parser_payload = JsonSchema(orden_evento.data.__class__)
            json_str = parser_payload.encode(orden_evento.data)

            evento_dto = EventosOrden()
            evento_dto.id = str(evento_dominio.id)
            evento_dto.id_entidad = str(evento.guid)
            evento_dto.fecha_evento = datetime.datetime.fromtimestamp(int(evento.fecha_creacion))
            evento_dto.version = str(orden_evento.specversion)
            evento_dto.tipo_evento = evento.__class__.__name__
            evento_dto.formato_contenido = 'JSON'
            evento_dto.nombre_servicio = str(orden_evento.service_name)
            evento_dto.contenido = json_str
            
            session.add(evento_dto)
        else:
            raise NotImplementedError()



    def actualizar(self, orden: Orden):
        raise NotImplementedError

    def eliminar(self, orden_id: UUID):
        raise NotImplementedError