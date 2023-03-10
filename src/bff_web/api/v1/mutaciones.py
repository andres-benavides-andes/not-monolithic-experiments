import strawberry
import typing
from typing import List

from strawberry.types import Info
from bff_web import utils
from bff_web.despachadores import Despachador, ComandoCrearOrden, ComandoCrearOrdenPayload

from .esquemas import *

@strawberry.input
class ItemInput:
    direccion_recogida: str
    direccion_entrega: str
    tamanio: str
    telefono: str

@strawberry.type
class Mutation:

    @strawberry.mutation
    async def crear_orden(self, id_usuario: str, items: List[ItemInput], info: Info) -> OrdenRespuesta:
        print(f"ID Usuario: {id_usuario}")
        for item in items:
            print(f"Dirección Recogida: {item.direccion_recogida}, Dirección Entrega: {item.direccion_entrega}, Tamaño: {item.tamanio}, Teléfono: {item.telefono}")
        
        payload = dict(
            id_usuario=id_usuario,
            fecha_creacion=utils.time_millis(),
            items=[item.__dict__ for item in items]
        )

        comando = ComandoCrearOrden(
            data= ComandoCrearOrdenPayload (
                items= [item.__dict__ for item in items],
                fecha_creacion=utils.time_millis(),
            )
        )

        # comando = dict(
        #     id = str(uuid.uuid4()),
        #     time=utils.time_millis(),
        #     specversion = "v1",
        #     type = "ComandoOrden",
        #     ingestion=utils.time_millis(),
        #     datacontenttype="AVRO",
        #     service_name = "BFF Web",
        #     data = payload
        # )
        despachador = Despachador()
        info.context["background_tasks"].add_task(despachador.publicar_mensaje, comando, "comandos-orden", "public/default/comandos-orden")
        
        return OrdenRespuesta(mensaje="Procesando Mensaje", codigo=203)