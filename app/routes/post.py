from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.requests import Request


class PostModel(BaseModel):
    id: int
    title: str
    content: str
    created_at: str
    updated_at: str


def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/manager/login")
    return user


class PostRouter(APIRouter):
    def __init__(self, templates: Jinja2Templates):
        super().__init__(prefix="/manager/posts", include_in_schema=False)
        self.templates = templates
        self.add_api_route("", self.post_page, methods=["GET"])
        self.add_api_route("/add", self.post_add_page, methods=["GET"])
        self.add_api_route("/edit", self.post_edit_page, methods=["GET"])

    async def posts_page(self, current_user: dict = Depends(get_current_user)):
        pass

    async def post_add_page(self, current_user: dict = Depends(get_current_user)):
        pass

    async def post_edit_page(self, current_user: dict = Depends(get_current_user)):
        pass
