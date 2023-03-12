


class PasoSaga():
    guid: str = None
    index: str = None
    comando: str = None
    evento: str = None
    error: str = None
    compensacion: str = None


    def crear_orden(self, orden: Orden):
        self.guid = orden.guid
        self.fecha_creacion = orden.fecha_creacion
        self.items = orden.items

        self.agregar_evento(OrdenCreada(
            fecha_creacion=self.fecha_creacion,
            guid=self.guid,
            items=self.items
        ))