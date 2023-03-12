from fastapi import FastAPI, Request
import asyncio
import time
import traceback
import uvicorn
import uuid
import datetime

from pydantic import BaseSettings
from typing import Any

from .consumidores import suscribirse_a_topico

from . import utils

class Config(BaseSettings):
    APP_VERSION: str = "1"

settings = Config()
app_configs: dict[str, Any] = {"title": "SAGA"}

app = FastAPI(**app_configs)
tasks = list()
eventos = list()

@app.on_event("startup")
async def app_startup():
    global tasks
    global eventos
    task1 = asyncio.ensure_future(suscribirse_a_topico("eventos-orden", "eoa-bff", "public/default/eventos-orden", eventos=eventos))
    tasks.append(task1)

@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()