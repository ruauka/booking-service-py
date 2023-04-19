from pydantic import BaseSettings


class Cfg(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SECRET_KEY: str
    ALGORITHM: str

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://" \
               f"{self.POSTGRES_USER}:" \
               f"{self.POSTGRES_PASSWORD}@" \
               f"{self.DB_HOST}:" \
               f"{self.DB_PORT}/" \
               f"{self.POSTGRES_DB}"

    @property
    def secret_key(self) -> str:
        return self.SECRET_KEY

    @property
    def sha_algorithm(self) -> str:
        return self.ALGORITHM

    class Config:
        env_file = "creds.env"


cfg = Cfg()
