from pulsar.schema import *
from dataclasses import dataclass, field
from pulsar.schema import String, Long, Array, Record
from ordenes.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from ordenes.seedwork.infraestructura.utils import time_millis

import uuid

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