import logging
import traceback
from ordenes.modulos.ordenes.aplicacion.comandos.base import CrearOrdenBaseHandler

from ordenes.modulos.ordenes.dominio.repositorios import RepositorioOrdenes, RepositorioEventosOrdenes


class EliminarOrdenHandler(CrearOrdenBaseHandler):
    
    def handle(self, orden_guid: str):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        repositorio_eventos = self.fabrica_repositorio.crear_objeto(RepositorioEventosOrdenes)

        try:
            repositorio_eventos.eliminar(orden_guid)
            repositorio.eliminar(orden_guid)
            # No hay que despachar ningun otro evento, porque en ordenes ya finaliza
        except:
            logging.error('ERROR: La transaccion de compensacion no se pudo realizar!')
            traceback.print_exc()
            
            