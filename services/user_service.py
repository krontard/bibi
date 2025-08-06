"""
Сервис для работы с пользователями
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from typing import Optional
import logging


class UserService:
    """Сервис для управления пользователями"""
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def get_or_create_user(self, telegram_id: int, username: Optional[str] = None, 
                                first_name: Optional[str] = None, last_name: Optional[str] = None) -> User:
        """Получение или создание пользователя"""
        
        # Попытка найти существующего пользователя
        result = await self.db_session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            # Обновляем информацию о пользователе
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            await self.db_session.commit()
            logging.info(f"Обновлен пользователь {telegram_id}")
            return user
        
        # Создаем нового пользователя
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        
        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)
        
        logging.info(f"Создан новый пользователь {telegram_id}")
        return user
    
    async def update_user_model(self, telegram_id: int, model_name: str) -> bool:
        """Обновление выбранной AI модели пользователя"""
        
        result = await self.db_session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        
        if user:
            user.current_ai_model = model_name
            await self.db_session.commit()
            logging.info(f"Пользователь {telegram_id} выбрал модель {model_name}")
            return True
        
        return False
    
    async def get_user_model(self, telegram_id: int) -> Optional[str]:
        """Получение текущей AI модели пользователя"""
        
        result = await self.db_session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        
        return user.current_ai_model if user else None