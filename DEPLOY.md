# 🚀 Развертывание TeleGPT на VPS

Пошаговое руководство по развертыванию TeleGPT на виртуальном сервере.

## 📋 Требования

- **VPS**: Ubuntu 20.04/22.04 LTS
- **RAM**: 1-2 GB
- **CPU**: 1-2 ядра  
- **Диск**: 20-40 GB SSD
- **Root доступ** к серверу

## 🚀 Автоматическая установка

### 1. Подключение к VPS
```bash
ssh root@ваш-ip-адрес
```

### 2. Загрузка и запуск скрипта установки
```bash
wget https://raw.githubusercontent.com/ваш-username/bibi/main/setup_vps.sh
chmod +x setup_vps.sh
sudo bash setup_vps.sh
```

### 3. Развертывание проекта
```bash
# Переключение на пользователя telegpt
sudo su - telegpt

# Клонирование проекта
git clone https://github.com/ваш-username/bibi.git
cd bibi

# Настройка переменных окружения
cp env.example .env
nano .env  # Добавьте ваши API ключи

# Запуск развертывания
bash deploy.sh
```

## ⚙️ Ручная установка

### 1. Установка зависимостей
```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Установка Git
sudo apt install git -y
```

### 2. Создание пользователя
```bash
sudo useradd -m -s /bin/bash telegpt
sudo usermod -aG docker telegpt
```

### 3. Клонирование и настройка
```bash
sudo su - telegpt
git clone https://github.com/ваш-username/bibi.git
cd bibi
cp env.example .env
nano .env
```

### 4. Запуск проекта
```bash
bash deploy.sh
```

## 🔧 Настройка автозапуска

### Создание systemd сервиса
```bash
sudo nano /etc/systemd/system/telegpt.service
```

Содержимое файла:
```ini
[Unit]
Description=TeleGPT Telegram Bot
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
User=telegpt
WorkingDirectory=/home/telegpt/bibi
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

### Активация сервиса
```bash
sudo systemctl daemon-reload
sudo systemctl enable telegpt
sudo systemctl start telegpt
```

## 📊 Мониторинг и обслуживание

### Настройка автоматической проверки здоровья
```bash
# Добавление в crontab
crontab -e

# Добавить строку (проверка каждые 5 минут):
*/5 * * * * /home/telegpt/bibi/health_check.sh
```

### Настройка резервного копирования
```bash
# Добавление в crontab (ежедневно в 2:00)
0 2 * * * /home/telegpt/bibi/backup.sh
```

## 🛠️ Полезные команды

### Управление контейнерами
```bash
# Просмотр статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f

# Перезапуск
docker-compose restart

# Остановка
docker-compose down

# Полная пересборка
docker-compose down && docker-compose up --build -d
```

### Обновление проекта
```bash
# Обновление кода и перезапуск
git pull origin main
bash deploy.sh
```

### Проверка работоспособности
```bash
# Проверка статуса сервиса
sudo systemctl status telegpt

# Проверка логов системы
journalctl -u telegpt -f

# Проверка использования ресурсов
docker stats
```

## 🔒 Безопасность

### Настройка firewall
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
```

### Регулярные обновления
```bash
# Настройка автообновлений
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure unattended-upgrades
```

## 🆘 Устранение проблем

### Проблемы с Docker
```bash
# Перезапуск Docker
sudo systemctl restart docker

# Очистка неиспользуемых ресурсов
docker system prune -a
```

### Проблемы с правами
```bash
# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
# Перелогиньтесь после этого
```

### Проблемы с местом на диске
```bash
# Проверка использования диска
df -h

# Очистка логов Docker
docker system prune -a --volumes

# Очистка старых бэкапов
find backups/ -mtime +30 -delete
```

## 📈 Мониторинг производительности

### Просмотр использования ресурсов
```bash
# Использование ресурсов контейнером
docker stats telegpt_bot

# Использование диска
du -sh data/ logs/ backups/

# Загрузка системы
htop
```

### Анализ логов
```bash
# Последние ошибки
grep -i error logs/telegpt.log | tail -20

# Статистика запросов
grep "HTTP Request" logs/telegpt.log | tail -50
```

## ✅ Проверочный список

- [ ] VPS настроен и обновлен
- [ ] Docker и Docker Compose установлены
- [ ] Пользователь telegpt создан
- [ ] Репозиторий склонирован
- [ ] .env файл настроен с API ключами
- [ ] Проект запущен через deploy.sh
- [ ] Systemd сервис настроен и активирован
- [ ] Cron задачи для мониторинга настроены
- [ ] Firewall настроен
- [ ] Резервное копирование настроено

## 🎉 Готово!

Ваш TeleGPT бот теперь работает на VPS в продакшене!

**Полезные ссылки:**
- Логи: `docker-compose logs -f`
- Статус: `docker-compose ps`
- Обновление: `bash deploy.sh`