from sagalog.config.db import Session, PasoSaga
import uuid

def seed_steps_table():
    with Session() as session:
        # Verificamos si la tabla está vacía
        if session.query(PasoSaga).count() == 0:
            # Si está vacía, insertamos los registros
            steps = [
                PasoSaga(guid=str(uuid.uuid4()), index=1, comando='CrearOrden', evento='OrdenCreada', error='CreacionOrdenFallida'),
                PasoSaga(guid=str(uuid.uuid4()), index=1, comando='AlistarOrden', evento='OrdenAlistada', error='CancelarOrden', compensacion='DesalistarOrden'),
                PasoSaga(guid=str(uuid.uuid4()), index=1, comando='EntregarOrden', evento='OrdenEntregada', error='OrdenDesAlistada', compensacion='CancelarEntrega')
            ]
            session.bulk_save_objects(steps)
            session.commit()