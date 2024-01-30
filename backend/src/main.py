from fastapi import FastAPI

from src.db import setup_db
from src.logger import configure_logger
from src.middleware import setup_middlewares
from src.routers.v1 import api, auth


app = FastAPI(title="Sprout Exam API")

app.include_router(api.router)
app.include_router(auth.router)

setup_middlewares(app)


@app.on_event("startup")
async def on_event_startup():
    configure_logger()
    setup_db()
