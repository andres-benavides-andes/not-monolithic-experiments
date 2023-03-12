import datetime
import pulsar
import _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import uuid

from saga.modulos.sagas.infraestructura.eventos import EventoOrdenCreada
from saga.seedwork.infraestructura import utils

def suscribirse_a_eventos_orden():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-orden', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='ordenes-sub-eventos', schema=AvroSchema(EventoOrdenCreada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento Orden Creada recibida: {mensaje.value().data}')
            
            orden_dto = mensaje.value().data
            
            cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()