from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from app import routes
from app.db import db


app = FastAPI(docs_url=None, redoc_url=None)

openapi_url = "/docs"


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(
    app.swagger_ui_oauth2_redirect_url or "/docs/oauth2-redirect",
    include_in_schema=False,
)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    await db.signin({"username": "root", "password": "root"})
    await db.use("main", "test")
    logger.info("Connected to database.")
    yield
    await db.close()


app = FastAPI(lifespan=lifespan)

app.include_router(routes.account, prefix="/account")
app.mount("/", StaticFiles(directory="dist", html=True), name="dist")
