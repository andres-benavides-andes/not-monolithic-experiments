from __future__ import annotations
from dataclasses import dataclass
from saga.seedwork.dominio.entidades import Entidad

@dataclass
class PasoSaga(Entidad):
    guid: str = None
    index: str = None
    comando: str = None
    evento: str = None
    error: str = None
    compensacion: str = None

    def crear_paso(self, paso: PasoSaga):
        self.guid = paso.guid
        self.index = paso.index
        self.comando = paso.comando
        self.evento = paso.evento
        self.error = paso.error
        self.compensacion = paso.compensacion

@dataclass
class TransactionSaga(Entidad):
    guid: str = None
    step: PasoSaga = None
    estado: str = None
    fecha_transaccion: str = None

    def crear_transaccion(self, transaccion: TransactionSaga):
        self.guid = transaccion.guid
        self.step = transaccion.step
        self.estado = transaccion.estado
        self.fecha_transaccion = transaccion.fecha_transaccion