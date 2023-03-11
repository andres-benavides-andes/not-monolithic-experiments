from aeroalpes.seedwork.aplicacion.sagas import CoordinadorOrquestacion, Transaccion, Inicio, Fin
from aeroalpes.seedwork.aplicacion.comandos import Comando
from aeroalpes.seedwork.dominio.eventos import EventoDominio


from ordenes.modulos.sagas.aplicacion.comandos.centrodistribucion import AlistarOrden, DesalistarOrden
from ordenes.modulos.sagas.aplicacion.comandos.entregas import EntregarOrden, CancelarEntrega
from ordenes.modulos.ordenes.aplicacion.comandos.crear_orden import CrearOrden
from ordenes.modulos.ordenes.dominio.eventos import OrdenCreada, CreacionOrdenFallida
from ordenes.modulos.sagas.dominio.eventos.centrodistribucion import OrdenAlistada, OrdenDesAlistada
from ordenes.modulos.sagas.dominio.eventos.entregas import OrdenEntregada, CancelarOrden


class CoordinadorOrdenes(CoordinadorOrquestacion):

    def inicializar_pasos(self):
        self.pasos = [
            Inicio(index=0),
            Transaccion(index=1, comando=CrearOrden, evento=OrdenCreada, error=CreacionOrdenFallida, compensacion=None),          
            Transaccion(index=2, comando=AlistarOrden, evento=OrdenAlistada, error=OrdenDesAlistada, compensacion=DesalistarOrden),
            Transaccion(index=3, comando=EntregarOrden, evento=OrdenEntregada, error=CancelarOrden, compensacion=CancelarEntrega),
            Fin(index=5)
        ]

    def iniciar(self):
        self.persistir_en_saga_log(self.pasos[0])
    
    def terminar():
        self.persistir_en_saga_log(self.pasos[-1])

    def persistir_en_saga_log(self, mensaje):
        # TODO-SAGA Persistir estado en DB
        # Probablemente usted podría usar un repositorio para ello
        ...

    def construir_comando(self, evento: EventoDominio, tipo_comando: type):
        # TODO-SAGA Transforma un evento en la entrada de un comando
        # Por ejemplo si el evento que llega es ReservaCreada y el tipo_comando es PagarReserva
        # Debemos usar los atributos de ReservaCreada para crear el comando PagarReserva
        ...


# TODO-SAGA Agregue un Listener/Handler para que se puedan redireccionar eventos de dominio
def oir_mensaje(mensaje):
    if isinstance(mensaje, EventoDominio):
        coordinador = CoordinadorReservas()
        coordinador.procesar_evento(mensaje)
    else:
        raise NotImplementedError("El mensaje no es evento de Dominio")