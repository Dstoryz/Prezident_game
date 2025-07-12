#!/bin/bash

# Скрипт развертывания для проекта "Президент: Экономика и Власть"

set -e  # Остановка при ошибке

echo "🚀 Начинаем развертывание проекта..."

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker и попробуйте снова."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose и попробуйте снова."
    exit 1
fi

# Создание .env файла если его нет
if [ ! -f .env ]; then
    echo "📝 Создаем .env файл..."
    cat > .env << EOF
# Настройки базы данных
POSTGRES_DB=prezident_game
POSTGRES_USER=game_user
POSTGRES_PASSWORD=game_password

# Настройки Django
DEBUG=False
SECRET_KEY=$(openssl rand -hex 32)
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Настройки приложения
DATABASE_URL=postgresql://game_user:game_password@db:5432/prezident_game
EOF
    echo "✅ .env файл создан"
fi

# Остановка существующих контейнеров
echo "🛑 Останавливаем существующие контейнеры..."
docker-compose down

# Удаление старых образов (опционально)
if [ "$1" = "--clean" ]; then
    echo "🧹 Удаляем старые образы..."
    docker-compose down --rmi all --volumes --remove-orphans
fi

# Сборка и запуск контейнеров
echo "🔨 Собираем и запускаем контейнеры..."
docker-compose up --build -d

# Ожидание готовности базы данных
echo "⏳ Ожидаем готовности базы данных..."
sleep 10

# Проверка статуса контейнеров
echo "📊 Проверяем статус контейнеров..."
docker-compose ps

# Создание суперпользователя (если нужно)
echo "👤 Создание суперпользователя..."
docker-compose exec backend python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Суперпользователь создан: admin/admin123')
else:
    print('ℹ️ Суперпользователь уже существует')
"

# Проверка доступности сервисов
echo "🔍 Проверяем доступность сервисов..."

# Проверка backend
if curl -f http://localhost:8000/api/health/ > /dev/null 2>&1; then
    echo "✅ Backend API доступен на http://localhost:8000"
else
    echo "⚠️ Backend API недоступен, проверьте логи: docker-compose logs backend"
fi

# Проверка frontend
if curl -f http://localhost:80 > /dev/null 2>&1; then
    echo "✅ Frontend доступен на http://localhost:80"
else
    echo "⚠️ Frontend недоступен, проверьте логи: docker-compose logs frontend"
fi

# Проверка nginx
if curl -f http://localhost:8080 > /dev/null 2>&1; then
    echo "✅ Nginx доступен на http://localhost:8080"
else
    echo "⚠️ Nginx недоступен, проверьте логи: docker-compose logs nginx"
fi

echo ""
echo "🎉 Развертывание завершено!"
echo ""
echo "📋 Доступные сервисы:"
echo "   🌐 Frontend: http://localhost:80"
echo "   🔧 Backend API: http://localhost:8000"
echo "   🌍 Nginx Proxy: http://localhost:8080"
echo "   🗄️ База данных: localhost:5432"
echo ""
echo "👤 Администратор: admin/admin123"
echo ""
echo "📝 Полезные команды:"
echo "   docker-compose logs -f [service]  # Просмотр логов"
echo "   docker-compose down               # Остановка сервисов"
echo "   docker-compose restart [service]  # Перезапуск сервиса"
echo "   docker-compose exec backend python manage.py shell  # Django shell"
echo "" 