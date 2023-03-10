import typing
import strawberry
import uuid
import requests
import os

from datetime import datetime


AEROALPES_HOST = os.getenv("API_ADDRESS", default="localhost")
FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

def obtener_ordenes(root) -> typing.List["Orden"]:
    ordenes_json = requests.get(f'http://{AEROALPES_HOST}:5000/orden').json()
    ordenes = []

    for orden in ordenes_json:
        ordenes.append(
            Orden(
                fecha_creacion=datetime.strptime(orden.get('fecha_creacion'), FORMATO_FECHA), 
                fecha_actualizacion=datetime.strptime(orden.get('fecha_actualizacion'), FORMATO_FECHA), 
                id=orden.get('id'), 
                id_usuario=orden.get('id_usuario', '')
            )
        )

    return ordenes

@strawberry.type
class Orden:
    id: str
    id_usuario: str
    fecha_creacion: datetime
    fecha_actualizacion: datetime

@strawberry.type
class OrdenRespuesta:
    mensaje: str
    codigo: int






