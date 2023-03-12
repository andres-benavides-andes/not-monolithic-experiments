from centrodistribucion.seedwork.aplicacion.comandos import Comando
from .base import AlistarOrdenBaseHandler
from dataclasses import dataclass, field
from centrodistribucion.seedwork.aplicacion.comandos import ejecutar_commando as comando
from typing import List

from centrodistribucion.modulos.ordenes.dominio.entidades import Orden, OrdenItems
from centrodistribucion.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from centrodistribucion.modulos.ordenes.dominio.repositorios import RepositorioOrdenes, RepositorioEventosOrdenes

@dataclass
class AlistarOrdenItems:
    guid: str
    direccion_centro_distribucion: str
    direccion_entrega: str
    tamanio: str
    telefono: str

@dataclass
class AlistarOrden(Comando):
    guid: str
    fecha_creacion: str
    items: List[AlistarOrdenItems]

class AlistarOrdenHandler(AlistarOrdenBaseHandler):
    
    def handle(self, comando: AlistarOrden):
        orden: Orden = Orden (
            guid=comando.guid,
            fecha_creacion=comando.fecha_creacion,
            items=[
                OrdenItems(
                    guid=item.guid,
                    direccion_centro_distribucion=item.direccion_centro_distribucion,
                    direccion_entrega=item.direccion_entrega,
                    tamanio=item.tamanio,
                    telefono=item.telefono
                ) for item in comando.items
            ]
        )

        orden.alistar_orden(orden)
        # Escribe en las tablas el evento y el objeto
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosOrdenes)

        UnidadTrabajoPuerto.registrar_batch(repositorio.agregar, orden, repositorio_eventos_func=repositorio_eventos.agregar)
        UnidadTrabajoPuerto.commit()
        UnidadTrabajoPuerto.clean_session()


@comando.register(AlistarOrden)
def ejecutar_comando_alistar_orden(comando: AlistarOrden):
    handler = AlistarOrdenHandler()
    handler.handle(comando)
