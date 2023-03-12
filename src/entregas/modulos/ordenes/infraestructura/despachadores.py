import pulsar
from pulsar.schema import *
# TODO
from entregas.modulos.ordenes.infraestructura.mapeadores import EventoDominioAIntegracion

from entregas.modulos.ordenes.infraestructura.schema.v1.eventos import EventoOrdenEntregada, EventoOrdenEntregadaPayload, EventoOrdenAlistadaCompensacion, EventoOrdenAlistadaCompensacionPayload
from entregas.seedwork.infraestructura import utils


class Despachador:
    def __init__(self):
        # self.mapper = MapadeadorEventosReserva()
        ...

    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(
            f'{utils.broker_connection_string()}', authentication=utils.broker_auth())
        publicador = cliente.create_producer(
            topico, schema=AvroSchema(EventoOrdenEntregada))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        # Transformar a Evento de Dominio a integracion
        evento = EventoDominioAIntegracion(evento)

        self._publicar_mensaje(evento, topico, AvroSchema(evento.__class__))


class DespachadorCompensacion:
    def __init__(self):
        ...

    def _publicar_mensaje(self, mensaje, topico):
        cliente = pulsar.Client(
            f'{utils.broker_connection_string()}', authentication=utils.broker_auth())
        publicador = cliente.create_producer(
            topico, schema=AvroSchema(EventoOrdenAlistadaCompensacion))
        publicador.send(mensaje)
        cliente.close()
