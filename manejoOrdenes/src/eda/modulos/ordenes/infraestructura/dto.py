from eda.config.db import db

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

class Orden(db.Model):
    __tablename__ = "orden"
    id = db.Column(db.String(40), primary_key=True)
    direccion_destino = db.Column(db.String(100))
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    items= db.relationship('Item', cascade = 'all, delete, delete-orphan')

class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.String(40), primary_key=True)
    nombre = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    orden = db.Column(db.String(40),db.ForeignKey('orden.id'))