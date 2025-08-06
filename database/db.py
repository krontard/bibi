"""
Модуль работы с базой данных
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config.settings import settings
import logging


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""
    pass


# Создание асинхронного движка
engine = create_async_engine(
    settings.database_url.replace("sqlite://", "sqlite+aiosqlite://"),
    echo=settings.log_level == "DEBUG"
)

# Создание фабрики сессий
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


async def get_db() -> AsyncSession:
    """Получение сессии базы данных"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_database():
    """Инициализация базы данных"""
    logging.info("Инициализация базы данных...")
    
    async with engine.begin() as conn:
        # Импортируем все модели для создания таблиц
        from models.user import User
        from models.message import Message
        from models.ai_model import AIModel
        
        # Создаем все таблицы
        await conn.run_sync(Base.metadata.create_all)
    
    logging.info("База данных инициализирована успешно!")