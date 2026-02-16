from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "ProcessData Serverless"
    API_VERSION: str = "/api/v1"
    ENVIRONMENT: str = "development"
    
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 540
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty = True,
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
settings = Settings()