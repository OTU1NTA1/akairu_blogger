from uvicorn import run

from app import EntryServer
from config import Config

# create an instance of the app
app_instance = EntryServer(Config).get_app()

if __name__ == "__main__":
    run("run:app_instance", host=Config.BIND_HOST, port=Config.BIND_PORT, reload=True)
