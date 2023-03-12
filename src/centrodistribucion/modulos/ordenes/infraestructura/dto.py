from centrodistribucion.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

class Paquete(db.Model):
    __tablename__ = "paquetes"
    guid = db.Column(db.String(40), primary_key=True)
    orden_guid = db.Column(db.String(40), db.ForeignKey('orden.guid', ondelete='CASCADE'))
    direccion_centro_distribucion = db.Column(db.String(40), nullable=False)
    direccion_entrega = db.Column(db.String(40), nullable=False)
    tamanio = db.Column(db.String(10), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)

class Orden(db.Model):
    __tablename__ = "orden"
    guid = db.Column(db.String(40), primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    items = db.relationship('Paquete',  backref="orden", passive_deletes=True)

class EventosOrden(db.Model):
    __tablename__ = "eventos_orden"
    id = db.Column(db.String(40), primary_key=True)
    id_entidad = db.Column(db.String(40), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)