import pulsar
from pulsar.schema import *

from dataclasses import dataclass
from datetime import datetime
import uuid
import time

from . import utils

def time_millis():
    return int(time.time() * 1000)

class Despachador:
    def __init__(self):
        ...

    async def publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(
            f'{utils.broker_connection_string()}',
            authentication=utils.broker_auth())
        publicador = cliente.create_producer(topico, schema=AvroSchema(ComandoCrearOrden))
        publicador.send(mensaje)
        cliente.close()

class ComandoIntegracion(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()

class ComandoCrearOrdenItem(Record):
    direccion_recogida = String()
    direccion_entrega = String()
    tamanio = String()
    telefono = String()

class ComandoCrearOrdenPayload(Record):
    items = Array(ComandoCrearOrdenItem())

class ComandoCrearOrden(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ComandoCrearOrdenPayload()
    sim_error = String()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)