from pydantic_settings import BaseSettings  # ✅ IMPORTANT

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    EMAIL_SENDER: str

    class Config:
        env_file = ".env"

settings = Settings()
