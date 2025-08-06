"""
Фабрика для создания и управления AI сервисами
"""

from typing import Optional, Dict
from .ai_service import AIService
from .chatgpt_service import ChatGPTService
from .claude_service import ClaudeService
from .deepseek_service import DeepSeekService
from config.settings import settings
import logging


class AIServiceFactory:
    """Фабрика для создания AI сервисов"""
    
    _instances: Dict[str, AIService] = {}
    
    @classmethod
    def get_service(cls, model_name: str) -> Optional[AIService]:
        """
        Получение экземпляра AI сервиса по названию модели
        
        Args:
            model_name: Название модели (chatgpt, claude, deepseek)
            
        Returns:
            Экземпляр AI сервиса или None если модель недоступна
        """
        
        # Проверяем кэш экземпляров
        if model_name in cls._instances:
            return cls._instances[model_name]
        
        # Создаем новый экземпляр
        service = cls._create_service(model_name)
        if service and service.is_available():
            cls._instances[model_name] = service
            return service
        
        return None
    
    @classmethod
    def _create_service(cls, model_name: str) -> Optional[AIService]:
        """Создание экземпляра AI сервиса"""
        
        try:
            if model_name == "chatgpt":
                if not settings.openai_api_key:
                    logging.warning("OpenAI API key не настроен")
                    return None
                return ChatGPTService(settings.openai_api_key)
            
            elif model_name == "claude":
                if not settings.anthropic_api_key:
                    logging.warning("Anthropic API key не настроен")
                    return None
                return ClaudeService(settings.anthropic_api_key)
            
            elif model_name == "deepseek":
                if not settings.deepseek_api_key:
                    logging.warning("DeepSeek API key не настроен")
                    return None
                return DeepSeekService(settings.deepseek_api_key)
            
            else:
                logging.error(f"Неизвестная модель: {model_name}")
                return None
                
        except Exception as e:
            logging.error(f"Ошибка создания сервиса {model_name}: {e}")
            return None
    
    @classmethod
    def get_available_models(cls) -> Dict[str, bool]:
        """
        Получение списка доступных моделей
        
        Returns:
            Словарь {model_name: is_available}
        """
        
        models = {
            "chatgpt": bool(settings.openai_api_key),
            "claude": bool(settings.anthropic_api_key),
            "deepseek": bool(settings.deepseek_api_key)
        }
        
        return models
    
    @classmethod
    def get_default_model(cls) -> str:
        """
        Получение модели по умолчанию (первая доступная)
        
        Returns:
            Название модели по умолчанию
        """
        
        available = cls.get_available_models()
        
        # Приоритет: ChatGPT -> Claude -> DeepSeek
        for model in ["chatgpt", "claude", "deepseek"]:
            if available.get(model, False):
                return model
        
        # Если ни одна не доступна, возвращаем ChatGPT
        return "chatgpt"
    
    @classmethod
    def clear_cache(cls):
        """Очистка кэша экземпляров сервисов"""
        cls._instances.clear()
        logging.info("Кэш AI сервисов очищен")


# Глобальный экземпляр фабрики
ai_factory = AIServiceFactory()