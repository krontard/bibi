#!/bin/bash

# Скрипт резервного копирования TeleGPT
# Добавьте в crontab: 0 2 * * * /home/telegpt/bibi/backup.sh

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="logs/backup.log"

# Создание директорий
mkdir -p $BACKUP_DIR logs

# Функция логирования
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

log "🗄️ Начало резервного копирования..."

# Резервное копирование базы данных
if [ -f "data/telegpt.db" ]; then
    cp data/telegpt.db $BACKUP_DIR/telegpt_${TIMESTAMP}.db
    log "✅ База данных скопирована: telegpt_${TIMESTAMP}.db"
else
    log "⚠️ База данных не найдена"
fi

# Резервное копирование логов
if [ -d "logs" ]; then
    tar -czf $BACKUP_DIR/logs_${TIMESTAMP}.tar.gz logs/
    log "✅ Логи архивированы: logs_${TIMESTAMP}.tar.gz"
fi

# Резервное копирование конфигурации
if [ -f ".env" ]; then
    cp .env $BACKUP_DIR/env_${TIMESTAMP}.backup
    log "✅ Конфигурация скопирована: env_${TIMESTAMP}.backup"
fi

# Удаление старых бэкапов (старше 30 дней)
find $BACKUP_DIR -name "telegpt_*.db" -mtime +30 -delete
find $BACKUP_DIR -name "logs_*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "env_*.backup" -mtime +30 -delete

log "🧹 Старые бэкапы очищены"

# Подсчет размера бэкапов
BACKUP_SIZE=$(du -sh $BACKUP_DIR | cut -f1)
BACKUP_COUNT=$(ls -1 $BACKUP_DIR | wc -l)

log "📊 Статистика бэкапов: $BACKUP_COUNT файлов, общий размер: $BACKUP_SIZE"
log "✅ Резервное копирование завершено"

echo ""