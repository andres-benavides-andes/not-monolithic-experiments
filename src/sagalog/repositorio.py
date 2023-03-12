from sagalog.config.db import Session, TransactionSaga, PasoSaga
from sqlalchemy import desc

import uuid
import datetime
import json

class TransactionSagaRepository:

    def guardarTrasanccion(datos, evento, estado):
        with Session() as session:
            if estado == 'EXITOSO':
                paso_saga = PasoSagaRepository.obtenerPasoPorEvento(evento)
            else:
                paso_saga = PasoSagaRepository.obtenerPasoPorError(evento)

            row = TransactionSaga(
                guid=str(uuid.uuid4()), 
                transaction_id=datos.data.guid,
                step=paso_saga.guid,
                estado=estado,
                fecha_transaccion=datetime.datetime.now()
            )
            session.add(row)
            session.commit()

    def obtenerTodasLasTransacciones():
        with Session() as session:
            result = session.query(TransactionSaga, PasoSaga).\
                join(PasoSaga).\
                order_by(desc(TransactionSaga.fecha_transaccion)).\
                all()
            transactions = []
            for transaction, paso in result:
                transaction_dict = {
                    'transaction_id': transaction.transaction_id,
                    'step': paso.evento,
                    'estado': transaction.estado,
                    'fecha_transaccion': str(transaction.fecha_transaccion)
                }
                transactions.append(transaction_dict)
            return transactions

    def obtenerTransaccionesPorId(transaction_id: str):
        with Session() as session:
            result = session.query(TransactionSaga, PasoSaga).\
                join(PasoSaga).\
                filter(TransactionSaga.transaction_id == transaction_id).\
                order_by(desc(TransactionSaga.fecha_transaccion)).\
                all()
            transactions = []
            for transaction, paso in result:
                transaction_dict = {
                    'transaction_id': transaction.transaction_id,
                    'step': paso.evento,
                    'estado': transaction.estado,
                    'fecha_transaccion': str(transaction.fecha_transaccion)
                }
                transactions.append(transaction_dict)
            return transactions

class PasoSagaRepository:

    def obtenerPasoPorEvento(evento):
        with Session() as session:
            return session.query(PasoSaga).filter_by(evento=evento).first()

    def obtenerPasoPorError(eventoError):
        with Session() as session:
            return session.query(PasoSaga).filter_by(error=eventoError).first()
