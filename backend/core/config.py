import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "EvalMesh Enterprise AI Operations Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = os.getenv("EVALMESH_ENV", "production")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1")
    
    # Database Settings
    DB_ENGINE: str = os.getenv("EVALMESH_DB_ENGINE", "sqlite")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./evalmesh.db" if DB_ENGINE == "sqlite" else "postgresql+asyncpg://postgres:postgres@localhost:5432/evalmesh"
    )
    
    # Redis Cache Settings
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "evalmesh_super_secret_jwt_key_2026_change_in_production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 Days

    class Config:
        case_sensitive = True

settings = Settings()
