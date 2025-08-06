"""
TeleGPT - Telegram бот для общения с различными AI моделями
С адаптивным polling для быстрых ответов
"""

import asyncio
import logging
import platform
import time
from typing import Dict, Set
from telegram.ext import Application

from bot.handlers import register_handlers
from config.settings import settings
from utils.logger import setup_logger
from database.db import init_database


class AdaptivePolling:
    """Адаптивный polling для TeleGPT"""
    
    def __init__(self, application: Application):
        self.application = application
        self.active_users: Set[int] = set()
        self.last_activity: Dict[int, float] = {}
        self.normal_interval = 10  # Обычный интервал (секунды)
        self.fast_interval = 2     # Быстрый интервал (секунды)
        self.activity_timeout = 20  # Таймаут активности (секунды)
        self.running = False
    
    def add_active_user(self, user_id: int):
        """Добавить пользователя в активные"""
        self.active_users.add(user_id)
        self.last_activity[user_id] = time.time()
        logging.info(f"⚡ Пользователь {user_id} активен - быстрый polling ({self.fast_interval}с)")
    
    def remove_active_user(self, user_id: int):
        """Убрать пользователя из активных"""
        self.active_users.discard(user_id)
        if user_id in self.last_activity:
            del self.last_activity[user_id]
        if not self.active_users:
            logging.info(f"🐌 Переключение на обычный polling ({self.normal_interval}с)")
    
    def cleanup_inactive_users(self):
        """Очистка неактивных пользователей"""
        current_time = time.time()
        inactive_users = [
            user_id for user_id, last_time in self.last_activity.items()
            if current_time - last_time > self.activity_timeout
        ]
        
        for user_id in inactive_users:
            self.remove_active_user(user_id)
    
    def get_current_interval(self) -> int:
        """Получить текущий интервал polling"""
        self.cleanup_inactive_users()
        return self.fast_interval if self.active_users else self.normal_interval
    
    async def start_adaptive_polling(self):
        """Запуск адаптивного polling"""
        logging.info("🚀 Адаптивный polling запущен")
        logging.info(f"⏱️ Обычный: {self.normal_interval}с, быстрый: {self.fast_interval}с")
        
        self.running = True
        current_interval = self.normal_interval
        last_update_id = 0
        
        while self.running:
            try:
                # Получаем новый интервал
                new_interval = self.get_current_interval()
                
                if new_interval != current_interval:
                    current_interval = new_interval
                    mode = "быстрый ⚡" if current_interval == self.fast_interval else "обычный 🐌"
                    logging.info(f"🔄 Режим: {mode} ({current_interval}с)")
                
                # Получаем обновления
                updates = await self.application.bot.get_updates(
                    offset=last_update_id,
                    limit=100,
                    timeout=5,
                    allowed_updates=["message", "callback_query"]
                )
                
                if updates:
                    for update in updates:
                        # Активируем быстрый polling для текстовых сообщений
                        if (update.message and update.message.text and 
                            not update.message.text.startswith('/') and
                            update.effective_user):
                            
                            self.add_active_user(update.effective_user.id)
                        
                        # Обрабатываем обновление
                        self.application.update_queue.put_nowait(update)
                        last_update_id = update.update_id + 1
                
                await asyncio.sleep(current_interval)
                
            except Exception as e:
                logging.error(f"❌ Ошибка в адаптивном polling: {e}")
                await asyncio.sleep(5)
    
    def stop(self):
        """Остановка polling"""
        self.running = False


class TeleGPTBot:
    """Основной класс TeleGPT бота"""
    
    def __init__(self):
        self.application = None
        self.adaptive_polling = None
        self.running = False
    
    async def initialize(self):
        """Инициализация бота"""
        setup_logger()
        logging.info("🤖 Инициализация TeleGPT с адаптивным polling...")
        
        # Инициализация базы данных
        await init_database()
        
        # Создание приложения бота
        self.application = Application.builder().token(settings.telegram_token).build()
        
        # Регистрация обработчиков
        register_handlers(self.application)
        
        # Создание адаптивного polling
        self.adaptive_polling = AdaptivePolling(self.application)
        
        # Добавляем middleware для деактивации после обработки
        self.add_completion_middleware()
        
        logging.info("✅ TeleGPT готов к работе!")
    
    def add_completion_middleware(self):
        """Middleware для деактивации быстрого polling после обработки"""
        
        # Находим обработчик текстовых сообщений
        for group in self.application.handlers.values():
            for handler in group:
                if (hasattr(handler, 'filters') and 
                    str(handler.filters).find('TEXT') != -1 and
                    hasattr(handler, 'callback')):
                    
                    original_callback = handler.callback
                    
                    async def completion_wrapper(update, context, original_func=original_callback):
                        user_id = update.effective_user.id if update.effective_user else None
                        
                        try:
                            # Вызываем оригинальный обработчик
                            result = await original_func(update, context)
                            return result
                            
                        finally:
                            # После обработки убираем пользователя из активных
                            if (user_id and self.adaptive_polling and 
                                user_id in self.adaptive_polling.active_users):
                                
                                await asyncio.sleep(3)  # Небольшая задержка
                                self.adaptive_polling.remove_active_user(user_id)
                    
                    handler.callback = completion_wrapper
                    break
    
    async def start(self):
        """Запуск бота"""
        if not self.application:
            await self.initialize()
        
        logging.info("🚀 Запуск TeleGPT бота...")
        self.running = True
        
        try:
            # Инициализация приложения
            await self.application.initialize()
            await self.application.start()
            
            # Запуск процессора обновлений
            processor_task = asyncio.create_task(self.process_updates())
            
            # Запуск адаптивного polling
            await self.adaptive_polling.start_adaptive_polling()
            
        except Exception as e:
            logging.error(f"❌ Ошибка запуска: {e}")
            raise
        finally:
            if 'processor_task' in locals():
                processor_task.cancel()
    
    async def process_updates(self):
        """Обработка обновлений из очереди"""
        logging.info("🔄 Процессор обновлений запущен")
        
        while self.running:
            try:
                try:
                    update = await asyncio.wait_for(
                        asyncio.to_thread(self.application.update_queue.get),
                        timeout=1.0
                    )
                    await self.application.process_update(update)
                except asyncio.TimeoutError:
                    continue
                    
            except Exception as e:
                logging.error(f"❌ Ошибка обработки: {e}")
                await asyncio.sleep(1)
    
    async def stop(self):
        """Остановка бота"""
        logging.info("🛑 Остановка TeleGPT...")
        self.running = False
        
        if self.adaptive_polling:
            self.adaptive_polling.stop()
        
        if self.application:
            await self.application.stop()
            await self.application.shutdown()
        
        logging.info("✅ TeleGPT остановлен")


async def main():
    """Основная функция запуска"""
    # Исправление для Windows
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    bot = TeleGPTBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logging.info("⌨️ Получен сигнал остановки")
    except Exception as e:
        logging.error(f"💥 Критическая ошибка: {e}")
    finally:
        await bot.stop()


if __name__ == "__main__":
    print("🚀 TeleGPT - Telegram бот с адаптивным polling")
    print("⚡ Быстрые ответы во время обработки AI запросов")
    print("🐌 Экономия ресурсов в режиме ожидания")
    print("📋 Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 TeleGPT остановлен")
    except Exception as e:
        print(f"\n💥 Ошибка: {e}")