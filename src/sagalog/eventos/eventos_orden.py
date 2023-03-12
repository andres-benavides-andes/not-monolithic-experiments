import uuid
from pulsar.schema import *
import time

def time_millis():
    return int(time.time() * 1000)

from sagalog.eventos.evento_integracion import EventoIntegracion 

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

#### EVENTO COMPENSACION ORDEN CREADA ###

class EventoOrdenCreadaCompensacionPayload(Record):
    guid = String()
    fecha_compensacion = Long()

class EventoOrdenCreadaCompensacion(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = EventoOrdenCreadaCompensacionPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)