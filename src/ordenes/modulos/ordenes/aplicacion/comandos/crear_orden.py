from ordenes.seedwork.aplicacion.comandos import Comando
from .base import CrearOrdenBaseHandler
from dataclasses import dataclass, field
from ordenes.seedwork.aplicacion.comandos import ejecutar_commando as comando
from typing import List

from ordenes.modulos.ordenes.dominio.entidades import Orden, OrdenItems
from ordenes.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from ordenes.modulos.ordenes.dominio.repositorios import RepositorioOrdenes, RepositorioEventosOrdenes

@dataclass
class CrearOrdenItems:
    guid: str
    direccion_recogida: str
    direccion_entrega: str
    tamanio: str
    telefono: str

@dataclass
class CrearOrden(Comando):
    guid: str
    fecha_creacion: str
    items: List[CrearOrdenItems]

class CrearOrdenHandler(CrearOrdenBaseHandler):
    
    def handle(self, comando: CrearOrden):
        orden: Orden = Orden (
            guid=comando.guid,
            fecha_creacion=comando.fecha_creacion,
            items=[
                OrdenItems(
                    guid=item.guid,
                    direccion_recogida=item.direccion_recogida,
                    direccion_entrega=item.direccion_entrega,
                    tamanio=item.tamanio,
                    telefono=item.telefono
                ) for item in comando.items
            ]
        )

        orden.crear_orden(orden)
        # Escribe en las tablas el evento y el objeto
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosOrdenes)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, orden, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()
        UnidadTrabajoPuerto.clean_session()


@comando.register(CrearOrden)
def ejecutar_comando_crear_orden(comando: CrearOrden):
    handler = CrearOrdenHandler()
    handler.handle(comando)