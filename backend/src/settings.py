from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    access_token_expire_minutes: int = 50400
    algorithm: str = "HS256"
    allowed_origins: list[str] = ["*"]
    refresh_token_expire_minutes: int = 86400
    pagination_max_per_page: int = 100

    secret_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow",
    )


settings = Settings()
