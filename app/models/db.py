from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import Config

engine = create_async_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    db = SessionLocal()
    return db


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
