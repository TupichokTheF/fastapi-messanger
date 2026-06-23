import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, asyncio
from contextlib import asynccontextmanager

from app.core.logging.log_config import Logger
from app.infrastructure.adapters.log_handlers import KafkaHandler
from app.presentation.api.v1.router import api_router
from app.infrastructure.database.postgresql.db import database
from app.infrastructure.database.redis.conn import RedisCon
from app.infrastructure.websockets.con_manager import connection_manager
from app.infrastructure.brockers.kafka.producer import KafkaProducer
from app.domain.user.exceptions import DomainError

from sqlalchemy.exc import IntegrityError
from asyncio.queues import Queue

async def send_logs(queue: Queue, producer: KafkaProducer):
    while True:
        message_log = await queue.get()
        try:
            await producer.send_message("app_logs", message_log)
        except Exception:
            pass
        finally:
            queue.task_done()

def setup_kafka_logger(producer: KafkaProducer):
    queue = Queue()
    loop = asyncio.get_running_loop()

    kafka_handler = KafkaHandler(queue, loop)
    kafka_handler.setLevel(level=logging.INFO)
    logger = Logger()
    logger.add_handler(kafka_handler)

    asyncio.create_task(send_logs(queue, producer))

    return queue

@asynccontextmanager
async def lifespan(app_: FastAPI):
    asyncio.create_task(connection_manager.init_listening())

    await database.init_database()

    producer = KafkaProducer()
    await producer.start()
    app.state.kafka_producer = producer
    queue = setup_kafka_logger(producer)

    yield
    await queue.join()
    await producer.stop()
    await RedisCon.dispose_redis()
    await database.dispose_database()

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)},
    )

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "Resource already exists or integrity violation."},
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.presentation.api.main:app",
        host="localhost",
        port=8000,
        reload=True,
    )