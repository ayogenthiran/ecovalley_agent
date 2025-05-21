from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "EcoValley Agent"
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4o-mini"
    DATABASE_URL: str = "sqlite:///./ecovalley.db"

    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env"
    )

@lru_cache()
def get_settings() -> Settings:
    return Settings() 