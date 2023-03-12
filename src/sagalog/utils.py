import time
import os
import datetime
import requests
import json
import pulsar

epoch = datetime.datetime.utcfromtimestamp(0)
PULSAR_ENV: str = 'BROKER_HOST'
TOKEN: str = 'BROKER_JWT_AUTH'

def time_millis():
    return int(time.time() * 1000)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

def millis_a_datetime(millis):
    return datetime.datetime.fromtimestamp(millis/1000.0)

def broker_host():
    return os.getenv(PULSAR_ENV, default="cluster-u-479cbdfd-93b9-4b83-8f6f-e694b327fe7c.gcp-shared-gcp-usce1-martin.streamnative.g.snio.cloud")

def get_token():
    return os.getenv(TOKEN, default=None)

def get_pulsar_auth():
    token = get_token()
    return pulsar.AuthenticationToken(token) if token is not None else None

