"""
Сервис для работы с ChatGPT/OpenAI API
"""

import openai
from typing import Optional
import logging
from .ai_service import AIService


class ChatGPTService(AIService):
    """Сервис для работы с ChatGPT"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        super().__init__(api_key)
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def generate_response(self, message: str, context: Optional[str] = None) -> str:
        """Генерация ответа от ChatGPT"""
        try:
            messages = []
            
            if context:
                messages.append({"role": "system", "content": context})
            
            messages.append({"role": "user", "content": message})
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=4000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logging.error(f"Ошибка при обращении к ChatGPT: {e}")
            return "Извините, произошла ошибка при обработке вашего запроса."
    
    def get_model_name(self) -> str:
        """Получение названия модели"""
        return f"ChatGPT ({self.model})"
    
    def is_available(self) -> bool:
        """Проверка доступности сервиса"""
        return bool(self.api_key)