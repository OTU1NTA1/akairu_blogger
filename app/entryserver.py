from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.models.db import init_db
from app.routes import ApiV1Router, HomeRouter, ManagerRouter


class EntryServer:
    def __init__(self, config):
        self.config = config
        self.app = FastAPI(
            title="Public API GATEWAY",
            docs_url="/api/docs",
            redoc_url=None,
            openapi_url="/api/openapi.json",
        )

        self._init_routers()
        self.app.add_event_handler("startup", self._init_db)

    def _init_routers(self):
        self.app.add_middleware(SessionMiddleware, secret_key=self.config.SESSION_SECRET_KEY)
        # mount static files
        self.app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
        self.app.mount("/assets", StaticFiles(directory="public/assets"), name="assets")
        # mount templates
        self.templates = Jinja2Templates(directory="public")
        # mount routers
        self.app.include_router(HomeRouter(self.templates))
        self.app.include_router(ApiV1Router())
        self.app.include_router(ManagerRouter(self.templates))

    async def _init_db(self):
        await init_db()

    def get_app(self):
        return self.app
