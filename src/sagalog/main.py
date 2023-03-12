from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import asyncio
import time
import traceback
import uvicorn
import uuid
import datetime


from pydantic import BaseSettings
from typing import Any

from .consumidores import suscribirse_a_topico

from .repositorio import TransactionSagaRepository

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
    task1 = asyncio.ensure_future(
        suscribirse_a_topico(
            "eventos-orden",
            "saga-log",
            "OrdenCreada",
            "EXITOSO",
            "public/default/eventos-orden",
            eventos=eventos
        )
    )
    tasks.append(task1)
    task2 = asyncio.ensure_future(
        suscribirse_a_topico(
            "eventos-centrosdistribucion",
            "saga-log",
            "OrdenAlistada",
            "EXITOSO",
            "public/default/eventos-centrosdistribucion",
            eventos=eventos
        )
    )
    tasks.append(task2)
    # task3 = asyncio.ensure_future(
    #     suscribirse_a_topico(
    #         "eventos-entregas",
    #         "saga-log",
    #         "OrdenEntregada",
    #         "EXITOSO",
    #         "public/default/eventos-entregas",
    #         eventos=eventos
    #     )
    # )
    # tasks.append(task3)

@app.on_event("shutdown")
def shutdown_event():
    global tasks
    for task in tasks:
        task.cancel()

@app.get('/transactions')
def get_transactions(request: Request):
    transactions = TransactionSagaRepository.obtenerTodasLasTransacciones()
    return JSONResponse(content={"transactions": transactions})