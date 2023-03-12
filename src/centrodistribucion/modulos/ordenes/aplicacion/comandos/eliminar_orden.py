import logging
import traceback
from centrodistribucion.modulos.ordenes.aplicacion.comandos.base import AlistarOrdenBaseHandler
from centrodistribucion.modulos.ordenes.dominio.repositorios import RepositorioEventosOrdenes, RepositorioOrdenes
from centrodistribucion.modulos.ordenes.infraestructura.despachadores import DespachadorCompensacion
from centrodistribucion.modulos.ordenes.infraestructura.schema.v1.eventos import EventoOrdenCreadaCompensacion, EventoOrdenCreadaCompensacionPayload


class EliminarOrdenHandler(AlistarOrdenBaseHandler):
    
    def handle(self, orden_guid: str):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosOrdenes)

        try:
            repositorio_eventos.eliminar(orden_guid)
            repositorio.eliminar(orden_guid)
            despachador = DespachadorCompensacion()
            despachador._publicar_mensaje(
                mensaje=EventoOrdenCreadaCompensacion(
                    data=EventoOrdenCreadaCompensacionPayload(
                        guid=orden_guid
                    )
                ),
                topico="eventos-orden-compensacion",
            )
        except:
            logging.error('ERROR: La transaccion de compensacion no se pudo realizar!')
            traceback.print_exc()
            
            