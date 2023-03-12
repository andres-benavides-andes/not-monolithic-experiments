from pulsar.schema import String, Long, Array, Record
from entregas.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from entregas.seedwork.infraestructura.utils import time_millis
import uuid


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
    # NOTE La librería Record de Pulsar no es capaz de reconocer campos heredados,
    # por lo que los mensajes al ser codificados pierden sus valores
    # Dupliqué el los cambios que ya se encuentran en la clase Mensaje
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

###########################
### EVENTO COMPENSACION ###
###########################
class EventoOrdenAlistadaCompensacionPayload(Record):
    guid = String()
    fecha_compensacion = Long(default=time_millis())

class EventoOrdenAlistadaCompensacion(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = EventoOrdenAlistadaCompensacionPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

