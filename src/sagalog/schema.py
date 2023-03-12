from pydantic import BaseModel
import datetime

class TransactionSchema(BaseModel):
    transaction_id: str
    step: str
    estado: str
    fecha_transaccion: datetime.datetime