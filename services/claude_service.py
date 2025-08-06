"""
Сервис для работы с Claude/Anthropic API
"""

import anthropic
from typing import Optional
import logging
from .ai_service import AIService


class ClaudeService(AIService):
    """Сервис для работы с Claude"""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        super().__init__(api_key)
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = model
    
    async def generate_response(self, message: str, context: Optional[str] = None) -> str:
        """Генерация ответа от Claude"""
        try:
            prompt = message
            if context:
                prompt = f"Контекст: {context}\n\nВопрос: {message}"
            
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            logging.error(f"Ошибка при обращении к Claude: {e}")
            return "Извините, произошла ошибка при обработке вашего запроса."
    
    def get_model_name(self) -> str:
        """Получение названия модели"""
        return f"Claude ({self.model})"
    
    def is_available(self) -> bool:
        """Проверка доступности сервиса"""
        return bool(self.api_key)