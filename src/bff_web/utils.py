import time
import os
import datetime
import requests
import json
from fastavro.schema import parse_schema
from pulsar.schema import *
import pulsar

epoch = datetime.datetime.utcfromtimestamp(0)
PULSAR_ENV: str = 'BROKER_HOST'

def time_millis():
    return int(time.time() * 1000)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

def millis_a_datetime(millis):
    return datetime.datetime.fromtimestamp(millis/1000.0)

def broker_host():
    return os.getenv(PULSAR_ENV, default="cluster-u-479cbdfd-93b9-4b83-8f6f-e694b327fe7c.gcp-shared-gcp-usce1-martin.streamnative.g.snio.cloud")

def broker_connection_string():
    return os.getenv('BROKER_CONNECTION_STRING', default="pulsar://localhost:6650")

def broker_auth():
    jwt_token = os.getenv('BROKER_JWT_AUTH', default=None)
    if jwt_token:
        return pulsar.AuthenticationToken(jwt_token)
    return None

def consultar_schema_registry(topico: str) -> dict:
    json_registry = requests.get(f'http://{broker_host()}:8080/admin/v2/schemas/{topico}/schema').json()
    return json.loads(json_registry.get('data',{}))

def obtener_schema_avro_de_diccionario(json_schema: dict) -> AvroSchema:
    definicion_schema = parse_schema(json_schema)
    return AvroSchema(None, schema_definition=definicion_schema)

