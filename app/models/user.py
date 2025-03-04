import bcrypt
from sqlalchemy import TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())

    posts = relationship("Post", backref="author", lazy="dynamic")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), self.password_hash.encode("utf-8")
        )

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
