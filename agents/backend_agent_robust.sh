#!/bin/bash

# УСТОЙЧИВЫЙ БЭКЕНД-АГЕНТ
# Автоматически запускает Django сервер и выполняет задачи из TODO листа

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Настройки
PROJECT_DIR="/home/alex/Downloads/Prezident_project"
BACKEND_DIR="$PROJECT_DIR/backend"
LOG_DIR="$PROJECT_DIR/agents/logs"
TODO_FILE="$PROJECT_DIR/TODO_CHECKLIST_AGENT_FRIENDLY.md"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/backend_${TIMESTAMP}.log"

# Создаем директорию для логов
mkdir -p "$LOG_DIR"

# Функция логирования
log() {
    echo -e "${BLUE}[$(date +"%H:%M:%S")] $1${NC}" | tee -a "$LOG_FILE"
}

# Функция чтения TODO листа
read_todo_tasks() {
    if [[ -f "$TODO_FILE" ]]; then
        # Ищем все невыполненные задачи только в секции BACKEND ЗАДАЧИ
        awk '/## 🚀 BACKEND ЗАДАЧИ/{flag=1;next}/^## /{flag=0}flag && /- \[ \]/' "$TODO_FILE"
    else
        echo "TODO файл не найден"
    fi
}

# Функция выполнения backend задач
execute_backend_tasks() {
    log "📝 Анализ TODO листа для backend задач..."
    
    if [[ ! -f "$TODO_FILE" ]]; then
        log "❌ TODO файл не найден: $TODO_FILE"
        return
    fi
    
    # Ищем незавершенные backend задачи
    local tasks_found=false
    
    # 1. Задачи по Python
    if grep -q "- [ ].*Python 3.9 установлен" "$TODO_FILE"; then
        log "🔄 Выполняю: Python 3.9 установлен"
        if python3 --version 2>/dev/null | grep -q "Python 3\.[9-9]\|Python 3\.[1-9][0-9]"; then
            sed -i 's/- [ ].*Python 3.9 установлен/- [x] Python 3.9 установлен/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: Python 3.9 установлен"
            tasks_found=true
        fi
    fi
    
    # 2. Задачи по виртуальному окружению
    if grep -q "- [ ].*Виртуальное окружение создано" "$TODO_FILE"; then
        log "🔄 Выполняю: Виртуальное окружение создано"
        if [[ -d "$PROJECT_DIR/.venv" ]]; then
            sed -i 's/- [ ].*Виртуальное окружение создано/- [x] Виртуальное окружение создано/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: Виртуальное окружение создано"
            tasks_found=true
        fi
    fi
    
    # 3. Задачи по зависимостям
    if grep -q "- [ ].*Зависимости установлены" "$TODO_FILE"; then
        log "🔄 Выполняю: Зависимости установлены"
        if [[ -f "$BACKEND_DIR/requirements.txt" ]]; then
            cd "$BACKEND_DIR" && source ../.venv/bin/activate && pip install -r requirements.txt --quiet
            if [[ $? -eq 0 ]]; then
                sed -i 's/- [ ].*Зависимости установлены/- [x] Зависимости установлены/' "$TODO_FILE"
                log "✅ Отмечено как выполненное: Зависимости установлены"
                tasks_found=true
            fi
        fi
    fi
    
    # 4. Задачи по проверке зависимостей
    if grep -q "- [ ].*Проверка зависимостей прошла" "$TODO_FILE"; then
        log "🔄 Выполняю: Проверка зависимостей прошла"
        cd "$BACKEND_DIR" && source ../.venv/bin/activate && python manage.py check
        if [[ $? -eq 0 ]]; then
            sed -i 's/- [ ].*Проверка зависимостей прошла/- [x] Проверка зависимостей прошла/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: Проверка зависимостей прошла"
            tasks_found=true
        fi
    fi
    
    # 5. Задачи по запуску backend
    if grep -q "- [ ].*Backend запускается на порту 8000" "$TODO_FILE"; then
        log "🔄 Выполняю: Backend запускается на порту 8000"
        if curl -s http://localhost:8000/api/game/status/ > /dev/null 2>&1; then
            sed -i 's/- [ ].*Backend запускается на порту 8000/- [x] Backend запускается на порту 8000/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: Backend запускается на порту 8000"
            tasks_found=true
        else
            log "🔄 Запускаю Django сервер..."
            start_django_server
            if curl -s http://localhost:8000/api/game/status/ > /dev/null 2>&1; then
                sed -i 's/- [ ].*Backend запускается на порту 8000/- [x] Backend запускается на порту 8000/' "$TODO_FILE"
                log "✅ Отмечено как выполненное: Backend запускается на порту 8000"
                tasks_found=true
            fi
        fi
    fi
    
    # 6. Задачи по миграциям
    if grep -q "- [ ].*Миграции применены" "$TODO_FILE"; then
        log "🔄 Выполняю: Миграции применены"
        cd "$BACKEND_DIR" && source ../.venv/bin/activate && python manage.py migrate --verbosity=0
        if [[ $? -eq 0 ]]; then
            sed -i 's/- [ ].*Миграции применены/- [x] Миграции применены/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: Миграции применены"
            tasks_found=true
        fi
    fi
    
    # 7. Задачи по API
    if grep -q "- [ ].*API доступен" "$TODO_FILE"; then
        log "🔄 Выполняю: API доступен"
        if curl -s http://localhost:8000/api/game/status/ > /dev/null 2>&1; then
            sed -i 's/- [ ].*API доступен/- [x] API доступен/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: API доступен"
            tasks_found=true
        fi
    fi
    
    # 8. Задачи по суперпользователю
    if grep -q "- [ ].*Суперпользователь создан" "$TODO_FILE"; then
        log "🔄 Выполняю: Суперпользователь создан"
        cd "$BACKEND_DIR" && source ../.venv/bin/activate && python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Суперпользователь создан')
else:
    print('Суперпользователь уже существует')
" --verbosity=0
        if [[ $? -eq 0 ]]; then
            sed -i 's/- [ ].*Суперпользователь создан/- [x] Суперпользователь создан/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: Суперпользователь создан"
            tasks_found=true
        fi
    fi
    
    # 9. Задачи по статическим файлам
    if grep -q "- [ ].*Статические файлы собраны" "$TODO_FILE"; then
        log "🔄 Выполняю: Статические файлы собраны"
        cd "$BACKEND_DIR" && source ../.venv/bin/activate && python manage.py collectstatic --noinput --verbosity=0
        if [[ $? -eq 0 ]]; then
            sed -i 's/- [ ].*Статические файлы собраны/- [x] Статические файлы собраны/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: Статические файлы собраны"
            tasks_found=true
        fi
    fi
    
    # 10. Задачи по тестам
    if grep -q "- [ ].*Тесты проходят" "$TODO_FILE"; then
        log "🔄 Выполняю: Тесты проходят"
        cd "$BACKEND_DIR" && source ../.venv/bin/activate && python manage.py test game --verbosity=0
        if [[ $? -eq 0 ]]; then
            sed -i 's/- [ ].*Тесты проходят/- [x] Тесты проходят/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: Тесты проходят"
            tasks_found=true
        fi
    fi
    
    if [[ "$tasks_found" == "false" ]]; then
        log "ℹ️ Нет незавершенных backend задач для выполнения"
    else
        log "✅ Backend задачи выполнены и отмечены в TODO листе"
    fi
}

# Функция запуска Django сервера
start_django_server() {
    log "🔍 Проверка Django сервера..."
    
    # Проверяем, запущен ли сервер
    if curl -s http://localhost:8000/api/game/status/ > /dev/null 2>&1; then
        log "✅ Django сервер уже запущен"
        return 0
    fi
    
    log "⚠️  Django сервер не запущен, стартую..."
    
    # Запускаем Django сервер в фоне
    cd "$BACKEND_DIR"
    source ../.venv/bin/activate
    
    # Убиваем старые процессы Django
    pkill -f "manage.py runserver" 2>/dev/null
    
    # Запускаем новый сервер
    nohup python manage.py runserver 0.0.0.0:8000 > /dev/null 2>&1 &
    DJANGO_PID=$!
    
    # Ждем запуска сервера
    for i in {1..30}; do
        if curl -s http://localhost:8000/api/game/status/ > /dev/null 2>&1; then
            log "✅ Django сервер запущен (PID: $DJANGO_PID)"
            return 0
        fi
        sleep 1
    done
    
    log "❌ Не удалось запустить Django сервер"
    return 1
}

# Функция проверки API
test_api() {
    log "🔄 Проверка api/game/status/ (таймаут: 5с)..."
    if timeout 5 curl -s http://localhost:8000/api/game/status/ > /dev/null 2>&1; then
        log "✅ Проверка api/game/status/ завершено успешно"
    else
        log "⚠️  API недоступен"
    fi
    
    log "🔄 Проверка api/game/economic-data/ (таймаут: 5с)..."
    if timeout 5 curl -s http://localhost:8000/api/game/economic-data/ > /dev/null 2>&1; then
        log "✅ Проверка api/game/economic-data/ завершено успешно"
    else
        log "⚠️  Economic API недоступен"
    fi
}

# Основной цикл
main_loop() {
    log "🔧 Устойчивый бэкенд-агент запущен"
    log "📁 Backend: $BACKEND_DIR"
    log "📝 Логи: $LOG_FILE"
    
    # Проверяем Django проект
    log "🔍 Проверка Django проекта..."
    if [[ -f "$BACKEND_DIR/manage.py" ]]; then
        log "✅ Django проект найден"
    else
        log "❌ Django проект не найден"
        exit 1
    fi
    
    # Проверяем настройки Django
    log "🔄 Проверка настроек Django (таймаут: 15с)..."
    if timeout 15 bash -c "cd $BACKEND_DIR && source ../.venv/bin/activate && python manage.py check" > /dev/null 2>&1; then
        log "✅ Проверка настроек Django завершено успешно"
    else
        log "⚠️  Проблемы с настройками Django"
    fi
    
    # Проверяем миграции
    log "🔄 Проверка миграций (таймаут: 30с)..."
    if timeout 30 bash -c "cd $BACKEND_DIR && source ../.venv/bin/activate && python manage.py showmigrations" > /dev/null 2>&1; then
        log "✅ Проверка миграций завершено успешно"
    else
        log "⚠️  Проблемы с миграциями"
    fi
    
    # Применяем миграции
    log "🔄 Применение миграций (таймаут: 60с)..."
    if timeout 60 bash -c "cd $BACKEND_DIR && source ../.venv/bin/activate && python manage.py migrate" > /dev/null 2>&1; then
        log "✅ Применение миграций завершено успешно"
    else
        log "⚠️  Проблемы с применением миграций"
    fi
    
    # Основной цикл мониторинга
    log "🔄 Цикл мониторинга бэкенда..."
    
    while true; do
        # Выполняем backend задачи
        execute_backend_tasks
        
        # Запускаем Django сервер
        start_django_server
        
        # Тестируем API
        test_api
        
        # Проверка производительности
        log "⚡ Проверка производительности..."
        
        # Проверяем использование памяти Django
        DJANGO_PROCESSES=$(ps aux | grep "manage.py runserver" | grep -v grep | wc -l)
        if [[ $DJANGO_PROCESSES -gt 0 ]]; then
            log "✅ Django процессы: $DJANGO_PROCESSES"
        else
            log "⚠️  Django процессы не найдены"
        fi
        
        # Проверяем логи Django
        if [[ -f "$BACKEND_DIR/django.log" ]]; then
            log "📝 Последние ошибки Django:"
            tail -n 3 "$BACKEND_DIR/django.log" 2>/dev/null | while IFS= read -r line; do
                log "  $line"
            done
        fi
        
        log "✅ Цикл завершен, ожидание 10 секунд..."
        sleep 10
    done
}

# Обработка сигналов
trap 'log "🛑 Получен сигнал остановки"; exit 0' SIGINT SIGTERM

# Запуск основного цикла
main_loop 