"""
Модуль настройки логирования
"""

import logging
import sys
from loguru import logger
from config.settings import settings


class InterceptHandler(logging.Handler):
    """Обработчик для перехвата стандартных логов Python"""
    
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logger():
    """Настройка системы логирования"""
    
    # Удаляем стандартный обработчик loguru
    logger.remove()
    
    # Добавляем новый обработчик с нашими настройками
    logger.add(
        sys.stdout,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
               "<level>{message}</level>",
        colorize=True,
    )
    
    # Добавляем файловый обработчик
    logger.add(
        "logs/telegpt.log",
        level=settings.log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
    )
    
    # Перехватываем стандартные логи Python
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)