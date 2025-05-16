from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL")

    class Config:
        env_file = ".env"
        extra = "ignore"
        from_attributes = True

settings = Settings()
print(settings.SQLALCHEMY_DATABASE_URI)  # This will print the DATABASE_URL from .env

