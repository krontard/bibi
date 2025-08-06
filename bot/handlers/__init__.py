"""
Модуль обработчиков команд и сообщений
"""

from telegram.ext import Application
from .start_handler import register_start_handlers
from .model_handler import register_model_handlers  
from .chat_handler import register_chat_handlers


def register_handlers(application: Application):
    """Регистрация всех обработчиков"""
    register_start_handlers(application)
    register_model_handlers(application)
    register_chat_handlers(application)