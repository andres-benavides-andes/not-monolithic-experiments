import datetime
import pulsar
import _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import uuid

from ordenes.modulos.ordenes.infraestructura.schema.v1.comandos import ComandoCrearOrden
from ordenes.modulos.ordenes.aplicacion.comandos.crear_orden import CrearOrden, CrearOrdenItems
from ordenes.seedwork.infraestructura import utils
from ordenes.seedwork.aplicacion.comandos import ejecutar_commando


def simular_error():
    print("===============================================")
    print("SERVICIO DE ORDENES FALLO, NO SE CREA ORDEN")
    print("===============================================")


def suscribirse_a_comandos():
    cliente = None
    try:
        cliente = pulsar.Client(
            f'{utils.broker_connection_string()}', authentication=utils.broker_auth())
        consumidor = cliente.subscribe('comandos-orden', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='ordenes-sub-comandos', schema=AvroSchema(ComandoCrearOrden))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')

            orden_dto = mensaje.value().data

            sim_error = mensaje.value().sim_error
            if (sim_error == "ordenes"):
                simular_error()
                consumidor.acknowledge(mensaje)
                continue

            print("===Se realizan las validaciones de pedido y se asigna un id===")
            comando = CrearOrden(
                fecha_creacion=int(datetime.datetime.utcnow().timestamp()),
                guid=str(uuid.uuid4()),
                # Llega una orden y la convierto a mi centro de distribuccion
                items=[
                    CrearOrdenItems(
                        guid=str(uuid.uuid4()),
                        direccion_recogida=item.direccion_recogida,
                        direccion_entrega=item.direccion_entrega,
                        tamanio=item.tamanio,
                        telefono=item.telefono
                    ) for item in orden_dto.items
                ]
            )

            utils.set_sim_error(
                comando.guid, sim_error
            )

            ejecutar_commando(comando)

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
