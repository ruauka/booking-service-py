from typing import Literal, Optional

from pydantic import BaseSettings


class Cfg(BaseSettings):
    """
    Конфигурация сервиса.
    """
    # мод работы сервиса
    MODE: Optional[Literal["DEV", "TEST", "PROD"]]
    # уровень логирования
    LOG_LEVEL: Optional[Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]]

    # конфиг БД
    DB_HOST: Optional[str]
    DB_PORT: Optional[int]
    POSTGRES_USER: Optional[str]
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_DB: Optional[str]

    @property
    def db_url(self) -> str:
        """
        Путь подключения к PostgresSQL
        :return: dsn
        """
        return f"postgresql+asyncpg://" \
               f"{self.POSTGRES_USER}:" \
               f"{self.POSTGRES_PASSWORD}@" \
               f"{self.DB_HOST}:" \
               f"{self.DB_PORT}/" \
               f"{self.POSTGRES_DB}"

    @property
    def db_url_test(self) -> str:
        """
        Путь подключения к тестовой PostgresSQL для запуска unit-тестов.
        :return: dsn
        """
        return f"postgresql+asyncpg://" \
               f"test:" \
               f"test@" \
               f"localhost:" \
               f"5432/" \
               f"test"

    # секреты для JWT
    SECRET_KEY: str = "secretKey"
    ALGORITHM: str = "HS256"

    @property
    def secret_key(self) -> str:
        return self.SECRET_KEY

    @property
    def sha_algorithm(self) -> str:
        return self.ALGORITHM

    # конфиг для redis
    REDIS_HOST: Optional[str]
    REDIS_PORT: Optional[int]

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    # конфиг для почтовой рассылки для celery
    SMTP_HOST: Optional[str]
    SMTP_PORT: Optional[int]
    SMTP_GMAIL: Optional[str]
    SMTP_PASSWORD: Optional[str]

    class Config:
        """
        Парсинг конфиг файла.
        """
        env_file = "creds.env"


cfg = Cfg()
