import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "akairu_blogger")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "123456")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BIND_HOST = os.getenv("BIND_HOST", "0.0.0.0")
    BIND_PORT = int(os.getenv("BIND_PORT", 8000))
