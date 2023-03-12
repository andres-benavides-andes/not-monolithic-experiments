from abc import ABC
from saga.seedwork.dominio.repositorios import Repositorio

class RepositorioPasosSaga(Repositorio, ABC):
    ...

class RepositorioTransaccionesSaga(Repositorio, ABC):
    ...