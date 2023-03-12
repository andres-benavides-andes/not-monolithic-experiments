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

from sagalog.eventos.evento_integracion import EventoIntegracion
from sagalog.eventos.eventos_orden import EventoOrdenCreada, EventoOrdenCreadaCompensacion
from sagalog.eventos.eventos_centrodistribucion import EventoOrdenAlistada, EventoOrdenAlistadaCompensacion
from sagalog.eventos.eventos_entregas import EventoOrdenEntregada

def time_millis():
    return int(time.time() * 1000)

async def suscribirse_a_topico(topico: str, suscripcion: str, evento: str, estado: str, schema: str, tipo_consumidor:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared, eventos=[]):
    try:
        avro_schema = get_avro_schema(evento)
        async with aiopulsar.connect(
            f'pulsar+ssl://{utils.broker_host()}:6651',
            authentication=utils.get_pulsar_auth()
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
    if evento == 'CancelarOrden':
        return AvroSchema(EventoOrdenCreadaCompensacion)
    if evento == 'OrdenDesAlistada':
        return AvroSchema(EventoOrdenAlistadaCompensacion)
