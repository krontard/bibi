"""
Базовый интерфейс для AI сервисов
"""

from abc import ABC, abstractmethod
from typing import Optional


class AIService(ABC):
    """Абстрактный базовый класс для всех AI сервисов"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @abstractmethod
    async def generate_response(self, message: str, context: Optional[str] = None) -> str:
        """
        Генерация ответа от AI модели
        
        Args:
            message: Сообщение пользователя
            context: Контекст беседы (опционально)
            
        Returns:
            Ответ от AI модели
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """Получение названия модели"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Проверка доступности сервиса"""
        pass