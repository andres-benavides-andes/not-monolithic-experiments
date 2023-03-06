from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask import Flask
import os

db = None
session = None

DB_USERNAME = os.getenv('DB_USERNAME', default="root")
DB_PASSWORD = os.getenv('DB_PASSWORD', default="adminadmin")
DB_HOSTNAME = os.getenv('DB_HOSTNAME', default="localhost")

class DatabaseConfigException(Exception):
    def __init__(self, message='Configuration file is Null or malformed'):
        self.message = message
        super().__init__(self.message)


def database_connection(config, basedir=os.path.abspath(os.path.dirname(__file__))) -> str:
    if not isinstance(config,dict):
        raise DatabaseConfigException
    
    if config.get('TESTING', False) == True:
        return f'sqlite:///{os.path.join(basedir, "database.db")}'
    else:
        return f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/centrodistribucion'


def init_db(app: Flask):
    global db 
    db = SQLAlchemy(app)
    with app.app_context():
        Session = sessionmaker(bind=db.engine)
        global session
        session = Session()