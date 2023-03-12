import logging
import traceback
import pulsar, _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from . import utils
import json
import uuid
from sagalog.repositorio import TransactionSagaRepository
import time
import datetime

def time_millis():
    return int(time.time() * 1000)

async def suscribirse_a_topico(topico: str, suscripcion: str, evento: str, estado: str, schema: str, tipo_consumidor:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared, eventos=[]):
    try:
        avro_schema = get_avro_schema(evento)
        async with aiopulsar.connect(
            f'pulsar+ssl://{utils.broker_host()}:6651',
            authentication=pulsar.AuthenticationToken(utils.get_token())
        ) as cliente:
        # async with aiopulsar.connect(
        #     f'pulsar://localhost:6650',
        # ) as cliente:
            async with cliente.subscribe(
                topico, 
                consumer_type=tipo_consumidor,
                subscription_name=suscripcion, 
                schema=avro_schema
            ) as consumidor:
                while True:
                    mensaje = await consumidor.receive()
                    print(mensaje)
                    datos = mensaje.value()
                    print(f'Evento recibido: {datos}')
                    eventos.append(str(datos))
                    TransactionSagaRepository.guardarTrasanccion(datos, evento, estado)
                    await consumidor.acknowledge(mensaje)

    except:
        logging.error(f'ERROR: Suscribiendose al tópico! {topico}, {suscripcion}, {schema}')
        traceback.print_exc()

def get_avro_schema(evento):
    if evento == 'OrdenCreada':
        return AvroSchema(EventoOrdenCreada)
    if evento == 'OrdenAlistada':
        return AvroSchema(EventoOrdenAlistada)
    if evento == 'OrdenEntregada':
        return AvroSchema(EventoOrdenEntregada)


class EventoIntegracion(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()

#### EVENTO ORDEN CREADA ###

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
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = EventoOrdenCreadaPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

#### EVENTO ORDEN ALISTADA ###

class EventoOrdenAlistadaItem(Record):
    guid = String()
    direccion_centro_distribucion = String()
    direccion_entrega = String()
    tamanio = String()
    telefono = String()

class EventoOrdenAlistadaPayload(Record):
    guid = String()
    items = Array(EventoOrdenAlistadaItem())
    fecha_creacion = Long()

class EventoOrdenAlistada(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = EventoOrdenAlistadaPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


#### EVENTO ORDEN ENTREGADA ###

class EventoOrdenEntregadaItem(Record):
    guid = String()
    direccion_centro_distribucion = String()
    direccion_entrega = String()
    tamanio = String()
    telefono = String()

class EventoOrdenEntregadaPayload(Record):
    guid = String()
    items = Array(EventoOrdenEntregadaItem())
    fecha_creacion = Long()

class EventoOrdenEntregada(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = EventoOrdenEntregadaPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)