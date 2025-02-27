from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app import routes
from app.db import db


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        await db.signin({"username": "root", "password": "root"})
        await db.use("main", "test")
        logger.info("Connected to database.")
        yield
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
    finally:
        await db.close()


app = FastAPI(
    title="Taluation",
    description="Teaching Evaluation System",
    lifespan=lifespan,
)

app.include_router(routes.account, prefix="/account")
app.include_router(routes.cls, prefix="/class")

app.mount("/", StaticFiles(directory="dist", html=True), name="dist")
