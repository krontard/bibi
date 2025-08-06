"""
Обработчик сообщений для общения с AI
"""

from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
from database.db import AsyncSessionLocal
from services.user_service import UserService
from services.ai_factory import ai_factory
from models.message import Message
import logging
import time
import asyncio


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Основной обработчик текстовых сообщений"""
    
    user = update.effective_user
    message_text = update.message.text
    
    if not message_text or message_text.strip() == "":
        await update.message.reply_text("🤔 Пожалуйста, отправьте текстовое сообщение.")
        return
    
    logging.info(f"Получено сообщение от пользователя {user.id}: {message_text[:50]}...")
    
    # Показываем, что бот печатает
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )
    
    start_time = time.time()
    
    async with AsyncSessionLocal() as db_session:
        try:
            # Получаем или создаем пользователя
            user_service = UserService(db_session)
            user_obj = await user_service.get_or_create_user(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            
            # Получаем выбранную модель
            current_model = user_obj.current_ai_model
            
            # Получаем AI сервис
            ai_service = ai_factory.get_service(current_model)
            
            if not ai_service:
                await send_model_unavailable_message(update, current_model)
                return
            
            # Генерируем ответ от AI
            try:
                # Получаем контекст предыдущих сообщений (последние 5)
                context_messages = await get_conversation_context(db_session, user_obj.id, limit=5)
                context_text = format_context(context_messages) if context_messages else None
                
                ai_response = await ai_service.generate_response(
                    message=message_text,
                    context=context_text
                )
                
                # Вычисляем время обработки
                processing_time = int((time.time() - start_time) * 1000)
                
                # Сохраняем сообщение в базу данных
                message_obj = Message(
                    user_id=user_obj.id,
                    user_message=message_text,
                    ai_response=ai_response,
                    ai_model_used=current_model,
                    telegram_message_id=update.message.message_id,
                    processing_time=processing_time
                )
                
                db_session.add(message_obj)
                await db_session.commit()
                
                # Отправляем ответ пользователю
                model_emoji = get_model_emoji(current_model)
                response_text = f"{model_emoji} <b>{ai_service.get_model_name()}</b>\n\n{ai_response}"
                
                await update.message.reply_text(
                    response_text,
                    parse_mode='HTML'
                )
                
                logging.info(f"Отправлен ответ пользователю {user.id} ({processing_time}ms)")
                
            except Exception as e:
                logging.error(f"Ошибка при генерации ответа AI: {e}")
                await update.message.reply_text(
                    "😔 Извините, произошла ошибка при обработке вашего запроса. "
                    "Попробуйте еще раз через несколько секунд."
                )
                
        except Exception as e:
            logging.error(f"Ошибка в обработчике сообщений: {e}")
            await update.message.reply_text(
                "😔 Произошла внутренняя ошибка. Попробуйте использовать команду /start для перезапуска."
            )


async def get_conversation_context(db_session, user_id: int, limit: int = 5) -> list:
    """Получение контекста беседы из базы данных"""
    
    from sqlalchemy.future import select
    from sqlalchemy import desc
    
    try:
        # Получаем последние сообщения пользователя
        result = await db_session.execute(
            select(Message)
            .where(Message.user_id == user_id)
            .where(Message.ai_response.isnot(None))
            .order_by(desc(Message.created_at))
            .limit(limit)
        )
        
        messages = result.scalars().all()
        return list(reversed(messages))  # Возвращаем в хронологическом порядке
        
    except Exception as e:
        logging.error(f"Ошибка получения контекста: {e}")
        return []


def format_context(messages: list) -> str:
    """Форматирование контекста для передачи в AI"""
    
    if not messages:
        return None
    
    context_parts = []
    for msg in messages:
        context_parts.append(f"Пользователь: {msg.user_message}")
        if msg.ai_response:
            context_parts.append(f"Ассистент: {msg.ai_response}")
    
    return "\n\n".join(context_parts)


async def send_model_unavailable_message(update: Update, model_name: str):
    """Отправка сообщения о недоступности модели"""
    
    available_models = ai_factory.get_available_models()
    available_list = [name for name, available in available_models.items() if available]
    
    if not available_list:
        error_text = """
😔 <b>К сожалению, ни одна AI модель сейчас недоступна.</b>

Это может быть связано с:
• Отсутствием API ключей
• Проблемами с подключением к сервисам

Обратитесь к администратору для настройки API ключей.
"""
    else:
        available_names = ", ".join(available_list)
        error_text = f"""
😔 <b>Модель {model_name} сейчас недоступна.</b>

Доступные модели: {available_names}

Используйте команду /model для выбора другой модели.
"""
    
    await update.message.reply_text(error_text, parse_mode='HTML')


def get_model_emoji(model_name: str) -> str:
    """Получение эмодзи для модели"""
    
    emojis = {
        "chatgpt": "🧠",
        "claude": "🎭",
        "deepseek": "🚀"
    }
    
    return emojis.get(model_name, "🤖")


async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик голосовых сообщений (пока заглушка)"""
    
    await update.message.reply_text(
        "🎤 Голосовые сообщения пока не поддерживаются.\n"
        "Пожалуйста, отправьте текстовое сообщение."
    )


async def handle_photo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик фото сообщений (пока заглушка)"""
    
    await update.message.reply_text(
        "📸 Обработка изображений пока не поддерживается.\n"
        "Пожалуйста, отправьте текстовое сообщение с вашим вопросом."
    )


def register_chat_handlers(application: Application):
    """Регистрация обработчиков сообщений"""
    
    # Обработчик текстовых сообщений (исключая команды)
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )
    
    # Обработчик голосовых сообщений
    application.add_handler(
        MessageHandler(
            filters.VOICE,
            handle_voice_message
        )
    )
    
    # Обработчик фото
    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_photo_message
        )
    )
    
    logging.info("Зарегистрированы обработчики сообщений")