from abc import ABC
from ordenes.seedwork.dominio.repositorios import Repositorio

class RepositorioPasosSaga(Repositorio, ABC):
    ...

class RepositorioTransaccionesSaga(Repositorio, ABC):
    ...