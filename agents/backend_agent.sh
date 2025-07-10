#!/bin/bash

# 🔧 БЭКЕНД-АГЕНТ
# Разработчик серверной части проекта "Президент: Экономика и Власть"

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Переменные
PROJECT_ROOT="/home/alex/Downloads/Prezident_project"
BACKEND_DIR="$PROJECT_ROOT/backend"
LOG_FILE="$PROJECT_ROOT/agents/logs/backend_$(date '+%Y%m%d_%H%M%S').log"

# Функция логирования
log() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

# Функция безопасного выполнения команд
safe_execute() {
    local timeout=$1
    local command="$2"
    local description="$3"
    
    log "🔄 $description (таймаут: ${timeout}с)..."
    
    if timeout $timeout bash -c "$command" 2>&1 | tee -a "$LOG_FILE"; then
        log "✅ $description завершено успешно"
        return 0
    else
        local exit_code=$?
        if [ $exit_code -eq 124 ]; then
            log "⏰ $description зависло, прерываю выполнение"
        else
            log "❌ $description завершилось с ошибкой (код: $exit_code)"
        fi
        return $exit_code
    fi
}

# Функция проверки Django проекта
check_django_project() {
    log "🔍 Проверка Django проекта..."
    
    if [ ! -f "$BACKEND_DIR/manage.py" ]; then
        log "❌ Django проект не найден"
        return 1
    fi
    
    log "✅ Django проект найден"
    
    # Проверка настроек
    safe_execute 15 "cd $BACKEND_DIR && python manage.py check" "Проверка настроек Django"
    
    # Проверка миграций
    safe_execute 30 "cd $BACKEND_DIR && python manage.py showmigrations" "Проверка миграций"
    
    # Применение миграций если нужно
    safe_execute 60 "cd $BACKEND_DIR && python manage.py migrate" "Применение миграций"
}

# Функция проверки базы данных
check_database() {
    log "🗄️  Проверка базы данных..."
    
    # Проверка подключения к БД
    safe_execute 15 "cd $BACKEND_DIR && python manage.py shell -c 'from django.db import connection; print(\"Активные соединения:\", len(connection.queries))'" "Проверка подключения к БД"
    
    # Проверка моделей
    safe_execute 15 "cd $BACKEND_DIR && python manage.py shell -c 'from game.models import *; print(\"Модели загружены успешно\")'" "Проверка моделей"
    
    # Проверка данных
    safe_execute 15 "cd $BACKEND_DIR && python manage.py shell -c 'from game.models import GameSession; print(\"Игровых сессий:\", GameSession.objects.count())'" "Проверка данных"
}

# Функция проверки кэширования
check_caching() {
    log "⚡ Проверка кэширования..."
    
    # Тест кэша
    safe_execute 15 "cd $BACKEND_DIR && python manage.py shell -c 'from django.core.cache import cache; cache.set(\"test\", \"value\", 60); print(\"Кэш работает:\", cache.get(\"test\"))'" "Тест кэширования"
    
    # Проверка Redis (если используется)
    if command -v redis-cli >/dev/null 2>&1; then
        safe_execute 5 "redis-cli ping" "Проверка Redis"
    else
        log "⚠️  Redis не установлен"
    fi
}

# Функция проверки памяти Django
check_django_memory() {
    log "🧠 Проверка памяти Django..."
    
    # Проверка использования памяти
    safe_execute 15 "ps aux | grep 'python.*manage.py' | grep -v grep" "Проверка процессов Django"
    
    # Проверка настроек памяти
    safe_execute 15 "cd $BACKEND_DIR && python manage.py shell -c 'import gc; print(\"Объектов в памяти:\", len(gc.get_objects()))'" "Проверка объектов в памяти"
}

# Функция проверки API endpoints
check_api_endpoints() {
    log "🌐 Проверка API endpoints..."
    
    # Список основных endpoints
    local endpoints=(
        "api/auth/register/"
        "api/auth/login/"
        "api/game/start/"
        "api/game/status/"
        "api/game/economic-data/"
    )
    
    for endpoint in "${endpoints[@]}"; do
        safe_execute 5 "curl --max-time 5 -s -o /dev/null -w '%{http_code}' http://localhost:8000/$endpoint" "Проверка $endpoint"
    done
}

# Функция проверки экономической модели
check_economic_model() {
    log "📊 Проверка экономической модели..."
    
    # Проверка файла модели
    local model_file="$BACKEND_DIR/game/services/enhanced_economic_model.py"
    if [ ! -f "$model_file" ]; then
        log "❌ EnhancedEconomicModel не найден"
        return 1
    fi
    
    log "✅ EnhancedEconomicModel найден"
    
    # Тестирование импорта
    safe_execute 15 "cd $BACKEND_DIR && python -c 'from game.services.enhanced_economic_model import EnhancedEconomicModel; print(\"Модель импортирована успешно\")'" "Тестирование импорта модели"
    
    # Тестирование инициализации
    safe_execute 30 "cd $BACKEND_DIR && python -c 'from game.services.enhanced_economic_model import EnhancedEconomicModel; model = EnhancedEconomicModel(); print(\"Модель инициализирована\")'" "Тестирование инициализации модели"
    
    # Проверка конфигурации
    if [ -f "$BACKEND_DIR/game/config/economic_config.py" ]; then
        safe_execute 15 "cd $BACKEND_DIR && python -c 'from game.config.economic_config import ECONOMIC_PARAMS; print(\"Конфигурация загружена:\", len(ECONOMIC_PARAMS), \"параметров\")'" "Проверка конфигурации"
    fi
}

# Функция проверки сервисов
check_services() {
    log "🔧 Проверка сервисов..."
    
    # Проверка сервисов игры
    local services=(
        "game_engine.py"
        "event_generator.py"
        "solow_model.py"
    )
    
    for service in "${services[@]}"; do
        local service_file="$BACKEND_DIR/game/services/$service"
        if [ -f "$service_file" ]; then
            log "✅ Сервис $service найден"
            safe_execute 15 "cd $BACKEND_DIR && python -c 'from game.services.${service%.*} import *; print(\"Сервис $service импортирован\")'" "Проверка сервиса $service"
        else
            log "⚠️  Сервис $service не найден"
        fi
    done
}

# Функция проверки сериализаторов
check_serializers() {
    log "📝 Проверка сериализаторов..."
    
    # Проверка сериализаторов
    safe_execute 15 "cd $BACKEND_DIR && python manage.py shell -c 'from game.serializers import *; print(\"Сериализаторы загружены\")'" "Проверка сериализаторов"
    
    # Тестирование сериализации
    safe_execute 30 "cd $BACKEND_DIR && python manage.py shell -c 'from game.models import GameSession; from game.serializers import GameSessionSerializer; session = GameSession.objects.first(); print(\"Сериализация:\", GameSessionSerializer(session).data if session else \"Нет данных\")'" "Тестирование сериализации"
}

# Функция проверки views
check_views() {
    log "👁️  Проверка views..."
    
    # Проверка views
    safe_execute 15 "cd $BACKEND_DIR && python manage.py shell -c 'from game.views import *; print(\"Views загружены\")'" "Проверка views"
    
    # Проверка URL patterns
    safe_execute 15 "cd $BACKEND_DIR && python manage.py shell -c 'from django.urls import get_resolver; print(\"URL patterns загружены:\", len(get_resolver().url_patterns))'" "Проверка URL patterns"
}

# Функция проверки аутентификации
check_authentication() {
    log "🔐 Проверка аутентификации..."
    
    # Проверка пользователей
    safe_execute 15 "cd $BACKEND_DIR && python manage.py shell -c 'from django.contrib.auth.models import User; print(\"Пользователей в системе:\", User.objects.count())'" "Проверка пользователей"
    
    # Проверка сессий
    safe_execute 15 "cd $BACKEND_DIR && python manage.py shell -c 'from django.contrib.sessions.models import Session; print(\"Активных сессий:\", Session.objects.count())'" "Проверка сессий"
}

# Функция проверки производительности
check_performance() {
    log "⚡ Проверка производительности..."
    
    # Тест времени отклика
    local start_time=$(date +%s%N)
    curl --max-time 5 -s http://localhost:8000/api/auth/register/ >/dev/null
    local end_time=$(date +%s%N)
    local response_time=$(( (end_time - start_time) / 1000000 ))
    
    log "📊 Время отклика API: ${response_time}ms"
    
    if [ $response_time -gt 200 ]; then
        log "⚠️  Медленный отклик API (>200ms)"
    else
        log "✅ Отклик API в норме"
    fi
    
    # Проверка использования ресурсов
    safe_execute 15 "ps aux | grep 'python.*manage.py' | grep -v grep | awk '{print \$3, \$4}'" "Проверка использования CPU и памяти"
}

# Функция создания отчетов
generate_backend_report() {
    log "📈 Создание отчета о бэкенде..."
    
    cat > "$PROJECT_ROOT/agents/reports/backend_status_$(date '+%Y%m%d_%H%M').md" << EOF
# 🔧 ОТЧЕТ О БЭКЕНДЕ
# Бэкенд-агент | $(date)

## 🎯 ОБЩАЯ ИНФОРМАЦИЯ
- **Проект:** Президент: Экономика и Власть
- **Backend:** Django
- **Версия:** 2.0
- **Время отчета:** $(date)

## 🗄️  БАЗА ДАННЫХ
- **Статус:** $(cd $BACKEND_DIR && python manage.py shell -c 'from django.db import connection; print("OK" if connection.ensure_connection() else "ERROR")' 2>/dev/null || echo "Неизвестно")
- **Миграции:** $(cd $BACKEND_DIR && python manage.py showmigrations 2>/dev/null | grep -c "\[X\]" || echo "Неизвестно")
- **Игровых сессий:** $(cd $BACKEND_DIR && python manage.py shell -c 'from game.models import GameSession; print(GameSession.objects.count())' 2>/dev/null || echo "Неизвестно")

## 🌐 API ENDPOINTS
- **Статус:** $(curl --max-time 5 -s http://localhost:8000/api/auth/register/ >/dev/null && echo "Работает" || echo "Недоступен")
- **Время отклика:** $(curl --max-time 5 -s -w '%{time_total}' http://localhost:8000/api/auth/register/ 2>/dev/null | tail -n1 || echo "Неизвестно")s

## 📊 ЭКОНОМИЧЕСКАЯ МОДЕЛЬ
- **EnhancedEconomicModel:** $(if [ -f "$BACKEND_DIR/game/services/enhanced_economic_model.py" ]; then echo "Найдена"; else echo "Не найдена"; fi)
- **Конфигурация:** $(if [ -f "$BACKEND_DIR/game/config/economic_config.py" ]; then echo "Найдена"; else echo "Не найдена"; fi)

## 🔐 АУТЕНТИФИКАЦИЯ
- **Пользователей:** $(cd $BACKEND_DIR && python manage.py shell -c 'from django.contrib.auth.models import User; print(User.objects.count())' 2>/dev/null || echo "Неизвестно")
- **Активных сессий:** $(cd $BACKEND_DIR && python manage.py shell -c 'from django.contrib.sessions.models import Session; print(Session.objects.count())' 2>/dev/null || echo "Неизвестно")

## ⚡ ПРОИЗВОДИТЕЛЬНОСТЬ
- **CPU:** $(ps aux | grep 'python.*manage.py' | grep -v grep | awk '{print $3}' | head -1 || echo "Неизвестно")%
- **Память:** $(ps aux | grep 'python.*manage.py' | grep -v grep | awk '{print $4}' | head -1 || echo "Неизвестно")%

## 🚨 ПРОБЛЕМЫ
$(if [ -f "$BACKEND_DIR/logs/error.log" ]; then
    echo "- Django ошибок: $(tail -n 100 "$BACKEND_DIR/logs/error.log" | grep -c "ERROR" || echo "0")"
else
    echo "- Django логи не найдены"
fi)

## 📋 РЕКОМЕНДАЦИИ
1. Продолжить мониторинг производительности
2. Оптимизировать запросы к БД
3. Добавить кэширование
4. Улучшить обработку ошибок

---
*Отчет создан автоматически бэкенд-агентом*
EOF

    log "✅ Отчет о бэкенде создан"
}

# Основной цикл работы
main() {
    log "🔧 Бэкенд-агент запущен"
    log "📁 Backend: $BACKEND_DIR"
    log "📝 Логи: $LOG_FILE"
    
    # Создание необходимых директорий
    mkdir -p "$PROJECT_ROOT/agents/reports"
    
    # Проверка Django проекта
    check_django_project
    
    # Проверка базы данных
    check_database
    
    # Проверка кэширования
    check_caching
    
    # Проверка памяти Django
    check_django_memory
    
    # Проверка API endpoints
    check_api_endpoints
    
    # Проверка экономической модели
    check_economic_model
    
    # Проверка сервисов
    check_services
    
    # Проверка сериализаторов
    check_serializers
    
    # Проверка views
    check_views
    
    # Проверка аутентификации
    check_authentication
    
    # Основной цикл мониторинга
    while true; do
        log "🔄 Цикл мониторинга бэкенда..."
        
        # Периодические проверки
        check_database
        check_api_endpoints
        check_performance
        
        # Создание отчетов каждые 30 минут
        local current_minute=$(date '+%M')
        if [ $((10#$current_minute % 30)) -eq 0 ]; then
            generate_backend_report
        fi
        
        log "✅ Цикл завершен, ожидание 60 секунд..."
        sleep 60
    done
}

# Запуск с обработкой сигналов
trap 'log "🛑 Бэкенд-агент остановлен"; exit 0' SIGINT SIGTERM

# Запуск основной функции
main "$@" 