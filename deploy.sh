#!/bin/bash

echo "🚀 Развертывание TeleGPT на VPS"

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден!"
    echo "📋 Скопируйте env.example в .env и настройте API ключи"
    exit 1
fi

# Создание необходимых директорий
mkdir -p data logs

# Обновление кода (если это не первый запуск)
if [ -d ".git" ]; then
    echo "📥 Обновление кода..."
    git pull origin main
fi

# Остановка старых контейнеров
echo "🛑 Остановка старых контейнеров..."
docker-compose down

# Пересборка и запуск
echo "🔨 Сборка и запуск контейнеров..."
docker-compose up --build -d

# Ожидание запуска
sleep 10

# Проверка статуса
echo "📊 Статус контейнеров:"
docker-compose ps

echo ""
echo "✅ Развертывание завершено!"
echo "📋 Полезные команды:"
echo "   Просмотр логов:    docker-compose logs -f"
echo "   Перезапуск:        docker-compose restart"
echo "   Остановка:         docker-compose down"
echo "   Статус:            docker-compose ps"