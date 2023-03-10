import time
import os
import datetime
import requests
import json
from fastavro.schema import parse_schema
from pulsar.schema import *

epoch = datetime.datetime.utcfromtimestamp(0)
PULSAR_ENV: str = 'cluster-u-479cbdfd-93b9-4b83-8f6f-e694b327fe7c.gcp-shared-gcp-usce1-martin.streamnative.g.snio.cloud'

def time_millis():
    return int(time.time() * 1000)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

def millis_a_datetime(millis):
    return datetime.datetime.fromtimestamp(millis/1000.0)

def broker_host():
    return os.getenv(PULSAR_ENV, default="localhost")

def get_token():
    return os.getenv(TOKEN, default='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5rRXdSVVU1TUVOQlJrWTJNalEzTVRZek9FVkZRVVUyT0RNME5qUkRRVEU1T1VNMU16STVPUSJ9.eyJodHRwczovL3N0cmVhbW5hdGl2ZS5pby91c2VybmFtZSI6Im5vLW1vbm9saXRvcy1hY2NvdW50QG8tdmJrcnAuYXV0aC5zdHJlYW1uYXRpdmUuY2xvdWQiLCJpc3MiOiJodHRwczovL2F1dGguc3RyZWFtbmF0aXZlLmNsb3VkLyIsInN1YiI6Ik96OGNZUzlTSDZyb3NBNWNleG1BbTJOVlpsMzFXeGRrQGNsaWVudHMiLCJhdWQiOiJ1cm46c246cHVsc2FyOm8tdmJrcnA6Y2x1c3Rlci11IiwiaWF0IjoxNjc4MzQ1NTk0LCJleHAiOjE2Nzg5NTAzOTQsImF6cCI6Ik96OGNZUzlTSDZyb3NBNWNleG1BbTJOVlpsMzFXeGRrIiwic2NvcGUiOiJhZG1pbiBhY2Nlc3MiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJwZXJtaXNzaW9ucyI6WyJhZG1pbiIsImFjY2VzcyJdfQ.DUW-F4QecOtmtwGUMdeYXGyUHcoq9DCX3u0m_Y9oJJyLXq5wFZCU2MSyvuqXc5myC3BcKxEsDho9q8JuKNexMLzA8I8x71MKw4AV9uQlRXIuYV2jGoVolIZ-2B6HhrxVquOeRfWpw1VGFYDOR1_qMR57W_yqCnXqXarS2O7tALEK3Q_9mCFSvJX0fu8TnGgdvJhxOR4Rsirn14WFVVt1AQg85Wre-YP_AKcRZocxshx7AwhfWLjMu6EmoLGKh1KlB1W4sqXjzuWywuC7zjCPPZquL40Kt6poKLhgRXmgRfk8FlhlZls-fkh6BQvJC5m71uuGbKgHgGGHyXHy1zbRrw')

def consultar_schema_registry(topico: str) -> dict:
    json_registry = requests.get(f'http://{broker_host()}:8080/admin/v2/schemas/{topico}/schema').json()
    return json.loads(json_registry.get('data',{}))

def obtener_schema_avro_de_diccionario(json_schema: dict) -> AvroSchema:
    definicion_schema = parse_schema(json_schema)
    return AvroSchema(None, schema_definition=definicion_schema)

