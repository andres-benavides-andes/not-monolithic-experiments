import logging
import traceback
import pulsar, _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from . import utils

async def suscribirse_a_topico(topico: str, suscripcion: str, schema: str, tipo_consumidor:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared, eventos=[]):
    try:
        json_schema = utils.consultar_schema_registry(schema)  
        avro_schema = utils.obtener_schema_avro_de_diccionario(json_schema)
        token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5rRXdSVVU1TUVOQlJrWTJNalEzTVRZek9FVkZRVVUyT0RNME5qUkRRVEU1T1VNMU16STVPUSJ9.eyJodHRwczovL3N0cmVhbW5hdGl2ZS5pby91c2VybmFtZSI6Im5vLW1vbm9saXRvcy1hY2NvdW50QG8tdmJrcnAuYXV0aC5zdHJlYW1uYXRpdmUuY2xvdWQiLCJpc3MiOiJodHRwczovL2F1dGguc3RyZWFtbmF0aXZlLmNsb3VkLyIsInN1YiI6Ik96OGNZUzlTSDZyb3NBNWNleG1BbTJOVlpsMzFXeGRrQGNsaWVudHMiLCJhdWQiOiJ1cm46c246cHVsc2FyOm8tdmJrcnA6Y2x1c3Rlci11IiwiaWF0IjoxNjc4MzQ1NTk0LCJleHAiOjE2Nzg5NTAzOTQsImF6cCI6Ik96OGNZUzlTSDZyb3NBNWNleG1BbTJOVlpsMzFXeGRrIiwic2NvcGUiOiJhZG1pbiBhY2Nlc3MiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJhZG1pbiIsImFjY2VzcyJdfQ.DUW-F4QecOtmtwGUMdeYXGyUHcoq9DCX3u0m_Y9oJJyLXq5wFZCU2MSyvuqXc5myC3BcKxEsDho9q8JuKNexMLzA8I8x71MKw4AV9uQlRXIuYV2jGoVolIZ-2B6HhrxVquOeRfWpw1VGFYDOR1_qMR57W_yqCnXqXarS2O7tALEK3Q_9mCFSvJX0fu8TnGgdvJhxOR4Rsirn14WFVVt1AQg85Wre-YP_AKcRZocxshx7AwhfWLjMu6EmoLGKh1KlB1W4sqXjzuWywuC7zjCPPZquL40Kt6poKLhgRXmgRfk8FlhlZls-fkh6BQvJC5m71uuGbKgHgGGHyXHy1zbRrw'
        cliente = pulsar.Client(
            'pulsar+ssl://cluster-u-479cbdfd-93b9-4b83-8f6f-e694b327fe7c.gcp-shared-gcp-usce1-martin.streamnative.g.snio.cloud:6651', authentication=pulsar.AuthenticationToken(token))
        async with cliente:
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