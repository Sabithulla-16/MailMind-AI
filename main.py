import sys

sys.stdout.reconfigure(
    encoding="utf-8"
)

sys.stderr.reconfigure(
    encoding="utf-8"
)

from contextlib import asynccontextmanager

from fastapi import FastAPI

from starlette.middleware.sessions import SessionMiddleware

from api.health import router as health_router
from api.auth import router as auth_router
from api.privacy import router as privacy_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

@asynccontextmanager
async def lifespan(app: FastAPI):

    yield


app = FastAPI(
    title="MailMind AI",
    lifespan=lifespan
)

app.mount(
    "/static",
    StaticFiles(
        directory="static"
    ),
    name="static"
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(privacy_router)

app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key"
)


@app.get("/")
def root():

    return {
        "message": "MailMind AI Running"
    }

@app.get("/favicon.ico")
def favicon():

    return RedirectResponse(
        url="/static/favicon.ico"
    )