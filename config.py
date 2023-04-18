from pydantic import BaseSettings


class Cfg(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def secret_key(self) -> str:
        return self.SECRET_KEY

    @property
    def sha_algorithm(self) -> str:
        return self.ALGORITHM

    class Config:
        env_file = ".env"


cfg = Cfg()
