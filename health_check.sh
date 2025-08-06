#!/bin/bash

# Скрипт проверки здоровья TeleGPT бота
# Добавьте в crontab: */5 * * * * /path/to/health_check.sh

LOG_FILE="logs/health.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Создание директории логов если не существует
mkdir -p logs

# Функция логирования
log() {
    echo "[$TIMESTAMP] $1" >> $LOG_FILE
    echo "[$TIMESTAMP] $1"
}

# Проверка работы Docker Compose
if ! docker-compose ps | grep -q "Up"; then
    log "❌ TeleGPT контейнер не работает, попытка перезапуска..."
    
    # Остановка контейнеров
    docker-compose down >> $LOG_FILE 2>&1
    
    # Запуск контейнеров
    docker-compose up -d >> $LOG_FILE 2>&1
    
    # Ожидание запуска
    sleep 30
    
    # Повторная проверка
    if docker-compose ps | grep -q "Up"; then
        log "✅ TeleGPT успешно перезапущен"
    else
        log "❌ Не удалось перезапустить TeleGPT"
        # Отправка уведомления (опционально)
        # curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
        #      -d chat_id="$ADMIN_CHAT_ID" \
        #      -d text="❌ TeleGPT на VPS не работает!"
    fi
else
    log "✅ TeleGPT работает нормально"
fi

# Очистка старых логов (оставляем только последние 1000 строк)
tail -n 1000 $LOG_FILE > ${LOG_FILE}.tmp && mv ${LOG_FILE}.tmp $LOG_FILE