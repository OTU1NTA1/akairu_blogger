from typing import List

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


class IXtem(BaseModel):
    name: str
    description: str


class ManagerRouter(APIRouter):
    def __init__(self, templates: Jinja2Templates):
        super().__init__(prefix="/manager", include_in_schema=False)
        self.templates = templates
        self.add_api_route("", self.manager, methods=["GET"])

    async def manager(self) -> List[IXtem]:
        return [
            {"name": "Item 1", "description": "This is item 1"},
            {"name": "Item 2", "description": "This is item 2"},
        ]
