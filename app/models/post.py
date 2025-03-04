from sqlalchemy import TIMESTAMP, Column, Integer, String, Text
from sqlalchemy.sql import func

from .db import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title})>"
