from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager

from app.presentation.api.v1.router import api_router
from app.infrastructure.database.postgresql.db import database
from app.domain.user.exceptions import DomainError
from sqlalchemy.exc import IntegrityError

@asynccontextmanager
async def lifespan(app_: FastAPI):
    await database.init_database()
    yield
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
    uvicorn.run("main:app", reload=True)