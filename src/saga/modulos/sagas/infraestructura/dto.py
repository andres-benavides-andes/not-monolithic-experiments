from saga.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

Base = db.declarative_base()

class PasoSaga(db.Model):
    __tablename__ = "saga_steps"
    guid = db.Column(db.String(40), primary_key=True)
    index = db.Column(db.Numeric(), nullable=False)
    comando = db.Column(db.String(40))
    evento = db.Column(db.String(40))
    error = db.Column(db.String(40))
    compensacion = db.Column(db.String(40))

class TransactionSaga(db.Model):
    __tablename__ = "saga_transactions"
    guid = db.Column(db.String(40), primary_key=True)
    transaction_id = db.Column(db.String(40), nullable=False)
    step = db.Column(db.String(40), db.ForeignKey('saga_steps.guid'))
    estado = db.Column(db.String(30), nullable=False)
    fecha_transaccion = db.Column(db.DateTime, nullable=False)
