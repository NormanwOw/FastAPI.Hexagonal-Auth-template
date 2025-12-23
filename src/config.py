from uuid import UUID

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='deploy/.env', env_file_encoding='utf-8')

    DEBUG: bool
    IS_OPEN_CLOSE_REG_ENABLED: bool

    DB_HOST: str
    DB_PORT: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str

    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    INVITE_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str


settings = Settings()


DATABASE_URL = (
    f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@'
    f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.POSTGRES_DB}?async_fallback=True'
)
ID = UUID
PREFIX_URL = '/api/v1'
