"""Objetos valor del dominio de ordenes

En este archivo usted encontrará los objetos valor del dominio de ordenes

"""

from __future__ import annotations

from dataclasses import dataclass, field
from eda.seedwork.dominio.objetos_valor import ObjetoValor
from datetime import datetime


@dataclass(frozen=True)
class NombreCentroDistribucion():
    nombre: str

@dataclass(frozen=True)
class DireccionRecogida():
	pais: str = field(default_factory=str)
	ciudad: str = field(default_factory=str)
	direccion: str = field(default_factory=str)
	codigo_postal: str = field(default_factory=str)
	telefono_responsable: str = field(default_factory=str)
	nombre_responsable: str = field(default_factory=str)

@dataclass(frozen=True)
class DireccionEntrega():
	pais: str = field(default_factory=str)
	ciudad: str = field(default_factory=str)
	direccion: str = field(default_factory=str)
	codigo_postal: str = field(default_factory=str)
	telefono_responsable: str = field(default_factory=str)
	nombre_responsable: str = field(default_factory=str)


@dataclass(frozen=True)
class Item(ObjetoValor):
	nombre: str 
	cantidad: int
	pais_recogida:str 
	ciudad_recogida:str 
	direccion_recogida:str 
	codigo_postal_recogida:str 
	telefono_responsable_recogida:str 
	nombre_responsable_recogida:str 
	pais_entrega:str 
	ciudad_entrega:str 
	direccion_entrega:str 
	codigo_postal_entrega:str 
	telefono_responsable_entrega:str 
	nombre_responsable_entrega:str

	def nombre(self) -> str:
		return self.nombre

	def cantidad(self) -> str:
		return self.cantidad
   

   
