from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки проекта."""
    time_sleep: int = Field("sleep", env="TIME_SLEEP")
    rss_link: str = Field("link", env="RSS_LINK")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
