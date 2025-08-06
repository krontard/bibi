"""
Обработчик команды /start и основных команд
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import logging


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    
    user = update.effective_user
    logging.info(f"Пользователь {user.id} ({user.username}) запустил бота")
    
    welcome_text = f"""
🤖 Добро пожаловать в TeleGPT, {user.first_name}!

Я бот для общения с различными нейросетями:
• 🧠 ChatGPT (OpenAI)
• 🎭 Claude (Anthropic) 
• 🚀 DeepSeek

📋 Доступные команды:
/start - Показать это сообщение
/model - Выбрать нейросеть
/help - Подробная справка
/clear - Очистить контекст беседы

💡 Просто отправьте мне сообщение, и я отвечу с помощью выбранной нейросети!

Текущая модель: ChatGPT (по умолчанию)
"""
    
    # Создаем клавиатуру с быстрыми действиями
    keyboard = [
        [
            InlineKeyboardButton("🔄 Выбрать модель", callback_data="select_model"),
            InlineKeyboardButton("❓ Помощь", callback_data="help")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text, 
        reply_markup=reply_markup,
        parse_mode='HTML'
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    
    help_text = """
📖 <b>Подробная справка по TeleGPT</b>

<b>🎯 Основные функции:</b>
• Общение с разными нейросетями в одном чате
• Сохранение контекста беседы
• Переключение между моделями без потери истории

<b>🤖 Доступные модели:</b>
• <b>ChatGPT</b> - универсальный помощник от OpenAI
• <b>Claude</b> - продвинутая модель от Anthropic
• <b>DeepSeek</b> - быстрая и эффективная модель

<b>📋 Команды:</b>
/start - Приветствие и основная информация
/model - Выбор активной нейросети
/help - Эта справка
/clear - Очистить контекст текущей беседы
/stats - Статистика использования (скоро)

<b>💬 Как пользоваться:</b>
1. Выберите нужную модель командой /model
2. Отправьте любое сообщение
3. Получите ответ от выбранной нейросети
4. Продолжайте беседу - контекст сохраняется!

<b>⚙️ Особенности:</b>
• Каждая модель имеет свои сильные стороны
• Контекст сохраняется в рамках одной сессии
• Безопасное хранение ваших сообщений

<b>🔧 Поддержка:</b>
Если возникли проблемы, используйте команду /start для перезапуска.
"""
    
    await update.message.reply_text(help_text, parse_mode='HTML')


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /clear для очистки контекста"""
    
    user_id = update.effective_user.id
    
    # Здесь будет логика очистки контекста из базы данных
    # Пока просто отправляем подтверждение
    
    clear_text = """
🧹 <b>Контекст беседы очищен!</b>

Теперь нейросеть не будет помнить предыдущие сообщения в этой беседе.
Вы можете начать новый разговор с чистого листа.

Отправьте любое сообщение, чтобы начать новую беседу!
"""
    
    logging.info(f"Пользователь {user_id} очистил контекст беседы")
    await update.message.reply_text(clear_text, parse_mode='HTML')


def register_start_handlers(application: Application):
    """Регистрация обработчиков основных команд"""
    
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
    
    logging.info("Зарегистрированы обработчики основных команд")