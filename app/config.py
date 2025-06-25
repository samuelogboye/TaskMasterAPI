from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str 
    PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
