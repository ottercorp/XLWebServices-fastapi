import time
import re

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.routing import Route
from starlette.middleware.sessions import SessionMiddleware

from .utils.common import get_settings
from .resources import router as resources_router
from .front import router as front_router
from .utils.front import FlashMessageMiddleware


# from .models import database


def get_app() -> FastAPI:
    app = FastAPI()

    origins = [
        "http://localhost",
        "http://localhost:8080",
    ]

    app.add_middleware(FlashMessageMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        GZipMiddleware,
        minimum_size=500
    )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    app.add_middleware(
        SessionMiddleware,
        secret_key='testkey'
    )

    app.include_router(resources_router)
    app.include_router(front_router)

    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/", StaticFiles(directory="artifact"), name="artifact")
    app.mount("/faq", StaticFiles(directory="artifact/faq"), name="faq")

    for route in app.router.routes:
        if isinstance(route, Route):
            # print(route.path_regex.pattern)
            route.path_regex = re.compile(route.path_regex.pattern, re.IGNORECASE)

    # No database needs, for now
    # @app.on_event("startup")
    # async def startup():
    #     await database.connect()

    # @app.on_event("shutdown")
    # async def shutdown():
    #     await database.disconnect()

    return app
