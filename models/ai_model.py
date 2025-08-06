"""
Модель AI модели
"""

from sqlalchemy import Column, Integer, String, Boolean, Text
from database.db import Base


class AIModel(Base):
    """Модель доступных AI моделей"""
    
    __tablename__ = "ai_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    # Настройки модели
    is_active = Column(Boolean, default=True, nullable=False)
    api_endpoint = Column(String, nullable=True)
    max_tokens = Column(Integer, default=4000, nullable=False)
    
    # Метаданные
    provider = Column(String, nullable=False)  # openai, anthropic, deepseek
    model_version = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<AIModel(name={self.name}, provider={self.provider})>"