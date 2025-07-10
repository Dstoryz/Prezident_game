#!/bin/bash

# 🐛 ТЕСТИРОВЩИК-АГЕНТ
# Специалист по тестированию и контролю качества проекта "Президент: Экономика и Власть"

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
FRONTEND_DIR="$PROJECT_ROOT/frontend"
LOG_FILE="$PROJECT_ROOT/agents/logs/testing_$(date '+%Y%m%d_%H%M%S').log"

# Функция логирования
log() {
    echo -e "${YELLOW}[$(date '+%H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
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

# Функция тестирования экономической модели
test_economic_model() {
    log "📊 Тестирование экономической модели..."
    
    # Проверка файла модели
    local model_file="$BACKEND_DIR/game/services/enhanced_economic_model.py"
    if [ ! -f "$model_file" ]; then
        log "❌ EnhancedEconomicModel не найден"
        return 1
    fi
    
    log "✅ EnhancedEconomicModel найден"
    
    # Тестирование импорта
    safe_execute 15 "cd $BACKEND_DIR && python -c 'from game.services.enhanced_economic_model import EnhancedEconomicModel; print(\"Модель импортирована успешно\")'" "Тестирование импорта модели"
    
    # Запуск тестов модели
    if [ -f "$PROJECT_ROOT/test_enhanced_model.py" ]; then
        safe_execute 60 "cd $PROJECT_ROOT && python test_enhanced_model.py" "Запуск тестов экономической модели"
    else
        log "⚠️  Файл тестов модели не найден"
    fi
    
    # Тестирование конфигурации
    if [ -f "$BACKEND_DIR/game/config/economic_config.py" ]; then
        safe_execute 15 "cd $BACKEND_DIR && python -c 'from game.config.economic_config import ECONOMIC_PARAMS; print(\"Конфигурация загружена:\", len(ECONOMIC_PARAMS), \"параметров\")'" "Тестирование конфигурации"
    fi
}

# Функция тестирования Django API
test_django_api() {
    log "🌐 Тестирование Django API..."
    
    # Проверка Django проекта
    if [ ! -f "$BACKEND_DIR/manage.py" ]; then
        log "❌ Django проект не найден"
        return 1
    fi
    
    # Запуск Django тестов (быстрые тесты)
    safe_execute 90 "cd $BACKEND_DIR && python manage.py test auth_app --verbosity=0" "Тестирование auth_app"
    safe_execute 90 "cd $BACKEND_DIR && python manage.py test game --verbosity=0" "Тестирование game"
    
    # Тестирование API endpoints
    local endpoints=(
        "api/auth/register/"
        "api/auth/login/"
        "api/game/start/"
        "api/game/status/"
    )
    
    for endpoint in "${endpoints[@]}"; do
        safe_execute 5 "curl --max-time 5 -s -o /dev/null -w '%{http_code}' http://localhost:8000/$endpoint" "Тестирование $endpoint"
    done
    
    # Проверка миграций
    safe_execute 30 "cd $BACKEND_DIR && python manage.py showmigrations" "Проверка миграций"
}

# Функция тестирования React фронтенда
test_react_frontend() {
    log "🎨 Тестирование React фронтенда..."
    
    # Проверка React проекта
    if [ ! -f "$FRONTEND_DIR/package.json" ]; then
        log "❌ React проект не найден"
        return 1
    fi
    
    # Запуск React тестов (быстрые тесты)
    if [ -f "$FRONTEND_DIR/src/App.test.tsx" ]; then
        safe_execute 60 "cd $FRONTEND_DIR && npm test -- --watchAll=false --passWithNoTests --silent" "Запуск React тестов"
    else
        log "⚠️  React тесты не найдены"
    fi
    
    # Проверка линтера
    if grep -q "eslint" "$FRONTEND_DIR/package.json"; then
        safe_execute 30 "cd $FRONTEND_DIR && npm run lint" "Проверка ESLint"
    fi
    
    # Тестирование сборки (быстрая проверка)
    safe_execute 120 "cd $FRONTEND_DIR && npm run build" "Тестирование сборки"
}

# Функция интеграционного тестирования
test_integration() {
    log "🔗 Интеграционное тестирование..."
    
    # Тестирование связи фронтенд-бэкенд
    safe_execute 5 "curl --max-time 5 -s http://localhost:8000/api/auth/register/" "Тест Django API"
    safe_execute 5 "curl --max-time 5 -s http://localhost:3000" "Тест React Frontend"
    
    # Проверка CORS
    safe_execute 5 "curl --max-time 5 -s -H 'Origin: http://localhost:3000' http://localhost:8000/api/auth/register/" "Тест CORS"
    
    # Тестирование аутентификации
    safe_execute 15 "curl --max-time 10 -s -X POST -H 'Content-Type: application/json' -d '{\"username\":\"test\",\"password\":\"test123\"}' http://localhost:8000/api/auth/register/" "Тест регистрации"
}

# Функция тестирования производительности
test_performance() {
    log "⚡ Тестирование производительности..."
    
    # Тест времени отклика API
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
    
    # Тест загрузки фронтенда
    start_time=$(date +%s%N)
    curl --max-time 5 -s http://localhost:3000 >/dev/null
    end_time=$(date +%s%N)
    response_time=$(( (end_time - start_time) / 1000000 ))
    
    log "📊 Время загрузки фронтенда: ${response_time}ms"
    
    if [ $response_time -gt 3000 ]; then
        log "⚠️  Медленная загрузка фронтенда (>3s)"
    else
        log "✅ Загрузка фронтенда в норме"
    fi
    
    # Проверка использования памяти
    safe_execute 15 "ps aux | grep -E '(python|node)' | grep -v grep" "Проверка использования памяти"
}

# Функция поиска ошибок
find_errors() {
    log "🔍 Поиск ошибок в коде..."
    
    # Поиск ошибок в Python коде (быстрая проверка)
    if command -v pylint >/dev/null 2>&1; then
        safe_execute 60 "cd $BACKEND_DIR && find . -name '*.py' -exec pylint {} +" "Проверка Python кода (pylint)"
    fi
    
    # Поиск ошибок в JavaScript/TypeScript коде
    if [ -f "$FRONTEND_DIR/package.json" ] && grep -q "eslint" "$FRONTEND_DIR/package.json"; then
        safe_execute 30 "cd $FRONTEND_DIR && npm run lint" "Проверка JavaScript кода (ESLint)"
    fi
    
    # Поиск синтаксических ошибок
    safe_execute 30 "cd $BACKEND_DIR && python -m py_compile game/models.py" "Проверка синтаксиса models.py"
    safe_execute 30 "cd $BACKEND_DIR && python -m py_compile game/views.py" "Проверка синтаксиса views.py"
    
    # Проверка логов на ошибки
    if [ -f "$BACKEND_DIR/logs/error.log" ]; then
        local error_count=$(tail -n 100 "$BACKEND_DIR/logs/error.log" | grep -c "ERROR" || echo "0")
        log "🚨 Ошибок в логах Django: $error_count"
    fi
    
    if [ -f "$FRONTEND_DIR/npm-debug.log" ]; then
        local npm_errors=$(grep -c "ERROR" "$FRONTEND_DIR/npm-debug.log" || echo "0")
        log "🚨 Ошибок в npm логах: $npm_errors"
    fi
}

# Функция тестирования безопасности
test_security() {
    log "🔒 Тестирование безопасности..."
    
    # Проверка HTTPS (если настроен)
    safe_execute 5 "curl --max-time 5 -s -k https://localhost:8000/api/auth/register/ 2>/dev/null || echo 'HTTPS не настроен'" "Проверка HTTPS"
    
    # Тест SQL инъекций (базовый)
    safe_execute 5 "curl --max-time 5 -s 'http://localhost:8000/api/auth/register/?username=test%27%20OR%201=1--'" "Тест SQL инъекции"
    
    # Тест XSS (базовый)
    safe_execute 5 "curl --max-time 5 -s -X POST -H 'Content-Type: application/json' -d '{\"username\":\"<script>alert(1)</script>\",\"password\":\"test\"}' http://localhost:8000/api/auth/register/" "Тест XSS"
    
    # Проверка заголовков безопасности
    safe_execute 5 "curl --max-time 5 -s -I http://localhost:8000/api/auth/register/" "Проверка заголовков безопасности"
}

# Функция создания отчетов о тестировании
generate_testing_report() {
    log "📈 Создание отчета о тестировании..."
    
    cat > "$PROJECT_ROOT/agents/reports/testing_status_$(date '+%Y%m%d_%H%M').md" << EOF
# 🐛 ОТЧЕТ О ТЕСТИРОВАНИИ
# Тестировщик-агент | $(date)

## 🎯 ОБЩАЯ ИНФОРМАЦИЯ
- **Проект:** Президент: Экономика и Власть
- **Тип тестирования:** Комплексное
- **Версия:** 2.0
- **Время отчета:** $(date)

## 🧪 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ

### 📊 Экономическая модель
- **Статус:** $(if [ -f "$BACKEND_DIR/game/services/enhanced_economic_model.py" ]; then echo "Найдена"; else echo "Не найдена"; fi)
- **Тесты:** $(if [ -f "$PROJECT_ROOT/test_enhanced_model.py" ]; then echo "Доступны"; else echo "Не найдены"; fi)

### 🌐 Django API
- **Статус:** $(curl --max-time 5 -s http://localhost:8000/api/auth/register/ >/dev/null && echo "Работает" || echo "Недоступен")
- **Unit тесты:** $(cd $BACKEND_DIR && python manage.py test --verbosity=0 2>/dev/null | grep -c "FAILED\|ERROR" || echo "Неизвестно")
- **Миграции:** $(cd $BACKEND_DIR && python manage.py showmigrations 2>/dev/null | grep -c "\[X\]" || echo "Неизвестно")

### 🎨 React Frontend
- **Статус:** $(curl --max-time 5 -s http://localhost:3000 >/dev/null && echo "Работает" || echo "Недоступен")
- **Unit тесты:** $(cd $FRONTEND_DIR && npm test -- --watchAll=false 2>/dev/null | grep -c "FAILED\|ERROR" || echo "Неизвестно")
- **ESLint:** $(cd $FRONTEND_DIR && npm run lint 2>/dev/null | grep -c "error" || echo "Неизвестно")

## ⚡ ПРОИЗВОДИТЕЛЬНОСТЬ
- **Время отклика API:** $(curl --max-time 5 -s -w '%{time_total}' http://localhost:8000/api/auth/register/ 2>/dev/null | tail -n1 || echo "Неизвестно")s
- **Время загрузки фронтенда:** $(curl --max-time 5 -s -w '%{time_total}' http://localhost:3000 2>/dev/null | tail -n1 || echo "Неизвестно")s

## 🚨 НАЙДЕННЫЕ ПРОБЛЕМЫ
$(if [ -f "$BACKEND_DIR/logs/error.log" ]; then
    echo "- Django ошибок: $(tail -n 100 "$BACKEND_DIR/logs/error.log" | grep -c "ERROR" || echo "0")"
else
    echo "- Django логи не найдены"
fi)

$(if [ -f "$FRONTEND_DIR/npm-debug.log" ]; then
    echo "- npm ошибок: $(grep -c "ERROR" "$FRONTEND_DIR/npm-debug.log" || echo "0")"
else
    echo "- npm логи не найдены"
fi)

## 📋 РЕКОМЕНДАЦИИ
1. Продолжить автоматизированное тестирование
2. Добавить интеграционные тесты
3. Настроить CI/CD pipeline
4. Улучшить покрытие тестами

---
*Отчет создан автоматически тестировщик-агентом*
EOF

    log "✅ Отчет о тестировании создан"
}

# Основной цикл работы
main() {
    log "🐛 Тестировщик-агент запущен"
    log "📁 Backend: $BACKEND_DIR"
    log "📁 Frontend: $FRONTEND_DIR"
    log "📝 Логи: $LOG_FILE"
    
    # Создание необходимых директорий
    mkdir -p "$PROJECT_ROOT/agents/reports"
    
    # Тестирование экономической модели
    test_economic_model
    
    # Тестирование Django API
    test_django_api
    
    # Тестирование React фронтенда
    test_react_frontend
    
    # Интеграционное тестирование
    test_integration
    
    # Тестирование производительности
    test_performance
    
    # Поиск ошибок
    find_errors
    
    # Тестирование безопасности
    test_security
    
    # Основной цикл мониторинга
    while true; do
        log "🔄 Цикл мониторинга тестирования..."
        
        # Периодическое тестирование
        test_performance
        find_errors
        
        # Создание отчетов каждые 30 минут
        local current_minute=$(date '+%M')
        if [ $((10#$current_minute % 30)) -eq 0 ]; then
            generate_testing_report
        fi
        
        log "✅ Цикл завершен, ожидание 60 секунд..."
        sleep 60
    done
}

# Запуск с обработкой сигналов
trap 'log "🛑 Тестировщик-агент остановлен"; exit 0' SIGINT SIGTERM

# Запуск основной функции
main "$@"
