"""
Простой тест для проверки основных компонентов бота
"""

import asyncio
import sys
import os

# Добавляем корневую папку в путь
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
from database.db import init_database
from services.ai_factory import ai_factory
from utils.logger import setup_logger


async def test_database():
    """Тест инициализации базы данных"""
    print("🗄️ Тестирование базы данных...")
    
    try:
        await init_database()
        print("✅ База данных инициализирована успешно!")
        return True
    except Exception as e:
        print(f"❌ Ошибка инициализации БД: {e}")
        return False


def test_settings():
    """Тест настроек приложения"""
    print("⚙️ Тестирование настроек...")
    
    try:
        print(f"📱 Telegram token: {'✅ Настроен' if settings.telegram_token else '❌ Не настроен'}")
        print(f"🧠 OpenAI API: {'✅ Настроен' if settings.openai_api_key else '❌ Не настроен'}")
        print(f"🎭 Anthropic API: {'✅ Настроен' if settings.anthropic_api_key else '❌ Не настроен'}")
        print(f"🚀 DeepSeek API: {'✅ Настроен' if settings.deepseek_api_key else '❌ Не настроен'}")
        print(f"🗄️ Database URL: {settings.database_url}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка настроек: {e}")
        return False


def test_ai_factory():
    """Тест фабрики AI сервисов"""
    print("\n🤖 Тестирование AI фабрики...")
    
    try:
        available_models = ai_factory.get_available_models()
        print("Доступные модели:")
        
        for model, available in available_models.items():
            status = "✅ Доступна" if available else "❌ Недоступна"
            print(f"  • {model}: {status}")
        
        default_model = ai_factory.get_default_model()
        print(f"\n🎯 Модель по умолчанию: {default_model}")
        
        # Пробуем получить сервис
        service = ai_factory.get_service(default_model)
        if service:
            print(f"✅ Сервис {default_model} создан успешно: {service.get_model_name()}")
        else:
            print(f"❌ Не удалось создать сервис {default_model}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка AI фабрики: {e}")
        return False


async def test_ai_service():
    """Тест AI сервиса (если доступен)"""
    print("\n💬 Тестирование AI сервиса...")
    
    try:
        default_model = ai_factory.get_default_model()
        service = ai_factory.get_service(default_model)
        
        if not service:
            print("⚠️ AI сервис недоступен (нет API ключей)")
            return True
        
        print(f"🔄 Отправляем тестовый запрос к {service.get_model_name()}...")
        
        # Простой тестовый запрос
        response = await service.generate_response("Привет! Это тест.")
        
        if response and len(response) > 0:
            print(f"✅ Получен ответ от AI ({len(response)} символов)")
            print(f"📝 Ответ: {response[:100]}{'...' if len(response) > 100 else ''}")
        else:
            print("❌ Пустой ответ от AI")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Ошибка AI сервиса: {e}")
        return False


async def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов TeleGPT бота\n")
    
    # Настройка логирования
    setup_logger()
    
    tests = [
        ("Настройки", test_settings),
        ("База данных", test_database),
        ("AI Фабрика", test_ai_factory),
        ("AI Сервис", test_ai_service)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"🧪 Тест: {test_name}")
        print('='*50)
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            results.append((test_name, result))
            
        except Exception as e:
            print(f"❌ Критическая ошибка в тесте {test_name}: {e}")
            results.append((test_name, False))
    
    # Итоговый отчет
    print(f"\n{'='*50}")
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print('='*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ ПРОШЕЛ" if result else "❌ ПРОВАЛЕН"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Результат: {passed}/{total} тестов прошли успешно")
    
    if passed == total:
        print("🎉 Все тесты прошли! Бот готов к запуску.")
        print("\n📋 Следующие шаги:")
        print("1. Настройте .env файл с вашими API ключами")
        print("2. Запустите бота: python main.py")
    else:
        print("⚠️ Некоторые тесты провалены. Проверьте настройки.")


if __name__ == "__main__":
    asyncio.run(main())