from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class PostgresSettings(BaseModel):
    """Настройки для подключения к POSTGRES"""

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str


class Settings(BaseSettings):
    psql_settings: PostgresSettings

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='__',
    )


settings = Settings()
print(settings)
