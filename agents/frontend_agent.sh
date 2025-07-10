#!/bin/bash

# 🎨 ФРОНТЕНД-АГЕНТ
# Разработчик пользовательского интерфейса проекта "Президент: Экономика и Власть"

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
FRONTEND_DIR="$PROJECT_ROOT/frontend"
LOG_FILE="$PROJECT_ROOT/agents/logs/frontend_$(date '+%Y%m%d_%H%M%S').log"

# Функция логирования
log() {
    echo -e "${PURPLE}[$(date '+%H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
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

# Функция проверки React проекта
check_react_project() {
    log "🔍 Проверка React проекта..."
    
    if [ ! -f "$FRONTEND_DIR/package.json" ]; then
        log "❌ React проект не найден в $FRONTEND_DIR"
        return 1
    fi
    
    log "✅ React проект найден"
    
    # Проверка зависимостей
    safe_execute 60 "cd $FRONTEND_DIR && npm list --depth=0" "Проверка React зависимостей"
    
    # Проверка версии Node.js
    safe_execute 10 "node --version" "Проверка версии Node.js"
    
    # Проверка версии npm
    safe_execute 10 "npm --version" "Проверка версии npm"
    
    return 0
}

# Функция проверки компонентов
check_components() {
    log "🧩 Проверка React компонентов..."
    
    local components=(
        "src/components/GameDashboard.tsx"
        "src/components/GamePage.tsx"
        "src/components/IndicatorsPanel.tsx"
        "src/components/ParametersPanel.tsx"
        "src/components/EventsPanel.tsx"
    )
    
    for component in "${components[@]}"; do
        if [ -f "$FRONTEND_DIR/$component" ]; then
            log "✅ $component найден"
        else
            log "❌ $component не найден"
        fi
    done
}

# Функция проверки API интеграции
check_api_integration() {
    log "🌐 Проверка интеграции с API..."
    
    # Проверка файла API
    if [ -f "$FRONTEND_DIR/src/services/api.ts" ]; then
        log "✅ API сервис найден"
        
        # Проверка базового URL
        if grep -q "localhost:8000" "$FRONTEND_DIR/src/services/api.ts"; then
            log "✅ API URL настроен правильно"
        else
            log "⚠️  API URL может быть неправильным"
        fi
    else
        log "❌ API сервис не найден"
    fi
    
    # Проверка типов
    if [ -f "$FRONTEND_DIR/src/types/game.ts" ]; then
        log "✅ Типы игры найдены"
    else
        log "❌ Типы игры не найдены"
    fi
}

# Функция проверки доступности фронтенда
check_frontend_availability() {
    log "🌐 Проверка доступности фронтенда..."
    
    # Проверка React dev server
    safe_execute 10 "curl --max-time 5 -s http://localhost:3000" "Проверка React dev server"
    
    # Проверка статических файлов
    if [ -f "$FRONTEND_DIR/public/index.html" ]; then
        log "✅ index.html найден"
    else
        log "❌ index.html не найден"
    fi
}

# Функция оптимизации производительности
optimize_performance() {
    log "⚡ Оптимизация производительности фронтенда..."
    
    # Проверка размера bundle
    if [ -f "$FRONTEND_DIR/build/static/js/main.*.js" ]; then
        local bundle_size=$(ls -lh "$FRONTEND_DIR/build/static/js/main.*.js" | awk '{print $5}')
        log "📦 Размер bundle: $bundle_size"
        
        # Проверка на большие файлы
        local size_in_kb=$(ls -l "$FRONTEND_DIR/build/static/js/main.*.js" | awk '{print $5}' | sed 's/K//')
        if [ $size_in_kb -gt 1000 ]; then
            log "⚠️  Bundle слишком большой ($size_in_kb KB)"
        else
            log "✅ Размер bundle оптимальный"
        fi
    fi
    
    # Проверка использования памяти
    safe_execute 30 "ps aux | grep 'npm start' | grep -v grep" "Проверка использования памяти React"
}

# Функция тестирования
run_tests() {
    log "🧪 Запуск тестов фронтенда..."
    
    # Проверка наличия тестов
    if [ -f "$FRONTEND_DIR/src/App.test.tsx" ]; then
        safe_execute 120 "cd $FRONTEND_DIR && npm test -- --watchAll=false" "Запуск unit тестов"
    else
        log "⚠️  Unit тесты не найдены"
    fi
    
    # Проверка линтера
    if [ -f "$FRONTEND_DIR/package.json" ] && grep -q "eslint" "$FRONTEND_DIR/package.json"; then
        safe_execute 60 "cd $FRONTEND_DIR && npm run lint" "Проверка линтера"
    else
        log "⚠️  ESLint не настроен"
    fi
}

# Функция сборки проекта
build_project() {
    log "🏗️ Сборка проекта..."
    
    # Установка зависимостей если нужно
    if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
        log "📦 Установка зависимостей..."
        safe_execute 300 "cd $FRONTEND_DIR && npm install" "Установка npm зависимостей"
    fi
    
    # Сборка проекта
    safe_execute 300 "cd $FRONTEND_DIR && npm run build" "Сборка React проекта"
    
    # Проверка результата сборки
    if [ -d "$FRONTEND_DIR/build" ]; then
        log "✅ Сборка завершена успешно"
        local build_size=$(du -sh "$FRONTEND_DIR/build" | cut -f1)
        log "📦 Размер сборки: $build_size"
    else
        log "❌ Ошибка сборки"
    fi
}

# Функция мониторинга логов
monitor_logs() {
    log "📝 Мониторинг логов фронтенда..."
    
    # Проверка логов npm
    if [ -f "$FRONTEND_DIR/npm-debug.log" ]; then
        local error_count=$(grep -c "ERROR" "$FRONTEND_DIR/npm-debug.log" || echo "0")
        log "🚨 Ошибок в npm логах: $error_count"
        
        if [ $error_count -gt 5 ]; then
            log "⚠️  Много ошибок в npm логах!"
            tail -n 3 "$FRONTEND_DIR/npm-debug.log" | tee -a "$LOG_FILE"
        fi
    fi
    
    # Проверка логов браузера (если доступны)
    if [ -f "$FRONTEND_DIR/browser.log" ]; then
        local browser_errors=$(grep -c "Error" "$FRONTEND_DIR/browser.log" || echo "0")
        log "🌐 Ошибок в браузере: $browser_errors"
    fi
}

# Функция создания отчетов
generate_frontend_report() {
    log "📈 Создание отчета о состоянии фронтенда..."
    
    cat > "$PROJECT_ROOT/agents/reports/frontend_status_$(date '+%Y%m%d_%H%M').md" << EOF
# 🎨 ОТЧЕТ О СОСТОЯНИИ ФРОНТЕНДА
# Фронтенд-агент | $(date)

## 🎯 ОБЩАЯ ИНФОРМАЦИЯ
- **Проект:** Президент: Экономика и Власть
- **Frontend:** React + TypeScript
- **Версия:** 2.0
- **Время отчета:** $(date)

## 🏗️ АРХИТЕКТУРА
- **React:** $(cd $FRONTEND_DIR && npm list react 2>/dev/null | grep react || echo "Неизвестно")
- **TypeScript:** $(cd $FRONTEND_DIR && npm list typescript 2>/dev/null | grep typescript || echo "Неизвестно")
- **Node.js:** $(node --version 2>/dev/null || echo "Неизвестно")

## 📊 МЕТРИКИ
- **Frontend доступен:** $(curl --max-time 5 -s http://localhost:3000 >/dev/null && echo "Да" || echo "Нет")
- **React процессы:** $(ps aux | grep "npm start" | grep -v grep | wc -l)
- **Размер bundle:** $(if [ -f "$FRONTEND_DIR/build/static/js/main.*.js" ]; then ls -lh "$FRONTEND_DIR/build/static/js/main.*.js" | awk '{print $5}'; else echo "Неизвестно"; fi)

## 🧪 ТЕСТИРОВАНИЕ
- **Unit тесты:** $(cd $FRONTEND_DIR && npm test -- --watchAll=false 2>/dev/null | grep -c "FAILED\|ERROR" || echo "Неизвестно")
- **ESLint:** $(cd $FRONTEND_DIR && npm run lint 2>/dev/null | grep -c "error" || echo "Неизвестно")

## 🚨 ПРОБЛЕМЫ
$(if [ -f "$FRONTEND_DIR/npm-debug.log" ]; then
    echo "- Ошибок в npm логах: $(grep -c "ERROR" "$FRONTEND_DIR/npm-debug.log" || echo "0")"
else
    echo "- Логи npm не найдены"
fi)

## 📋 СЛЕДУЮЩИЕ ШАГИ
1. Продолжить оптимизацию UI/UX
2. Улучшить производительность компонентов
3. Добавить новые функции интерфейса
4. Расширить тестирование

---
*Отчет создан автоматически фронтенд-агентом*
EOF

    log "✅ Отчет о состоянии фронтенда создан"
}

# Основной цикл работы
main() {
    log "🎨 Фронтенд-агент запущен"
    log "📁 Frontend: $FRONTEND_DIR"
    log "📝 Логи: $LOG_FILE"
    
    # Создание необходимых директорий
    mkdir -p "$PROJECT_ROOT/agents/reports"
    
    # Проверка React проекта
    if ! check_react_project; then
        log "❌ Проблемы с React проектом"
        return 1
    fi
    
    # Проверка компонентов
    check_components
    
    # Проверка API интеграции
    check_api_integration
    
    # Сборка проекта
    build_project
    
    # Запуск тестов
    run_tests
    
    # Основной цикл мониторинга
    while true; do
        log "🔄 Цикл мониторинга фронтенда..."
        
        # Проверка доступности фронтенда
        check_frontend_availability
        
        # Оптимизация производительности
        optimize_performance
        
        # Мониторинг логов
        monitor_logs
        
        # Создание отчетов каждые 30 минут
        local current_minute=$(date '+%M')
        if [ $((10#$current_minute % 30)) -eq 0 ]; then
            generate_frontend_report
        fi
        
        log "✅ Цикл завершен, ожидание 60 секунд..."
        sleep 60
    done
}

# Запуск с обработкой сигналов
trap 'log "🛑 Фронтенд-агент остановлен"; exit 0' SIGINT SIGTERM

# Запуск основной функции
main "$@"
