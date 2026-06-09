from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:int
    DB_NAME:str
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.1-8b-instant"

    class Config:
        env_file='.env'

settings = Settings()
