#!/bin/bash

# Скрипт резервного копирования для проекта "Президент: Экономика и Власть"

set -e

# Настройки
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="prezident_game"
DB_USER="game_user"
DB_HOST="localhost"
DB_PORT="5432"

# Создание директории для бэкапов
mkdir -p $BACKUP_DIR

echo "🔄 Начинаем резервное копирование..."

# Резервное копирование базы данных
echo "🗄️ Создаем бэкап базы данных..."
docker-compose exec -T db pg_dump -U $DB_USER -h $DB_HOST -p $DB_PORT $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Сжатие бэкапа БД
gzip $BACKUP_DIR/db_backup_$DATE.sql

# Резервное копирование файлов приложения
echo "📁 Создаем бэкап файлов приложения..."
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='logs' \
    --exclude='backups' \
    .

# Резервное копирование логов
echo "📝 Создаем бэкап логов..."
tar -czf $BACKUP_DIR/logs_backup_$DATE.tar.gz logs/

# Создание метаданных бэкапа
cat > $BACKUP_DIR/backup_meta_$DATE.json << EOF
{
  "timestamp": "$(date -Iseconds)",
  "backup_type": "full",
  "files": {
    "database": "db_backup_$DATE.sql.gz",
    "application": "app_backup_$DATE.tar.gz",
    "logs": "logs_backup_$DATE.tar.gz"
  },
  "size": {
    "database": "$(du -h $BACKUP_DIR/db_backup_$DATE.sql.gz | cut -f1)",
    "application": "$(du -h $BACKUP_DIR/app_backup_$DATE.tar.gz | cut -f1)",
    "logs": "$(du -h $BACKUP_DIR/logs_backup_$DATE.tar.gz | cut -f1)"
  }
}
EOF

# Удаление старых бэкапов (оставляем последние 7 дней)
echo "🧹 Удаляем старые бэкапы..."
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
find $BACKUP_DIR -name "backup_meta_*.json" -mtime +7 -delete

echo "✅ Резервное копирование завершено!"
echo "📊 Статистика:"
echo "   🗄️ База данных: $BACKUP_DIR/db_backup_$DATE.sql.gz"
echo "   📁 Приложение: $BACKUP_DIR/app_backup_$DATE.tar.gz"
echo "   📝 Логи: $BACKUP_DIR/logs_backup_$DATE.tar.gz"
echo "   📋 Метаданные: $BACKUP_DIR/backup_meta_$DATE.json"

# Проверка целостности бэкапа БД
echo "🔍 Проверяем целостность бэкапа БД..."
gunzip -t $BACKUP_DIR/db_backup_$DATE.sql.gz
if [ $? -eq 0 ]; then
    echo "✅ Бэкап БД корректен"
else
    echo "❌ Ошибка в бэкапе БД"
    exit 1
fi 