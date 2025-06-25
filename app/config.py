from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./taskmaster.db"
    
    class Config:
        env_file = ".env"

settings = Settings()