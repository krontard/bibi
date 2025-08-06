# 🤖 TeleGPT

Telegram бот для общения с различными AI моделями с адаптивным polling для быстрых ответов.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Telegram Bot API](https://img.shields.io/badge/Telegram%20Bot%20API-Latest-blue.svg)](https://core.telegram.org/bots/api)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Особенности

- 🧠 **Поддержка 3 AI моделей**: ChatGPT, Claude, DeepSeek
- ⚡ **Адаптивный polling**: Быстрые ответы при активном использовании
- 🗄️ **Сохранение истории**: Контекст беседы в SQLite
- 🎛️ **Интуитивный интерфейс**: Inline кнопки для выбора модели
- 📊 **Подробное логирование**: Отслеживание всех действий
- 🔧 **Модульная архитектура**: Легко расширяемая структура

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/ваш-username/TeleGPT.git
cd TeleGPT
```

### 2. Создание виртуального окружения
```bash
python -m venv telegpt_env
# Windows:
telegpt_env\Scripts\activate
# macOS/Linux:
source telegpt_env/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения
```bash
# Скопируйте пример файла
copy env.example .env  # Windows
# cp env.example .env  # macOS/Linux

# Отредактируйте .env файл, добавив ваши API ключи
```

### 5. Запуск бота
```bash
python main.py
```

## Архитектура проекта

```
TeleGPT/
├── main.py                 # Точка входа в приложение
├── requirements.txt        # Зависимости Python
├── .env_example           # Пример файла с переменными окружения
├── bot/                   # Основная логика бота
│   ├── __init__.py
│   └── handlers/          # Обработчики команд и сообщений
│       ├── __init__.py
│       ├── start_handler.py    (планируется)
│       ├── model_handler.py    (планируется)
│       └── chat_handler.py     (планируется)
├── models/                # Модели данных (SQLAlchemy)
│   ├── __init__.py
│   ├── user.py           # Модель пользователя
│   ├── message.py        # Модель сообщения
│   └── ai_model.py       # Модель AI модели
├── services/              # Бизнес-логика и сервисы
│   ├── __init__.py
│   ├── ai_service.py     # Базовый интерфейс для AI
│   ├── chatgpt_service.py # Сервис ChatGPT
│   ├── claude_service.py  # Сервис Claude
│   ├── deepseek_service.py # Сервис DeepSeek
│   └── user_service.py    # Сервис пользователей
├── config/                # Конфигурация
│   ├── __init__.py
│   └── settings.py        # Настройки приложения
├── database/              # База данных
│   ├── __init__.py
│   └── db.py             # Подключение к БД
└── utils/                 # Утилиты
    ├── __init__.py
    └── logger.py          # Настройка логирования
```

## Установка и настройка

### 1. Создание виртуального окружения

```bash
# Создание виртуального окружения
python -m venv telegpt_env

# Активация виртуального окружения
# На Windows:
telegpt_env\Scripts\activate
# На macOS/Linux:
source telegpt_env/bin/activate
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

```bash
# Скопировать пример файла с переменными окружения
copy .env_example .env

# Отредактировать .env файл, добавив ваши API ключи:
# - TELEGRAM_BOT_TOKEN (обязательно)
# - OPENAI_API_KEY (для ChatGPT)
# - ANTHROPIC_API_KEY (для Claude)
# - DEEPSEEK_API_KEY (для DeepSeek)
```

### 4. Получение API ключей

#### Telegram Bot Token:
1. Найдите @BotFather в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в .env файл

#### OpenAI API Key (ChatGPT):
1. Перейдите на https://platform.openai.com/api-keys
2. Создайте новый API ключ
3. Скопируйте ключ в .env файл

#### Anthropic API Key (Claude):
1. Перейдите на https://console.anthropic.com/
2. Создайте новый API ключ
3. Скопируйте ключ в .env файл

#### DeepSeek API Key:
1. Перейдите на https://platform.deepseek.com/
2. Создайте новый API ключ
3. Скопируйте ключ в .env файл

## Что делать дальше

### Следующие шаги для завершения разработки:

1. **Создать обработчики команд** (`bot/handlers/`):
   - `start_handler.py` - приветствие и помощь
   - `model_handler.py` - выбор AI модели
   - `chat_handler.py` - обработка сообщений

2. **Создать фабрику AI сервисов** для управления различными моделями

3. **Добавить middleware** для:
   - Ограничения скорости запросов
   - Логирования действий пользователей
   - Обработки ошибок

4. **Улучшить базу данных**:
   - Добавить индексы для оптимизации
   - Создать миграции Alembic
   - Добавить кэширование

5. **Добавить дополнительные функции**:
   - Контекст беседы
   - Настройки температуры и других параметров
   - Статистика использования
   - Экспорт истории чата

6. **Тестирование и деплой**:
   - Написать unit тесты
   - Настроить CI/CD
   - Подготовить Docker контейнер

## Запуск проекта

```bash
# Убедитесь, что виртуальное окружение активировано
# и все зависимости установлены

# Запуск бота с адаптивным polling
python main.py
```

## Особенности адаптивного polling

TeleGPT использует **адаптивный polling** для оптимизации производительности:

- **🐌 Обычный режим**: 10 секунд между запросами (режим ожидания)
- **⚡ Быстрый режим**: 2 секунды между запросами (во время обработки AI)
- **🔄 Автопереключение**: Автоматически ускоряется при получении сообщений
- **⏰ Таймаут**: Через 20 секунд бездействия возвращается к обычному режиму

Это обеспечивает быстрые ответы при активном использовании и экономит ресурсы в режиме ожидания.

## Структура команд бота (планируется)

- `/start` - Приветствие и инструкции
- `/help` - Справка по командам
- `/model` - Выбор AI модели
- `/settings` - Настройки пользователя
- `/stats` - Статистика использования
- `/clear` - Очистка контекста беседы

## Технологии

- **Python 3.8+**
- **python-telegram-bot** - для работы с Telegram API
- **SQLAlchemy** - ORM для работы с базой данных
- **Pydantic** - валидация настроек
- **OpenAI API** - для ChatGPT
- **Anthropic API** - для Claude
- **DeepSeek API** - для DeepSeek
- **Loguru** - для логирования