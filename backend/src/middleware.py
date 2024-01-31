import logging
from sqlite3 import IntegrityError

from asgi_correlation_id import CorrelationIdMiddleware, correlation_id
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.settings import settings

logger = logging.getLogger(__name__)


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(CorrelationIdMiddleware)


def setup_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(IntegrityError)(exc_integrity_error)


async def exc_integrity_error(
    _request: Request,
    exc: IntegrityError
) -> JSONResponse:
    logger.error(f"IntegrityError: {exc}")
    return JSONResponse(
        content={"message": "Duplicate resource"},
        headers={"X-Error": correlation_id.get()},
        status_code=status.HTTP_409_CONFLICT,
    )
