from typing import List

from fastapi import APIRouter
from pydantic import BaseModel


class IXXtem(BaseModel):
    name: str
    description: str


class ApiV1Router(APIRouter):
    def __init__(self):
        super().__init__(prefix="/api/v1", include_in_schema=True)
        self.add_api_route("", self.get_items, methods=["GET"])

    async def get_items(self) -> List[IXXtem]:
        return [
            {"name": "Item 1", "description": "This is item 1"},
            {"name": "Item 2", "description": "This is item 2"},
        ]
