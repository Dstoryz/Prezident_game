#!/bin/bash

# 🚀 Скрипт запуска проекта "Президент: Экономика и Власть"
# Автор: Система агентов
# Дата: $(date)

echo "🎮 Запуск проекта 'Президент: Экономика и Власть'"
echo "=================================================="
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка наличия Python и Node.js
check_dependencies() {
    print_status "Проверка зависимостей..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 не найден. Установите Python 3.9+"
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        print_error "Node.js не найден. Установите Node.js 16+"
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        print_error "npm не найден. Установите npm"
        exit 1
    fi
    
    print_success "Все зависимости найдены"
}

# Функция для остановки всех процессов
cleanup() {
    print_status "Остановка всех процессов..."
    pkill -f "manage.py runserver" 2>/dev/null
    pkill -f "react-scripts start" 2>/dev/null
    print_success "Процессы остановлены"
}

# Обработка сигналов для корректного завершения
trap cleanup SIGINT SIGTERM

# Основная функция запуска
main() {
    check_dependencies
    
    # Переходим в корневую директорию проекта
    cd "$(dirname "$0")"
    
    print_status "Запуск бэкенда (Django)..."
    
    # Проверяем, существует ли виртуальное окружение
    if [ ! -d "backend/venv" ]; then
        print_warning "Виртуальное окружение не найдено. Создаем..."
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        python manage.py migrate
        cd ..
    fi
    
    # Запускаем Django сервер в фоне
    cd backend
    source venv/bin/activate
    nohup python manage.py runserver 8000 > ../backend.log 2>&1 &
    DJANGO_PID=$!
    cd ..
    
    # Ждем запуска Django
    print_status "Ожидание запуска Django сервера..."
    sleep 5
    
    # Проверяем, что Django запустился
    if curl -s http://localhost:8000/admin/ > /dev/null; then
        print_success "Django сервер запущен на http://localhost:8000"
    else
        print_error "Django сервер не запустился"
        exit 1
    fi
    
    print_status "Запуск фронтенда (React)..."
    
    # Проверяем, установлены ли зависимости React
    if [ ! -d "frontend/node_modules" ]; then
        print_warning "Node.js зависимости не найдены. Устанавливаем..."
        cd frontend
        npm install
        cd ..
    fi
    
    # Запускаем React сервер в фоне
    cd frontend
    nohup npm start > ../frontend.log 2>&1 &
    REACT_PID=$!
    cd ..
    
    # Ждем запуска React
    print_status "Ожидание запуска React сервера..."
    sleep 10
    
    # Проверяем, что React запустился
    if curl -s http://localhost:3000 > /dev/null; then
        print_success "React сервер запущен на http://localhost:3000"
    else
        print_warning "React сервер может еще запускаться..."
    fi
    
    echo ""
    echo "🎉 Проект успешно запущен!"
    echo ""
    echo "📱 Фронтенд: http://localhost:3000"
    echo "🔧 Бэкенд API: http://localhost:8000"
    echo "👨‍💼 Админ панель: http://localhost:8000/admin"
    echo ""
    echo "📋 Логи:"
    echo "   Бэкенд: backend.log"
    echo "   Фронтенд: frontend.log"
    echo ""
    echo "🛑 Для остановки нажмите Ctrl+C"
    echo ""
    
    # Ждем завершения
    wait
}

# Функция для остановки проекта
stop_project() {
    print_status "Остановка проекта..."
    cleanup
    print_success "Проект остановлен"
}

# Обработка аргументов командной строки
case "$1" in
    "stop")
        stop_project
        ;;
    "restart")
        stop_project
        sleep 2
        main
        ;;
    "status")
        echo "Статус процессов:"
        echo "Django: $(pgrep -f 'manage.py runserver' || echo 'Не запущен')"
        echo "React: $(pgrep -f 'react-scripts start' || echo 'Не запущен')"
        ;;
    "logs")
        echo "Логи бэкенда:"
        tail -f backend.log &
        echo "Логи фронтенда:"
        tail -f frontend.log &
        wait
        ;;
    *)
        main
        ;;
esac 