from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from pydantic import PostgresDsn, RedisDsn, validator
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = 'LLM Backend Api'
    VERSION: str = None
    APP_NAME: str
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str

    ENVIRONMENT: Optional[str]
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    DB_HOST: Optional[str] = None
    DB_PORT: int = 6432

    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_PORT: int
    REDIS_DB_CELERY: str = None
    REDIS_DB_CACHE: str = None

    CELERY_URI: Optional[RedisDsn] = None

    S3_ROOT_USER: Optional[str] = None
    S3_ROOT_PASSWORD: Optional[str] = None
    S3_HOST: Optional[str] = None

    S3_KNOWLEDGE_BASE_BUCKET: str = 'knowledge-base-bucket'

    SENTRY_DSN: Optional[str] = None

    @validator('SQLALCHEMY_DATABASE_URI', pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme='postgresql',
            username=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('DB_HOST'),
            port=values.get('DB_PORT'),
            path=values.get('POSTGRES_DB'),
        )

    @validator('CELERY_URI', pre=True)
    def assemble_celery_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme='redis',
            host=values.get('REDIS_HOST'),
            port=values.get('REDIS_PORT'),
            password=values.get('REDIS_PASSWORD'),
            path=f"{values.get('REDIS_DB_CELERY') or ''}",
        )

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
