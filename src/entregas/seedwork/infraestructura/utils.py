import time
import os
import datetime
import pulsar

epoch = datetime.datetime.utcfromtimestamp(0)

def time_millis():
    return int(time.time() * 1000)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

def broker_host():
    return os.getenv('BROKER_HOST', default="localhost")

def broker_connection_string():
    return os.getenv('BROKER_CONNECTION_STRING', default="pulsar://localhost:6650")

def broker_auth():
    jwt_token = os.getenv('BROKER_JWT_AUTH', default=None)
    if jwt_token:
        return pulsar.AuthenticationToken(jwt_token)
    return None