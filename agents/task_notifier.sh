#!/bin/bash

# 🔔 СИСТЕМА УВЕДОМЛЕНИЙ О ВЫПОЛНЕННЫХ ЗАДАЧАХ
# Отслеживает изменения в TODO листе и уведомляет о выполненных задачах

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Настройки
PROJECT_DIR="/home/alex/Downloads/Prezident_project"
TODO_FILE="$PROJECT_DIR/TODO_CHECKLIST.md"
LOG_FILE="$PROJECT_DIR/agents/logs/task_notifications.log"
CHECK_INTERVAL=30  # секунд

# Создаем директорию для логов
mkdir -p "$(dirname "$LOG_FILE")"

# Функция логирования
log_notification() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Функция получения хеша TODO файла
get_todo_hash() {
    if [[ -f "$TODO_FILE" ]]; then
        md5sum "$TODO_FILE" 2>/dev/null | cut -d' ' -f1 || echo "no_file"
    else
        echo "no_file"
    fi
}

# Функция получения выполненных задач
get_completed_tasks() {
    if [[ -f "$TODO_FILE" ]]; then
        grep -n "^- \[x\]" "$TODO_FILE" 2>/dev/null || echo ""
    else
        echo ""
    fi
}

# Функция получения незавершенных задач
get_pending_tasks() {
    if [[ -f "$TODO_FILE" ]]; then
        grep -n "^- \[ \]" "$TODO_FILE" 2>/dev/null || echo ""
    else
        echo ""
    fi
}

# Функция анализа изменений в TODO
analyze_todo_changes() {
    local current_hash=$(get_todo_hash)
    local current_completed=$(get_completed_tasks)
    local current_pending=$(get_pending_tasks)
    
    # Сохраняем текущее состояние во временный файл
    local temp_file="/tmp/todo_state_$$"
    echo "$current_hash" > "$temp_file"
    echo "$current_completed" >> "$temp_file"
    echo "$current_pending" >> "$temp_file"
    
    # Если это первая проверка, просто сохраняем состояние
    if [[ ! -f "/tmp/todo_previous_state" ]]; then
        cp "$temp_file" "/tmp/todo_previous_state"
        rm -f "$temp_file"
        return
    fi
    
    # Читаем предыдущее состояние
    local prev_hash=$(head -1 "/tmp/todo_previous_state" 2>/dev/null || echo "")
    local prev_completed=$(sed -n '2p' "/tmp/todo_previous_state" 2>/dev/null || echo "")
    local prev_pending=$(sed -n '3p' "/tmp/todo_previous_state" 2>/dev/null || echo "")
    
    # Проверяем изменения
    if [[ "$current_hash" != "$prev_hash" ]]; then
        # Файл изменился
        local completed_count=$(echo "$current_completed" | wc -l)
        local prev_completed_count=$(echo "$prev_completed" | wc -l)
        
        if [[ $completed_count -gt $prev_completed_count ]]; then
            local new_tasks=$((completed_count - prev_completed_count))
            log_notification "${GREEN}🎉 ВЫПОЛНЕНО НОВЫХ ЗАДАЧ: $new_tasks${NC}"
            
            # Показываем новые выполненные задачи
            echo -e "${GREEN}📋 НОВЫЕ ВЫПОЛНЕННЫЕ ЗАДАЧИ:${NC}"
            local new_tasks_list=$(comm -13 <(echo "$prev_completed" | sort) <(echo "$current_completed" | sort))
            echo "$new_tasks_list" | while read -r line; do
                if [[ -n "$line" ]]; then
                    local task_text=$(echo "$line" | sed 's/^[0-9]*:^- \[x\] //')
                    echo -e "  ✅ $task_text"
                fi
            done
            echo ""
        fi
        
        # Обновляем предыдущее состояние
        cp "$temp_file" "/tmp/todo_previous_state"
    fi
    
    rm -f "$temp_file"
}

# Функция вывода статистики
print_statistics() {
    local total_tasks=$(grep -c "^- \[" "$TODO_FILE" 2>/dev/null || echo "0")
    local completed_tasks=$(grep -c "^- \[x\]" "$TODO_FILE" 2>/dev/null || echo "0")
    local pending_tasks=$((total_tasks - completed_tasks))
    local percentage=$((completed_tasks * 100 / (total_tasks + 1)))
    
    echo -e "${BOLD}📊 СТАТИСТИКА ВЫПОЛНЕНИЯ ЗАДАЧ:${NC}"
    echo -e "${CYAN}----------------------------------------${NC}"
    echo -e "  📋 Всего задач: $total_tasks"
    echo -e "  ✅ Выполнено: $completed_tasks"
    echo -e "  ⏳ Осталось: $pending_tasks"
    echo -e "  📈 Прогресс: $percentage%"
    echo ""
}

# Функция мониторинга в реальном времени
monitor_tasks_realtime() {
    log_notification "${BOLD}${GREEN}🚀 Запуск системы уведомлений о задачах...${NC}"
    log_notification "${YELLOW}📊 Проверка каждые $CHECK_INTERVAL секунд${NC}"
    log_notification "${YELLOW}📁 Отслеживаемый файл: $TODO_FILE${NC}"
    echo ""
    
    # Инициализация
    analyze_todo_changes
    print_statistics
    
    # Основной цикл мониторинга
    while true; do
        # Проверяем изменения
        analyze_todo_changes
        
        # Ждем указанное время
        sleep $CHECK_INTERVAL
    done
}

# Обработка сигналов для корректного завершения
trap 'echo -e "\n${YELLOW}🛑 Система уведомлений остановлена${NC}"; rm -f "/tmp/todo_previous_state" 2>/dev/null; exit 0' INT TERM

# Запуск мониторинга
monitor_tasks_realtime 