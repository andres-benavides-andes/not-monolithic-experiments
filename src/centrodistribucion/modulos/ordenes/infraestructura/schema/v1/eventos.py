from pulsar.schema import String, Long, Array, Record
from centrodistribucion.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from centrodistribucion.seedwork.infraestructura.utils import time_millis
import uuid

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
    data = EventoOrdenCreadaPayload()
    sim_error = String()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

###########################
### EVENTO COMPENSACION ###
###########################
class EventoOrdenCreadaCompensacionPayload(Record):
    guid = String()
    fecha_compensacion = Long(default=time_millis())

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
