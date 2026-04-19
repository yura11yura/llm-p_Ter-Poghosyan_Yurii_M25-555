from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс конфигурации приложения, загружающий настройки из переменных окружения."""
    app_name: str
    env: str
    sqlite_path: str
    openrouter_api_key: str
    openrouter_base_url: str
    openrouter_model: str
    openrouter_site_url: str
    openrouter_app_name: str
    jwt_secret: str
    jwt_alg: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
