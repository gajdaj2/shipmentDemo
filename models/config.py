from pydantic_settings import SettingsConfigDict
from pydantic_settings.main import BaseSettings


class DatabaseSettings(BaseSettings):
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = DatabaseSettings()  # pyright: ignore[reportCallIssue]

print(settings.POSTGRES_PASSWORD)
print(settings.POSTGRES_USER)
