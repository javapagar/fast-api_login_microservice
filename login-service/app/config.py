from pydantic import BaseSettings

class Settings(BaseSettings):
    db_url : str
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    POSTGRES_SERVER : str
    POSTGRES_PORT : str
    POSTGRES_DB : str
    SECRET_KEY : str
    ALGORITHM : str


    class Config:#desde fichero .env
        env_file=".env"
       