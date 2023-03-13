import pulsar
from pulsar.schema import *
from dataclasses import dataclass
from datetime import datetime
import uuid
import time

def time_millis():
    return int(time.time() * 1000)

def _consumir_mensajes(topico, schema):
    cliente = pulsar.Client('pulsar://localhost:6650')
    consumidor = cliente.subscribe(topico, subscription_name="centrodistribucion-sub-eventos", schema=AvroSchema(EventoOrdenCreada))
    
    while True:
        mensaje = consumidor.receive()
        print(f'Evento recibido: {mensaje.value().data}')

        consumidor.acknowledge(mensaje)

class EventoIntegracion(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()

class EventoOrdenCreadaItem(Record):
    guid = String()
    direccion_recogida = String()
    direccion_entrega = String()
    tamanio = String()
    telefono = String()

class EventoOrdenCreadaPayload(Record):
    guid = String()
    items = Array(EventoOrdenCreadaItem())
    fecha_creacion = Long()

class EventoOrdenCreada(EventoIntegracion):
    # NOTE La librería Record de Pulsar no es capaz de reconocer campos heredados, 
    # por lo que los mensajes al ser codificados pierden sus valores
    # Dupliqué el los cambios que ya se encuentran en la clase Mensaje
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = EventoOrdenCreadaPayload()
    sim_error = String()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


_consumir_mensajes('eventos-orden', AvroSchema(EventoOrdenCreada))