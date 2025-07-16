from pathlib import Path
from pydantic_settings  import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENVIRONMENT: str = "development"
    DATABASE_URL: str

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"

settings = Settings()
