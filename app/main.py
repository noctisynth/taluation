from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from pydantic import BaseModel

from app import routes
from app.db import db
from app.utils.auth import AuthMiddleware


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
        if db.close:
            await db.close()


app = FastAPI(
    title="Taluation",
    description="Teaching Evaluation System",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    AuthMiddleware,
    exclude_paths=[
        "/account/login",
        "/account/register",
        "/docs",
        "/openapi.json",
        "/redoc",
    ],
)

app.include_router(routes.account, prefix="/account")
app.include_router(routes.cls, prefix="/class")
app.include_router(routes.evaluation, prefix="/evaluation")


@app.get("/announce")
async def getAnnounce():
    return await db.query("RETURN $announce")


class Announce(BaseModel):
    announce: str


@app.put("/announce")
async def putAnnounce(data: Announce):
    return await db.let("announce", data.announce)


app.mount("/", StaticFiles(directory="dist", html=True), name="dist")
