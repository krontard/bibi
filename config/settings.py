"""
Настройки приложения
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Класс настроек приложения"""
    
    # Telegram Bot Token
    telegram_token: str = Field("dummy_token_for_testing", env="TELEGRAM_BOT_TOKEN")
    
    # AI API Keys
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    deepseek_api_key: Optional[str] = Field(None, env="DEEPSEEK_API_KEY")
    
    # Database
    database_url: str = Field("sqlite:///telegpt.db", env="DATABASE_URL")
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    # Rate Limiting
    max_requests_per_minute: int = Field(10, env="MAX_REQUESTS_PER_MINUTE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Глобальный экземпляр настроек
settings = Settings()