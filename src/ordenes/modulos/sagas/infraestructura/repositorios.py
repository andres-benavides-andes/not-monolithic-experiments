from ordenes.modulos.ordenes.dominio.entidades import Orden, OrdenItems

from .dto import SagaSteps as SagaStepsDTO

class RepositorioPasosSagaSQLAlchemy(RepositorioPasosSaga):
    def obtener_por_id(self, id: UUID) -> Orden:
    orden_dto = db.session.query(OrdenDTO).filter_by(guid=str(id)).one()
    # TODO
    raise NotImplementedError