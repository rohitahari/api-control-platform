from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ENV: str = "dev"

    @property
    def is_production(self) -> bool:
        return self.ENV.lower() == "prod"

    class Config:
        env_file = ".env"


settings = Settings()