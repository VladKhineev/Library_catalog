from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

    POSTGRES_URL: str
    JSONBIN_MASTER_KEY: str
    JSONBIN_BIN_ID: str


settings = Settings()  # Через Depends желателньо прокинуть где будешь юзать или создать def get_settings()
