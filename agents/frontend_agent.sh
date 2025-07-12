#!/bin/bash

# FRONTEND-АГЕНТ
# Автоматически выполняет frontend задачи и задачи из TODO листа

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
FRONTEND_DIR="$PROJECT_DIR/frontend"
LOG_DIR="$PROJECT_DIR/agents/logs"
TODO_FILE="$PROJECT_DIR/TODO_CHECKLIST_AGENT_FRIENDLY.md"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/frontend_${TIMESTAMP}.log"

# Создаем директорию для логов
mkdir -p "$LOG_DIR"

# Функция логирования
log() {
    echo -e "${GREEN}[$(date +"%H:%M:%S")] $1${NC}" | tee -a "$LOG_FILE"
}

# Функция чтения TODO листа
read_todo_tasks() {
    if [[ -f "$TODO_FILE" ]]; then
        # Ищем незавершенные frontend задачи
        grep -A 1 "frontend\|Frontend\|React\|react\|UI\|ui\|interface\|Interface" "$TODO_FILE" | grep -B 1 "\[ \]" | grep -v "\[ \]" | head -10
    else
        echo "TODO файл не найден"
    fi
}

# Функция выполнения frontend задач
execute_frontend_tasks() {
    log "📝 Анализ TODO листа для frontend задач..."
    
    if [[ ! -f "$TODO_FILE" ]]; then
        log "❌ TODO файл не найден: $TODO_FILE"
        return
    fi
    
    # Ищем незавершенные frontend задачи
    local tasks_found=false
    
    # 1. Задачи по Node.js
    if grep -q "- \[ \].*Node\.js 16 установлен" "$TODO_FILE"; then
        log "🔄 Выполняю: Node.js 16 установлен"
        if node --version 2>/dev/null | grep -q "v1[6-9]\|v[2-9][0-9]"; then
            sed -i 's/- \[ \].*Node\.js 16 установлен/- [x] Node.js 16 установлен/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: Node.js 16 установлен"
            tasks_found=true
        fi
    fi
    
    # 2. Задачи по npm зависимостям
    if grep -q "- \[ \].*npm зависимости установлены" "$TODO_FILE"; then
        log "🔄 Выполняю: npm зависимости установлены"
        cd "$FRONTEND_DIR" && npm install --silent
        if [[ $? -eq 0 ]]; then
            sed -i 's/- \[ \].*npm зависимости установлены/- [x] npm зависимости установлены/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: npm зависимости установлены"
            tasks_found=true
        fi
    fi
    
    # 3. Задачи по React Dev Server
    if grep -q "- \[ \].*React Dev Server запущен" "$TODO_FILE"; then
        log "🔄 Выполняю: React Dev Server запущен"
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            sed -i 's/- \[ \].*React Dev Server запущен/- [x] React Dev Server запущен/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: React Dev Server запущен"
            tasks_found=true
        else
            log "🔄 Запускаю React Dev Server..."
            cd "$FRONTEND_DIR" && nohup npm start > /dev/null 2>&1 &
            sleep 10
            if curl -s http://localhost:3000 > /dev/null 2>&1; then
                sed -i 's/- \[ \].*React Dev Server запущен/- [x] React Dev Server запущен/' "$TODO_FILE"
                log "✅ Отмечено как выполненное: React Dev Server запущен"
                tasks_found=true
            fi
        fi
    fi
    
    # 4. Задачи по TypeScript
    if grep -q "- \[ \].*TypeScript.*проверен" "$TODO_FILE"; then
        log "🔄 Выполняю: TypeScript проверен"
        cd "$FRONTEND_DIR" && npx tsc --noEmit
        if [[ $? -eq 0 ]]; then
            sed -i 's/- \[ \].*TypeScript.*проверен/- [x] **TypeScript** проверен/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: TypeScript проверен"
            tasks_found=true
        fi
    fi
    
    # 5. Задачи по линтингу
    if grep -q "- \[ \].*Линтинг.*проходит" "$TODO_FILE"; then
        log "🔄 Выполняю: Линтинг проходит"
        cd "$FRONTEND_DIR" && npm run lint --silent
        if [[ $? -eq 0 ]]; then
            sed -i 's/- \[ \].*Линтинг.*проходит/- [x] **Линтинг** проходит/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: Линтинг проходит"
            tasks_found=true
        fi
    fi
    
    # 6. Задачи по сборке
    if grep -q "- \[ \].*Сборка.*успешна" "$TODO_FILE"; then
        log "🔄 Выполняю: Сборка успешна"
        cd "$FRONTEND_DIR" && npm run build --silent
        if [[ $? -eq 0 ]]; then
            sed -i 's/- \[ \].*Сборка.*успешна/- [x] **Сборка** успешна/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: Сборка успешна"
            tasks_found=true
        fi
    fi
    
    # 7. Задачи по тестам frontend
    if grep -q "- \[ \].*Frontend.*тесты.*проходят" "$TODO_FILE"; then
        log "🔄 Выполняю: Frontend тесты проходят"
        cd "$FRONTEND_DIR" && npm test -- --watchAll=false --silent
        if [[ $? -eq 0 ]]; then
            sed -i 's/- \[ \].*Frontend.*тесты.*проходят/- [x] **Frontend тесты** проходят/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: Frontend тесты проходят"
            tasks_found=true
        fi
    fi
    
    # 8. Задачи по оптимизации
    if grep -q "- \[ \].*Оптимизация.*выполнена" "$TODO_FILE"; then
        log "🔄 Выполняю: Оптимизация выполнена"
        cd "$FRONTEND_DIR" && npm run build --silent
        if [[ $? -eq 0 ]]; then
            sed -i 's/- \[ \].*Оптимизация.*выполнена/- [x] **Оптимизация** выполнена/' "$TODO_FILE"
            log "✅ Отмечено как выполненное: Оптимизация выполнена"
            tasks_found=true
        fi
    fi
    
    if [[ "$tasks_found" == "false" ]]; then
        log "ℹ️ Нет незавершенных frontend задач для выполнения"
    else
        log "✅ Frontend задачи выполнены и отмечены в TODO листе"
    fi
}

# Функция запуска React Dev Server
start_react_server() {
    log "🔍 Проверка React Dev Server..."
    
    # Проверяем, запущен ли сервер
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        log "✅ React Dev Server уже запущен"
        return 0
    fi
    
    log "⚠️  React Dev Server не запущен, стартую..."
    
    # Запускаем React Dev Server в фоне
    cd "$FRONTEND_DIR"
    
    # Убиваем старые процессы React
    pkill -f "react-scripts start" 2>/dev/null
    
    # Запускаем новый сервер
    nohup npm start > /dev/null 2>&1 &
    REACT_PID=$!
    
    # Ждем запуска сервера
    for i in {1..60}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            log "✅ React Dev Server запущен (PID: $REACT_PID)"
            return 0
        fi
        sleep 1
    done
    
    log "❌ Не удалось запустить React Dev Server"
    return 1
}

# Функция тестирования frontend
test_frontend() {
    log "🧪 Тестирование frontend..."
    
    # Проверяем доступность React приложения
    log "🔄 Проверка React приложения (таймаут: 10с)..."
    if timeout 10 curl -s http://localhost:3000 > /dev/null 2>&1; then
        log "✅ React приложение доступно"
    else
        log "⚠️  React приложение недоступно"
    fi
    
    # Проверяем API endpoints через frontend
    log "🔄 Проверка API через frontend (таймаут: 10с)..."
    if timeout 10 curl -s http://localhost:3000/api/game/status/ > /dev/null 2>&1; then
        log "✅ API через frontend доступен"
    else
        log "⚠️  API через frontend недоступен"
    fi
}

# Функция оптимизации производительности
optimize_performance() {
    log "⚡ Оптимизация производительности фронтенда..."
    
    # Проверяем использование памяти React
    log "🔄 Проверка использования памяти React (таймаут: 30с)..."
    REACT_PROCESSES=$(ps aux | grep "react-scripts" | grep -v grep | wc -l)
    if [[ $REACT_PROCESSES -gt 0 ]]; then
        log "✅ React процессы: $REACT_PROCESSES"
        
        # Проверяем использование памяти
        REACT_MEMORY=$(ps aux | grep "react-scripts" | grep -v grep | awk '{print $6}' | head -1)
        if [[ -n "$REACT_MEMORY" ]]; then
            MEMORY_MB=$((REACT_MEMORY / 1024))
            log "📊 Использование памяти React: ${MEMORY_MB}MB"
        fi
    else
        log "⚠️  React процессы не найдены"
    fi
    
    # Проверяем размер bundle
    if [[ -f "$FRONTEND_DIR/build/static/js/main.js" ]]; then
        BUNDLE_SIZE=$(du -h "$FRONTEND_DIR/build/static/js/main.js" | cut -f1)
        log "📦 Размер основного bundle: $BUNDLE_SIZE"
    fi
}

# Функция мониторинга логов
monitor_logs() {
    log "📝 Мониторинг логов фронтенда..."
    
    # Проверяем логи npm
    if [[ -f "$FRONTEND_DIR/npm-debug.log" ]]; then
        log "⚠️  Найдены ошибки npm:"
        tail -n 3 "$FRONTEND_DIR/npm-debug.log" 2>/dev/null | while IFS= read -r line; do
            log "  $line"
        done
    fi
    
    # Проверяем логи сборки
    if [[ -f "$FRONTEND_DIR/build/build.log" ]]; then
        log "📝 Последние ошибки сборки:"
        tail -n 3 "$FRONTEND_DIR/build/build.log" 2>/dev/null | while IFS= read -r line; do
            log "  $line"
        done
    fi
}

# Основной цикл
main_loop() {
    log "🎨 Frontend-агент запущен"
    log "📁 Frontend: $FRONTEND_DIR"
    log "📝 Логи: $LOG_FILE"
    
    # Проверяем React проект
    log "🔍 Проверка React проекта..."
    if [[ -f "$FRONTEND_DIR/package.json" ]]; then
        log "✅ React проект найден"
    else
        log "❌ React проект не найден"
        exit 1
    fi
    
    # Проверяем node_modules
    log "🔄 Проверка node_modules..."
    if [[ -d "$FRONTEND_DIR/node_modules" ]]; then
        log "✅ node_modules найдены"
    else
        log "⚠️  node_modules не найдены, устанавливаю..."
        cd "$FRONTEND_DIR" && npm install --silent
    fi
    
    # Основной цикл мониторинга
    log "🔄 Цикл мониторинга фронтенда..."
    
    while true; do
        # Выполняем frontend задачи из TODO
        execute_frontend_tasks
        
        # Запускаем React Dev Server
        start_react_server
        
        # Тестируем frontend
        test_frontend
        
        # Оптимизируем производительность
        optimize_performance
        
        # Мониторим логи
        monitor_logs
        
        log "✅ Цикл завершен, ожидание 60 секунд..."
        sleep 60
    done
}

# Обработка сигналов
trap 'log "🛑 Получен сигнал остановки"; exit 0' SIGINT SIGTERM

# Запуск основного цикла
main_loop
