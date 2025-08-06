#!/bin/bash

# Скрипт автоматической настройки VPS для TeleGPT
# Запустите с правами root: sudo bash setup_vps.sh

set -e

echo "🚀 Настройка VPS для TeleGPT"

# Обновление системы
echo "📦 Обновление системы..."
apt update && apt upgrade -y

# Установка Docker
echo "🐳 Установка Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
else
    echo "✅ Docker уже установлен"
fi

# Установка Docker Compose
echo "🐳 Установка Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo "✅ Docker Compose уже установлен"
fi

# Установка Git
echo "📦 Установка Git..."
if ! command -v git &> /dev/null; then
    apt install git -y
else
    echo "✅ Git уже установлен"
fi

# Создание пользователя для приложения
echo "👤 Создание пользователя telegpt..."
if ! id "telegpt" &>/dev/null; then
    useradd -m -s /bin/bash telegpt
    usermod -aG docker telegpt
    echo "✅ Пользователь telegpt создан"
else
    echo "✅ Пользователь telegpt уже существует"
    usermod -aG docker telegpt
fi

# Настройка firewall
echo "🔥 Настройка firewall..."
if command -v ufw &> /dev/null; then
    ufw --force enable
    ufw allow ssh
    ufw allow 80
    ufw allow 443
    echo "✅ Firewall настроен"
fi

# Установка автообновлений
echo "🔄 Настройка автообновлений..."
apt install unattended-upgrades -y
echo 'Unattended-Upgrade::Automatic-Reboot "false";' >> /etc/apt/apt.conf.d/50unattended-upgrades

# Создание systemd сервиса
echo "⚙️ Создание systemd сервиса..."
cat > /etc/systemd/system/telegpt.service << 'EOF'
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
EOF

systemctl daemon-reload
systemctl enable telegpt

echo ""
echo "✅ Настройка VPS завершена!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Переключитесь на пользователя telegpt: sudo su - telegpt"
echo "2. Клонируйте репозиторий: git clone https://github.com/ваш-username/bibi.git"
echo "3. Перейдите в папку: cd bibi"
echo "4. Настройте .env файл: cp env.example .env && nano .env"
echo "5. Запустите деплой: bash deploy.sh"
echo "6. Добавьте healthcheck в crontab: crontab -e"
echo "   */5 * * * * /home/telegpt/bibi/health_check.sh"
echo ""
echo "🎉 Готово!"