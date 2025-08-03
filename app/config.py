import secrets
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, computed_field
from pydantic_core import MultiHostUrl


def generate_secret_key() -> str:
    return secrets.token_urlsafe(32)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_ignore_empty=True,
        extra="ignore",
    )

    secret_key: str = Field(description="Secret key ")
    algorithm: str = Field(description="Algorithm")
    postgres_user: str = Field(description="Postgres user")
    postgres_password: str = Field(description="Postgres password")
    postgres_host: str = Field(description="Postgres host")
    postgres_port: int = Field(default=5432, description="Postgres port")
    postgres_db: str = Field(description="Postgres database")

    @computed_field
    @property
    def database_url(self) -> str:
        url = MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            path=self.postgres_db,
        )

        return str(url)


settings = Settings()
