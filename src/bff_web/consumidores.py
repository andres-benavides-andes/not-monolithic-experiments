import logging
import traceback
import pulsar, _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from . import utils
from bff_web.despachadores import ComandoCrearOrden

async def suscribirse_a_topico(topico: str, suscripcion: str, schema: str, tipo_consumidor:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared, eventos=[]):
    try:
        # json_schema = utils.consultar_schema_registry(schema)  
        avro_schema = AvroSchema(ComandoCrearOrden)
        print(f'HOSTTTTTTTTTTTTTT {get_token()}')
        async with aiopulsar.connect(
            f'pulsar+ssl://{broker_host()}:6651',
            authentication=pulsar.AuthenticationToken(get_token())
        ) as cliente:
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
                    await consumidor.acknowledge(mensaje)    

    except:
        logging.error(f'ERROR: Suscribiendose al tópico! {topico}, {suscripcion}, {schema}')
        traceback.print_exc()