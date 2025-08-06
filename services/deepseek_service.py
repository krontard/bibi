"""
Сервис для работы с DeepSeek API
"""

import aiohttp
import json
from typing import Optional
import logging
from .ai_service import AIService


class DeepSeekService(AIService):
    """Сервис для работы с DeepSeek"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        super().__init__(api_key)
        self.model = model
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
    
    async def generate_response(self, message: str, context: Optional[str] = None) -> str:
        """Генерация ответа от DeepSeek"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = []
            if context:
                messages.append({"role": "system", "content": context})
            
            messages.append({"role": "user", "content": message})
            
            data = {
                "model": self.model,
                "messages": messages,
                "max_tokens": 4000,
                "temperature": 0.7
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"].strip()
                    else:
                        logging.error(f"DeepSeek API вернул статус {response.status}")
                        return "Извините, сервис временно недоступен."
                        
        except Exception as e:
            logging.error(f"Ошибка при обращении к DeepSeek: {e}")
            return "Извините, произошла ошибка при обработке вашего запроса."
    
    def get_model_name(self) -> str:
        """Получение названия модели"""
        return f"DeepSeek ({self.model})"
    
    def is_available(self) -> bool:
        """Проверка доступности сервиса"""
        return bool(self.api_key)