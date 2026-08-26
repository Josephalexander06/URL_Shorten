from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "shorten_url"
    DB_URL: str
    SECRET_KEY: str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

