from typing import List

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str


class HomeRouter(APIRouter):
    def __init__(self, templates: Jinja2Templates):
        super().__init__(include_in_schema=False)
        self.templates = templates
        self.add_api_route("/", self.get_items, methods=["GET"])

    async def get_items(self, request: Request) -> List[Item]:
        return self.templates.TemplateResponse(
            request=request, name="index.html", context={"id": id}
        )
