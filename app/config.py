import os
from pydantic_settings import BaseSettings
import logging


class Settings(BaseSettings):
    public_key: str = os.getenv("PUBLIC_KEY")

settings = Settings()
