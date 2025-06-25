from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./taskmaster.db"
    PORT: int = 8000  # default value

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
