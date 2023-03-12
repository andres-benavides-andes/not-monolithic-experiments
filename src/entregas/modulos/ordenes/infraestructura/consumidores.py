import pulsar
import _pulsar
from pulsar.schema import *
import uuid
import time
import logging
import traceback

from entregas.modulos.ordenes.infraestructura.schema.v1.eventos import EventoOrdenAlistada
from entregas.modulos.ordenes.aplicacion.comandos.entregar_orden import EntregarOrden, EntregarOrdenItems
from entregas.seedwork.infraestructura import utils
from entregas.seedwork.aplicacion.comandos import ejecutar_commando

import random
import datetime

OPCIONES = {
    "persona_recibe": ["Juan", "Raul", "Maria", "Natalia"],
    "mecanismo_entrega": ["Porteria", "Directo", "Puerta", "Correo"],
}


def simularEntrega():
    return {
        "persona_recibe": random.choice(OPCIONES["persona_recibe"]),
        "mecanismo_entrega": random.choice(OPCIONES["mecanismo_entrega"]),
        "fecha_entrega": datetime.datetime.utcnow().isoformat()
    }


def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'{utils.broker_connection_string()}', authentication=utils.broker_auth())
        consumidor = cliente.subscribe('eventos-centrodistribucion', consumer_type=_pulsar.ConsumerType.Shared,
                                       subscription_name='entregas-sub-eventos', schema=AvroSchema(EventoOrdenAlistada))

        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')

            orden_dto = mensaje.value().data
            print("===Simulacion Items Entregados===")

            orden_items = []
            for item in orden_dto.items:
                op_entrega = simularEntrega()
                orden_items.append(
                    EntregarOrdenItems(
                        guid=item.guid,
                        fecha_entrega=op_entrega["fecha_entrega"],
                        direccion_entrega=item.direccion_entrega,
                        persona_recibe=op_entrega["persona_recibe"],
                        mecanismo_entrega=op_entrega["mecanismo_entrega"]
                    )
                )

            comando = EntregarOrden(
                fecha_creacion=orden_dto.fecha_creacion,
                guid=orden_dto.guid,
                items=orden_items
            )

            ejecutar_commando(comando)

            consumidor.acknowledge(mensaje)

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()
