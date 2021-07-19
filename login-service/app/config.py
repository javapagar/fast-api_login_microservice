from pydantic import BaseSettings

class Settings(BaseSettings):
    #SQLALCHEMY_DATABASE_URL : str = "sqlite:///./sql_app.db"
    db_url : str
    user : str = ""
    password : str = ""

    class Config:#desde fichero .env
        env_file=".env"