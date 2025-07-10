from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    PUSH_NOTIFICATION_PUBLIC_KEY: str
    PUSH_NOTIFICATION_PRIVATE_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
