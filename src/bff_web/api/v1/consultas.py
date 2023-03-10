
import strawberry
from .esquemas import *

@strawberry.type
class Query:
    reservas: typing.List[Orden] = strawberry.field(resolver=obtener_reservas)