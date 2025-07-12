#!/bin/bash

# 🚀 BACKEND-АГЕНТ С КОМАНДНОЙ СИСТЕМОЙ
# Читает команды от архитектора и выполняет их

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
COMMANDS_FILE="$PROJECT_DIR/agents/commands/backend_tasks.txt"
REPORTS_DIR="$PROJECT_DIR/agents/reports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$LOG_DIR/backend_commander_${TIMESTAMP}.log"

# Создаем директории
mkdir -p "$LOG_DIR" "$REPORTS_DIR"

# Функция логирования
log() {
    echo -e "${BLUE}[$(date +"%H:%M:%S")] $1${NC}" | tee -a "$LOG_FILE"
}

# Функция чтения команд
read_commands() {
    if [[ -f "$COMMANDS_FILE" ]]; then
        # Читаем все pending команды
        awk '/STATUS: pending/{flag=1; task=""} /^---$/{if(flag) print task; flag=0; task=""} flag{task=task $0 "\n"} END{if(flag) print task}' "$COMMANDS_FILE"
    else
        log "❌ Файл команд не найден: $COMMANDS_FILE"
        return 1
    fi
}

# Функция обновления статуса задачи
update_task_status() {
    local task_id="$1"
    local status="$2"
    local result="$3"
    
    if [[ -f "$COMMANDS_FILE" ]]; then
        # Обновляем статус задачи
        sed -i "/TASK_ID: $task_id/,/^---$/ s/STATUS: .*/STATUS: $status/" "$COMMANDS_FILE"
        
        if [[ "$status" == "completed" ]]; then
            local completed_time=$(date +"%Y-%m-%d %H:%M:%S")
            sed -i "/TASK_ID: $task_id/,/^---$/ s/COMPLETED: .*/COMPLETED: $completed_time/" "$COMMANDS_FILE"
            sed -i "/TASK_ID: $task_id/,/^---$/ s/RESULT: .*/RESULT: $result/" "$COMMANDS_FILE"
        fi
        
        log "✅ Обновлен статус задачи $task_id: $status"
    fi
}

# Функция выполнения команды check_python_version
execute_check_python_version() {
    local task_id="$1"
    log "🔄 Выполняю: $task_id - Проверка версии Python"
    
    update_task_status "$task_id" "running" ""
    
    if python3 --version 2>/dev/null | grep -q "Python 3\.[9-9]\|Python 3\.[1-9][0-9]"; then
        local version=$(python3 --version 2>/dev/null)
        update_task_status "$task_id" "completed" "SUCCESS: $version"
        log "✅ Python версия проверена: $version"
        return 0
    else
        update_task_status "$task_id" "failed" "ERROR: Python 3.9+ не найден"
        log "❌ Python 3.9+ не найден"
        return 1
    fi
}

# Функция выполнения команды check_virtual_env
execute_check_virtual_env() {
    local task_id="$1"
    log "🔄 Выполняю: $task_id - Проверка виртуального окружения"
    
    update_task_status "$task_id" "running" ""
    
    if [[ -d "$PROJECT_DIR/.venv" ]]; then
        update_task_status "$task_id" "completed" "SUCCESS: Виртуальное окружение найдено"
        log "✅ Виртуальное окружение найдено"
        return 0
    else
        update_task_status "$task_id" "failed" "ERROR: Виртуальное окружение не найдено"
        log "❌ Виртуальное окружение не найдено"
        return 1
    fi
}

# Функция выполнения команды install_dependencies
execute_install_dependencies() {
    local task_id="$1"
    log "🔄 Выполняю: $task_id - Установка зависимостей"
    
    update_task_status "$task_id" "running" ""
    
    if [[ -f "$BACKEND_DIR/requirements.txt" ]]; then
        cd "$BACKEND_DIR" && source ../.venv/bin/activate && pip install -r requirements.txt --quiet
        if [[ $? -eq 0 ]]; then
            update_task_status "$task_id" "completed" "SUCCESS: Зависимости установлены"
            log "✅ Зависимости установлены"
            return 0
        else
            update_task_status "$task_id" "failed" "ERROR: Ошибка установки зависимостей"
            log "❌ Ошибка установки зависимостей"
            return 1
        fi
    else
        update_task_status "$task_id" "failed" "ERROR: requirements.txt не найден"
        log "❌ requirements.txt не найден"
        return 1
    fi
}

# Функция выполнения команд
execute_commands() {
    log "📝 Чтение команд от архитектора..."
    
    if [[ ! -f "$COMMANDS_FILE" ]]; then
        log "❌ Файл команд не найден: $COMMANDS_FILE"
        return
    fi
    
    # Читаем pending команды
    local commands=$(read_commands)
    log "🔍 Найдено команд: $(echo "$commands" | wc -l)"
    if [[ -z "$commands" ]]; then
        log "ℹ️ Нет pending команд для выполнения"
        return
    fi
    
    # Обрабатываем каждую команду
    local current_task_id=""
    local current_command=""
    
    echo "$commands" | while IFS= read -r line; do
        if [[ "$line" =~ TASK_ID:[[:space:]]*(.+) ]]; then
            current_task_id="${BASH_REMATCH[1]}"
            log "📋 Обрабатываю задачу: $current_task_id"
        elif [[ "$line" =~ COMMAND:[[:space:]]*(.+) ]]; then
            current_command="${BASH_REMATCH[1]}"
            log "🔄 Команда: $current_command для задачи: $current_task_id"
            
            # Выполняем команду
            case "$current_command" in
                "check_python_version")
                    execute_check_python_version "$current_task_id"
                    ;;
                "check_virtual_env")
                    execute_check_virtual_env "$current_task_id"
                    ;;
                "install_dependencies")
                    execute_install_dependencies "$current_task_id"
                    ;;
                *)
                    log "⚠️ Неизвестная команда: $current_command"
                    update_task_status "$current_task_id" "failed" "ERROR: Неизвестная команда"
                    ;;
            esac
        fi
    done
}

# Функция мониторинга Django
monitor_django() {
    log "🔍 Проверка Django сервера..."
    
    # Проверяем, запущен ли сервер
    if curl -s http://localhost:8000/api/game/status/ > /dev/null 2>&1; then
        log "✅ Django сервер работает"
    else
        log "⚠️ Django сервер не запущен"
    fi
}

# Основной цикл
main_loop() {
    log "🚀 Backend агент с командной системой запущен"
    log "📁 Backend: $BACKEND_DIR"
    log "📝 Логи: $LOG_FILE"
    log "📋 Команды: $COMMANDS_FILE"
    
    while true; do
        # Выполняем команды от архитектора
        execute_commands
        
        # Мониторим Django
        monitor_django
        
        # Проверка производительности
        log "⚡ Проверка производительности..."
        DJANGO_PROCESSES=$(ps aux | grep "manage.py runserver" | grep -v grep | wc -l)
        if [[ $DJANGO_PROCESSES -gt 0 ]]; then
            log "✅ Django процессы: $DJANGO_PROCESSES"
        else
            log "⚠️ Django процессы не найдены"
        fi
        
        log "✅ Цикл завершен, ожидание 10 секунд..."
        sleep 10
    done
}

# Обработка сигналов
trap 'log "🛑 Получен сигнал остановки"; exit 0' SIGINT SIGTERM

# Запуск основного цикла
main_loop 