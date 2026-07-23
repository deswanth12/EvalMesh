import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "EvalMesh Control Plane"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # Provider Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    
    # Feature Flags
    SMART_ROUTING_ENABLED: bool = True
    AUTO_FAILOVER_ENABLED: bool = True
    DEFAULT_FAILOVER_PROVIDER: str = "anthropic"
    
    class Config:
        env_file = ".env"

settings = Settings()
