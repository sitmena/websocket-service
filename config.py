import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    public_key: str

    class Config:
        env_file = ".env"

settings = Settings()
