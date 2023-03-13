import uuid
from pulsar.schema import *
import time

def time_millis():
    return int(time.time() * 1000)

from sagalog.eventos.evento_integracion import EventoIntegracion

#### EVENTO ORDEN ENTREGADA ###

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
    sim_error = String()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class EventoOrdenEntregadaItem(Record):
    guid = String()
    direccion_entrega = String()
    fecha_entrega = Long()
    persona_recibe = String()
    mecanismo_entrega = String()

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
