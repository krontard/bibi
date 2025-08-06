"""
Модель сообщения
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.db import Base


class Message(Base):
    """Модель сообщения в чате"""
    
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Содержимое сообщения
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=True)
    ai_model_used = Column(String, nullable=False)
    
    # Метаданные
    telegram_message_id = Column(Integer, nullable=True)
    processing_time = Column(Integer, nullable=True)  # в миллисекундах
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Связи
    user = relationship("User", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, user_id={self.user_id}, ai_model={self.ai_model_used})>"