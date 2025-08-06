"""
Обработчик выбора AI модели
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database.db import AsyncSessionLocal
from services.user_service import UserService
import logging


# Конфигурация доступных моделей
AVAILABLE_MODELS = {
    "chatgpt": {
        "name": "ChatGPT",
        "emoji": "🧠",
        "description": "Универсальный помощник от OpenAI",
        "provider": "OpenAI"
    },
    "claude": {
        "name": "Claude",
        "emoji": "🎭", 
        "description": "Продвинутая модель от Anthropic",
        "provider": "Anthropic"
    },
    "deepseek": {
        "name": "DeepSeek",
        "emoji": "🚀",
        "description": "Быстрая и эффективная модель",
        "provider": "DeepSeek"
    }
}


async def model_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /model"""
    
    user = update.effective_user
    logging.info(f"Пользователь {user.id} открыл меню выбора модели")
    
    # Получаем текущую модель пользователя
    async with AsyncSessionLocal() as db_session:
        user_service = UserService(db_session)
        current_model = await user_service.get_user_model(user.id)
        
        if not current_model:
            # Создаем пользователя если его нет
            await user_service.get_or_create_user(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            current_model = "chatgpt"  # по умолчанию
    
    text = f"""
🤖 <b>Выбор нейросети</b>

Текущая модель: {AVAILABLE_MODELS[current_model]['emoji']} <b>{AVAILABLE_MODELS[current_model]['name']}</b>

Выберите модель для общения:
"""
    
    # Создаем клавиатуру с моделями
    keyboard = []
    for model_key, model_info in AVAILABLE_MODELS.items():
        # Отмечаем текущую модель
        prefix = "✅ " if model_key == current_model else ""
        button_text = f"{prefix}{model_info['emoji']} {model_info['name']}"
        
        keyboard.append([
            InlineKeyboardButton(
                button_text, 
                callback_data=f"select_{model_key}"
            )
        ])
    
    # Добавляем кнопку "Назад"
    keyboard.append([
        InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text, 
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def model_selection_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора модели через inline кнопки"""
    
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    callback_data = query.data
    
    if callback_data == "select_model":
        # Показываем меню выбора модели
        await show_model_selection(query, user)
        
    elif callback_data.startswith("select_"):
        # Выбор конкретной модели
        model_key = callback_data.replace("select_", "")
        await handle_model_selection(query, user, model_key)
        
    elif callback_data == "back_to_main":
        # Возврат к главному меню
        await show_main_menu(query, user)
        
    elif callback_data == "help":
        # Показать справку
        await show_help_inline(query)


async def show_model_selection(query, user):
    """Показать меню выбора модели"""
    
    # Получаем текущую модель пользователя
    async with AsyncSessionLocal() as db_session:
        user_service = UserService(db_session)
        current_model = await user_service.get_user_model(user.id) or "chatgpt"
    
    text = f"""
🤖 <b>Выбор нейросети</b>

Текущая модель: {AVAILABLE_MODELS[current_model]['emoji']} <b>{AVAILABLE_MODELS[current_model]['name']}</b>

Выберите модель для общения:
"""
    
    # Создаем клавиатуру с моделями
    keyboard = []
    for model_key, model_info in AVAILABLE_MODELS.items():
        prefix = "✅ " if model_key == current_model else ""
        button_text = f"{prefix}{model_info['emoji']} {model_info['name']}"
        
        keyboard.append([
            InlineKeyboardButton(
                button_text, 
                callback_data=f"select_{model_key}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        text, 
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def handle_model_selection(query, user, model_key):
    """Обработка выбора конкретной модели"""
    
    if model_key not in AVAILABLE_MODELS:
        await query.edit_message_text("❌ Неизвестная модель!")
        return
    
    # Обновляем модель в базе данных
    async with AsyncSessionLocal() as db_session:
        user_service = UserService(db_session)
        success = await user_service.update_user_model(user.id, model_key)
        
        if not success:
            # Создаем пользователя если его нет
            await user_service.get_or_create_user(
                telegram_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name
            )
            await user_service.update_user_model(user.id, model_key)
    
    model_info = AVAILABLE_MODELS[model_key]
    
    success_text = f"""
✅ <b>Модель успешно изменена!</b>

{model_info['emoji']} <b>{model_info['name']}</b>
📝 {model_info['description']}
🏢 Провайдер: {model_info['provider']}

Теперь отправьте любое сообщение, и я отвечу с помощью выбранной модели!
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Выбрать другую", callback_data="select_model"),
            InlineKeyboardButton("🏠 Главная", callback_data="back_to_main")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        success_text, 
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    
    logging.info(f"Пользователь {user.id} выбрал модель {model_key}")


async def show_main_menu(query, user):
    """Показать главное меню"""
    
    welcome_text = f"""
🤖 <b>TeleGPT - Главное меню</b>

Привет, {user.first_name}! 

Я бот для общения с различными нейросетями:
• 🧠 ChatGPT (OpenAI)
• 🎭 Claude (Anthropic) 
• 🚀 DeepSeek

💡 Отправьте мне сообщение, и я отвечу с помощью выбранной нейросети!
"""
    
    keyboard = [
        [
            InlineKeyboardButton("🔄 Выбрать модель", callback_data="select_model"),
            InlineKeyboardButton("❓ Помощь", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        welcome_text, 
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def show_help_inline(query):
    """Показать справку через inline"""
    
    help_text = """
📖 <b>Краткая справка</b>

<b>📋 Команды:</b>
/start - Главное меню
/model - Выбор нейросети  
/help - Подробная справка
/clear - Очистить контекст

<b>💬 Использование:</b>
1. Выберите модель
2. Отправьте сообщение
3. Получите ответ от ИИ

Для подробной справки используйте команду /help
"""
    
    keyboard = [
        [InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        help_text, 
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


def register_model_handlers(application: Application):
    """Регистрация обработчиков выбора модели"""
    
    application.add_handler(CommandHandler("model", model_command))
    application.add_handler(CallbackQueryHandler(model_selection_callback))
    
    logging.info("Зарегистрированы обработчики выбора модели")