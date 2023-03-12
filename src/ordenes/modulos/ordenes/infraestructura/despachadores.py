import pulsar
from pulsar.schema import *
from ordenes.modulos.ordenes.infraestructura.mapeadores import EventoDominioAIntegracion

from ordenes.modulos.ordenes.infraestructura.schema.v1.eventos import EventoOrdenCreada
from ordenes.seedwork.infraestructura import utils

# from ordenes.modulos.ordenes.infraestructura.mapeadores import MapadeadorEventosReserva

class Despachador:
    def __init__(self):
        # self.mapper = MapadeadorEventosReserva()
        ...

    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'{utils.broker_connection_string()}', authentication=utils.broker_auth())

        publicador = cliente.create_producer(topico, schema=AvroSchema(EventoOrdenCreada))
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento(self, evento, topico):
        #Transformar a Evento de Dominio a integracion
        evento = EventoDominioAIntegracion(evento)

        self._publicar_mensaje(evento, topico, AvroSchema(evento.__class__))