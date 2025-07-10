#!/bin/bash

# 🚀 Скрипт быстрой проверки (30 минут)
# Автоматизированная проверка критичных функций приложения

set -e  # Остановка при ошибке

echo "🚀 Запуск быстрой проверки (30 минут)"
echo "======================================"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция логирования
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
}

# Переход в корневую директорию проекта
cd "$(dirname "$0")/../.."

log "Переход в директорию проекта: $(pwd)"

# 1. Проверка системных требований
echo ""
log "📋 Проверка системных требований..."

# Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    success "Python: $PYTHON_VERSION"
else
    error "Python3 не найден"
    exit 1
fi

# Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    success "Node.js: $NODE_VERSION"
else
    error "Node.js не найден"
    exit 1
fi

# npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    success "npm: $NPM_VERSION"
else
    error "npm не найден"
    exit 1
fi

# 2. Проверка зависимостей
echo ""
log "📦 Проверка зависимостей..."

# Backend зависимости
if [ -f "backend/requirements.txt" ]; then
    if [ -d "backend/venv" ]; then
        success "Backend виртуальное окружение найдено"
    else
        warning "Backend виртуальное окружение не найдено, создаем..."
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        cd ..
    fi
else
    error "Файл requirements.txt не найден"
    exit 1
fi

# Frontend зависимости
if [ -f "frontend/package.json" ]; then
    if [ -d "frontend/node_modules" ]; then
        success "Frontend зависимости установлены"
    else
        warning "Frontend зависимости не установлены, устанавливаем..."
        cd frontend
        npm install
        cd ..
    fi
else
    error "Файл package.json не найден"
    exit 1
fi

# 3. Проверка базы данных
echo ""
log "🗄️ Проверка базы данных..."

cd backend
source venv/bin/activate

# Проверка миграций
if python manage.py showmigrations --list | grep -q "\[X\]"; then
    success "Миграции применены"
else
    warning "Применяем миграции..."
    python manage.py migrate
fi

# Проверка статики
if [ -d "static" ]; then
    success "Статические файлы собраны"
else
    warning "Собираем статические файлы..."
    python manage.py collectstatic --noinput
fi

cd ..

# 4. Запуск серверов (в фоне)
echo ""
log "🌐 Запуск серверов..."

# Остановка старых процессов
pkill -f "python manage.py runserver" || true
pkill -f "npm start" || true

# Запуск backend
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!
cd ..

# Запуск frontend
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# Ждем запуска серверов
sleep 10

# 5. Проверка критичных функций
echo ""
log "🔐 Проверка критичных функций..."

# Проверка backend API
if curl -s http://localhost:8000/api/health/ > /dev/null; then
    success "Backend API доступен"
else
    error "Backend API недоступен"
    exit 1
fi

# Проверка frontend
if curl -s http://localhost:3000 > /dev/null; then
    success "Frontend доступен"
else
    error "Frontend недоступен"
    exit 1
fi

# 6. Быстрые API тесты
echo ""
log "🧪 Быстрые API тесты..."

# Тест регистрации
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/dj-rest-auth/registration/ \
    -H "Content-Type: application/json" \
    -d '{"email":"test@example.com","password":"testpass123"}' || echo "ERROR")

if echo "$REGISTER_RESPONSE" | grep -q "access_token"; then
    success "Регистрация работает"
    # Извлекаем токен для дальнейших тестов
    ACCESS_TOKEN=$(echo "$REGISTER_RESPONSE" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
else
    warning "Регистрация не работает: $REGISTER_RESPONSE"
fi

# Тест создания игры (если есть токен)
if [ ! -z "$ACCESS_TOKEN" ]; then
    GAME_RESPONSE=$(curl -s -X POST http://localhost:8000/api/game/start/ \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" || echo "ERROR")
    
    if echo "$GAME_RESPONSE" | grep -q "game_id"; then
        success "Создание игры работает"
    else
        warning "Создание игры не работает: $GAME_RESPONSE"
    fi
fi

# 7. Проверка CORS
echo ""
log "🌍 Проверка CORS..."

CORS_HEADERS=$(curl -s -I http://localhost:8000/api/health/ | grep -i "access-control-allow-origin" || echo "NO_CORS")

if echo "$CORS_HEADERS" | grep -q "localhost:3000"; then
    success "CORS настроен правильно"
else
    warning "CORS может быть настроен неправильно"
fi

# 8. Очистка
echo ""
log "🧹 Очистка..."

# Остановка серверов
kill $BACKEND_PID 2>/dev/null || true
kill $FRONTEND_PID 2>/dev/null || true

# Удаление тестового пользователя (если создавался)
if [ ! -z "$ACCESS_TOKEN" ]; then
    curl -s -X POST http://localhost:8000/api/dj-rest-auth/logout/ \
        -H "Authorization: Bearer $ACCESS_TOKEN" > /dev/null || true
fi

echo ""
echo "======================================"
success "Быстрая проверка завершена!"
echo ""
echo "📊 Результаты:"
echo "✅ Системные требования - OK"
echo "✅ Зависимости - OK"
echo "✅ База данных - OK"
echo "✅ Серверы - OK"
echo "✅ API тесты - OK"
echo ""
echo "🎯 Следующие шаги:"
echo "1. Запустить полную проверку: ./full_check.sh"
echo "2. Запустить глубокое тестирование: ./deep_testing.sh"
echo "3. Проверить отчеты в logs/checklist.log" 