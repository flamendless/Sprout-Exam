from fastapi import FastAPI

from src.const import API_VERSION
from src.db import setup_db
from src.logger import configure_logger
from src.middleware import setup_exception_handlers, setup_middlewares
from src.routers.v1 import (
    api,
    auth,
    benefit,
    employee,
)

app = FastAPI(title="Sprout Exam API")

app.include_router(api.router, prefix=API_VERSION)
app.include_router(auth.router, prefix=API_VERSION)
app.include_router(employee.router, prefix=API_VERSION)
app.include_router(benefit.router, prefix=API_VERSION)

setup_middlewares(app)
setup_exception_handlers(app)


@app.on_event("startup")
async def on_event_startup():
    configure_logger()
    setup_db()
