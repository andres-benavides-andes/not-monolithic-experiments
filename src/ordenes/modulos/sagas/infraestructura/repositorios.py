import datetime
from ordenes.config.db import db, session
from ordenes.modulos.sagas.dominio.entidades import PasoSaga, TransactionSaga
from ordenes.modulos.sagas.dominio.repositorios import RepositorioPasosSaga, RepositorioTransaccionesSaga

from uuid import UUID
from .dto import PasoSaga as PasoSagaDTO
from .dto import TransactionSaga as TransactionSagaDTO

from typing import List

class RepositorioPasosSagaSQLAlchemy(RepositorioPasosSaga):
    def obtener_por_id(self, id: UUID) -> PasoSaga:
        paso_saga_dto = db.session.query(PasoSagaDTO).filter_by(guid=str(id)).one()
        
        paso_saga = PasoSaga()
        paso_saga.guid = paso_saga_dto.guid
        paso_saga.index = paso_saga_dto.index
        paso_saga.comando = paso_saga_dto.comando
        paso_saga.evento = paso_saga_dto.evento
        paso_saga.error = paso_saga_dto.error
        paso_saga.compensacion = paso_saga_dto.compensacion

        return paso_saga
    
    def obtener_todos(self) -> List[PasoSaga]:
        pasos_saga_dto = db.session.query(PasoSagaDTO).all()
        
        pasos_saga = []
        for paso_saga_dto in pasos_saga_dto:
            paso_saga = PasoSaga()
            paso_saga.guid = paso_saga_dto.guid
            paso_saga.index = paso_saga_dto.index
            paso_saga.comando = paso_saga_dto.comando
            paso_saga.evento = paso_saga_dto.evento
            paso_saga.error = paso_saga_dto.error
            paso_saga.compensacion = paso_saga_dto.compensacion
            pasos_saga.append(paso_saga)

        return pasos_saga
    
    def agregar(self, paso: PasoSaga):
        orden_dto = PasoSagaDTO()
        orden_dto.guid = paso.guid
        orden_dto.index = paso.index
        orden_dto.comando = paso.comando
        orden_dto.evento = paso.evento
        orden_dto.error = paso.error
        orden_dto.compensacion = paso.compensacion
        
        session.add(orden_dto)

    def actualizar(self, paso: PasoSaga):
        # TODO
        raise NotImplementedError
    
    def eliminar(self, paso_id: UUID):
        # TODO
        raise NotImplementedError
    
class RepositorioTransaccionesSagaSQLAlchemy(RepositorioTransaccionesSaga):
    def obtener_por_id(self, id: UUID) -> TransactionSaga:
        transaccion_saga_dto = db.session.query(TransactionSagaDTO).filter_by(guid=str(id)).one()

        transaccion = TransactionSaga()
        transaccion.guid = transaccion_saga_dto.guid
        transaccion.step = transaccion_saga_dto.step
        transaccion.estado = transaccion_saga_dto.estado
        transaccion.fecha_transaccion = transaccion_saga_dto.fecha_transaccion

        return transaccion
    
    def obtener_todos(self) -> List[TransactionSaga]:
        transacciones_saga_dto = db.session.query(TransactionSagaDTO).all()
        
        transacciones_saga = []
        for transaccion_saga_dto in transacciones_saga_dto:
            transaccion_saga = TransactionSaga()
            transaccion_saga.guid = transaccion_saga_dto.guid
            transaccion_saga.step = transaccion_saga_dto.step
            transaccion_saga.estado = transaccion_saga_dto.estado
            transaccion_saga.fecha_transaccion = transaccion_saga_dto.fecha_transaccion
            transacciones_saga.append(transaccion_saga)

        return transacciones_saga
    
    def agregar(self, transaccion: TransactionSaga):
        transaccion_dto = TransactionSagaDTO()
        transaccion_dto.guid = transaccion.guid
        transaccion_dto.step = transaccion.step
        transaccion_dto.estado = transaccion.estado
        transaccion_dto.fecha_transaccion = datetime.datetime.fromtimestamp(transaccion.fecha_creacion)
        
        session.add(transaccion_dto)

    def actualizar(self, transaccion: TransactionSaga):
        transaccion_dto = db.session.query(TransactionSagaDTO).filter_by(guid=str(transaccion.guid)).one()
        transaccion_dto.guid = transaccion.guid
        transaccion_dto.step = transaccion.step
        transaccion_dto.estado = transaccion.estado
        transaccion_dto.fecha_transaccion = datetime.datetime.fromtimestamp(transaccion.fecha_creacion)
        
        transaccion_dto.save()

    def eliminar(self, transaccion_id: UUID):
        transaccion_dto = db.session.query(TransactionSagaDTO).filter_by(guid=str(transaccion_id)).one()
        
        transaccion_dto.delete()

    