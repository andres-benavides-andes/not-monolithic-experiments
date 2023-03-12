from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DB_USERNAME = os.getenv('DB_USERNAME', default="root")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="adminadmin")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")

engine = create_engine(f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/saga_log')
Base = declarative_base()

class PasoSaga(Base):
    __tablename__ = "saga_steps"
    guid = Column(String(40), primary_key=True)
    index = Column(Integer(), nullable=False)
    comando = Column(String(40))
    evento = Column(String(40))
    error = Column(String(40))
    compensacion = Column(String(40))

class TransactionSaga(Base):
    __tablename__ = "saga_transactions"
    guid = Column(String(40), primary_key=True)
    transaction_id = Column(String(40), nullable=False)
    step = Column(String(40), ForeignKey('saga_steps.guid'))
    estado = Column(String(30), nullable=False)
    fecha_transaccion = Column(DateTime, nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def seed_steps_table():
    from sagalog.config.seed import seed_steps_table as seed
    seed()