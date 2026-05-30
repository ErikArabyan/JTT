from functools import lru_cache
from os import getenv
from urllib.parse import quote_plus

DEFAULT_POSTGRES_HOST = "localhost"
DEFAULT_POSTGRES_PORT = "5432"
DEFAULT_POSTGRES_DB = "JTT"
DEFAULT_POSTGRES_USER = "postgres"
DEFAULT_POSTGRES_PASSWORD = "password"


class Settings:
    postgres_host: str
    postgres_port: str
    postgres_db: str
    postgres_user: str
    postgres_password: str

    def __init__(self) -> None:
        self.postgres_host = getenv("POSTGRES_HOST", DEFAULT_POSTGRES_HOST)
        self.postgres_port = getenv("POSTGRES_PORT", DEFAULT_POSTGRES_PORT)
        self.postgres_db = getenv("POSTGRES_DB", DEFAULT_POSTGRES_DB)
        self.postgres_user = getenv("POSTGRES_USER", DEFAULT_POSTGRES_USER)
        self.postgres_password = getenv("POSTGRES_PASSWORD", DEFAULT_POSTGRES_PASSWORD)

    @property
    def async_database_url(self) -> str:
        return self._build_async_database_url(self.postgres_db)

    @property
    def async_maintenance_database_url(self) -> str:
        return self._build_async_database_url("postgres")

    def _build_async_database_url(self, database_name: str) -> str:
        required_fields = {
            "POSTGRES_HOST": self.postgres_host,
            "POSTGRES_PORT": self.postgres_port,
            "POSTGRES_DB": database_name,
            "POSTGRES_USER": self.postgres_user,
            "POSTGRES_PASSWORD": self.postgres_password,
        }
        missing_fields = [name for name, value in required_fields.items() if not value]
        if missing_fields:
            missing = ", ".join(missing_fields)
            raise RuntimeError(f"Postgres connection settings are empty: {missing}.")

        user = quote_plus(self.postgres_user)
        password = quote_plus(self.postgres_password)
        host = self.postgres_host
        port = self.postgres_port
        database = quote_plus(database_name)
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
