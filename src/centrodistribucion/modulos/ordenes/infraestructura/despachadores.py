import pulsar
from pulsar.schema import *
from centrodistribucion.modulos.ordenes.infraestructura.mapeadores import EventoDominioAIntegracion

from centrodistribucion.modulos.ordenes.infraestructura.schema.v1.eventos import EventoOrdenAlistada, EventoOrdenAlistadaPayload, EventoOrdenCreadaCompensacion
from centrodistribucion.seedwork.infraestructura import utils

# from centrodistribucion.modulos.ordenes.infraestructura.mapeadores import MapadeadorEventosReserva

class Despachador:
    def __init__(self):
        # self.mapper = MapadeadorEventosReserva()
        ...

    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'{utils.broker_connection_string()}', authentication=utils.broker_auth())
        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoOrdenAlistada))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        #Transformar a Evento de Dominio a integracion
        evento = EventoDominioAIntegracion(evento)
        evento.sim_error = utils.get_sim_error(evento.data.guid)
        self._publicar_mensaje(evento, topico, AvroSchema(evento.__class__))


class DespachadorCompensacion:
    def __init__(self):
        ...

    def _publicar_mensaje(self, mensaje, topico):
        cliente = pulsar.Client(
            f'{utils.broker_connection_string()}', authentication=utils.broker_auth())
        publicador = cliente.create_producer(
            topico, schema=AvroSchema(EventoOrdenCreadaCompensacion))
        publicador.send(mensaje)
        cliente.close()
