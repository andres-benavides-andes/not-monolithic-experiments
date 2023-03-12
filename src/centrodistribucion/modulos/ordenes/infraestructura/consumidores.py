import pulsar
import _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from centrodistribucion.modulos.ordenes.infraestructura.schema.v1.eventos import EventoOrdenCreada
from centrodistribucion.modulos.ordenes.aplicacion.comandos.alistar_orden import AlistarOrden, AlistarOrdenItems
from centrodistribucion.seedwork.infraestructura import utils
from centrodistribucion.seedwork.aplicacion.comandos import ejecutar_commando

CENTRO_DISTRIBUCCION_ADDR = "Av Centro distribucion 123"
def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'{utils.broker_connection_string()}', authentication=utils.broker_auth())
        consumidor = cliente.subscribe('eventos-orden', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='centrodistribucion-sub-eventos', schema=AvroSchema(EventoOrdenCreada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')
            
            orden_dto = mensaje.value().data
            print("===Item recogido y listo en bodega===")
            comando = AlistarOrden (
                fecha_creacion=orden_dto.fecha_creacion,
                guid=orden_dto.guid,
                # Llega una orden y la convierto a mi centro de distribuccion
                items=[
                    AlistarOrdenItems(
                        guid=item.guid,
                        direccion_centro_distribucion="Av Centro distribucion 123",
                        direccion_entrega=item.direccion_entrega,
                        tamanio=item.tamanio,
                        telefono=item.telefono
                    ) for item in orden_dto.items
                ]
            )
            
            ejecutar_commando(comando)

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()