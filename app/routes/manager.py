from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.models import User
from app.models.db import get_db


class LoginPost(BaseModel):
    username: str
    password: str


class RegisterPost(BaseModel):
    username: str
    password: str
    password_confirmation: str


def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/manager/login")
    return user


class ManagerRouter(APIRouter):
    def __init__(self, templates: Jinja2Templates):
        super().__init__(prefix="/manager", include_in_schema=False)
        self.templates = templates
        self.add_api_route("", self.manager_page, methods=["GET"])
        self.add_api_route("/login", self.login_page, methods=["GET"])

    async def manager_page(self, current_user: dict = Depends(get_current_user)):
        if isinstance(current_user, RedirectResponse):
            return current_user
        return [
            {"name": "Item 1", "description": "This is item 1"},
            {"name": "Item 2", "description": "This is item 2"},
        ]

    async def login_page(self, request: Request):
        return self.templates.TemplateResponse(
            "manager_login.html", {"request": request}
        )

    async def login(
        request: Request, login_data: LoginPost, db: Session = Depends(get_db)
    ):
        user = db.query(User).filter(User.username == login_data.username).first()

        if not user or not user.verify_password(login_data.password):
            raise JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Invalid credentials", "status": 401},
            )
        if not user.verify_password(login_data.password):
            raise JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Invalid password ur username", "status": 401},
            )

        request.session["user"] = {"username": user.username}
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Login successful", "status": 200},
        )

    async def register(
        request: Request, register_data: RegisterPost, db: Session = Depends(get_db)
    ):
        if register_data.password != register_data.password_confirmation:
            raise JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Passwords do not match", "status": 401},
            )
        existing_user = (
            db.query(User).filter(User.username == register_data.username).first()
        )
        if existing_user:
            raise JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "Username already exists", "status": 401},
            )

        user = User(
            username=register_data.username,
            email=register_data.email,
            password_hash=User.hash_password(register_data.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        request.session["user"] = {"username": user.username}
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Register successful", "status": 200},
        )
