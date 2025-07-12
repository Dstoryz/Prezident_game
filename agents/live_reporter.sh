#!/bin/bash

# 📊 ЖИВОЙ РЕПОРТЕР - ОТЧЕТЫ КАЖДУЮ МИНУТУ
# Выводит отчеты каждую минуту и после выполнения задач

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
REPORT_INTERVAL=60  # секунд
LAST_TODO_COUNT=0
LAST_REPORT_TIME=0

# Функция получения статуса агентов
get_agent_status() {
    local agents=("architect" "backend" "frontend" "testing" "devops" "analyst")
    local working=0
    local total=${#agents[@]}
    
    for agent in "${agents[@]}"; do
        local pid=$(ps aux | grep -E ".*${agent}_agent.*sh" | grep -v grep | awk '{print $2}' | head -1)
        if [[ -n "$pid" ]]; then
            ((working++))
        fi
    done
    
    echo "$working/$total"
}

# Функция проверки портов
check_ports() {
    local django_active=0
    local react_active=0
    
    if lsof -i :8000 >/dev/null 2>&1; then
        django_active=1
    fi
    
    if lsof -i :3000 >/dev/null 2>&1; then
        react_active=1
    fi
    
    echo "$django_active:$react_active"
}

# Функция получения прогресса TODO
get_todo_progress() {
    if [[ -f "$TODO_FILE" ]]; then
        local total=$(grep -c "^- \[" "$TODO_FILE" 2>/dev/null || echo "0")
        local completed=$(grep -c "^- \[x\]" "$TODO_FILE" 2>/dev/null || echo "0")
        local percentage=$((completed * 100 / (total + 1)))
        echo "$completed:$total:$percentage"
    else
        echo "0:0:0"
    fi
}

# Функция проверки новых выполненных задач
check_new_completed_tasks() {
    if [[ -f "$TODO_FILE" ]]; then
        local current_count=$(grep -c "^- \[x\]" "$TODO_FILE" 2>/dev/null || echo "0")
        if [[ $current_count -gt $LAST_TODO_COUNT ]]; then
            local new_tasks=$((current_count - LAST_TODO_COUNT))
            LAST_TODO_COUNT=$current_count
            echo "$new_tasks"
        else
            echo "0"
        fi
    else
        echo "0"
    fi
}

# Функция получения последних событий
get_latest_events() {
    local events=()
    local log_dir="$PROJECT_DIR/agents/logs"
    
    if [[ -d "$log_dir" ]]; then
        for log_file in "$log_dir"/*.log; do
            if [[ -f "$log_file" ]]; then
                local agent=$(basename "$log_file" | cut -d'_' -f1)
                local last_line=$(tail -1 "$log_file" 2>/dev/null | sed 's/^[[:space:]]*//' | cut -c1-60)
                if [[ -n "$last_line" ]]; then
                    events+=("$agent: $last_line")
                fi
            fi
        done
    fi
    
    # Возвращаем только последние 3 события
    printf '%s\n' "${events[@]: -3}"
}

# Функция вывода отчета
print_report() {
    local current_time=$(date '+%H:%M:%S')
    local agent_status=$(get_agent_status)
    local port_status=$(check_ports)
    local todo_progress=$(get_todo_progress)
    local new_tasks=$(check_new_completed_tasks)
    
    # Парсим данные
    IFS=':' read -r working_agents total_agents <<< "$agent_status"
    IFS=':' read -r django_active react_active <<< "$port_status"
    IFS=':' read -r completed_tasks total_tasks percentage <<< "$todo_progress"
    
    # Очищаем экран каждые 5 минут
    local minutes_since_start=$((SECONDS / 60))
    if [[ $((minutes_since_start % 5)) -eq 0 ]] && [[ $minutes_since_start -gt 0 ]]; then
        clear
        echo -e "${BOLD}${CYAN}🎯 ЖИВОЙ РЕПОРТЕР - ПРОЕКТ 'ПРЕЗИДЕНТ: ЭКОНОМИКА И ВЛАСТЬ'${NC}"
        echo -e "${CYAN}================================================================${NC}"
        echo ""
    fi
    
    # Выводим отчет
    echo -e "${BOLD}📊 ОТЧЕТ НА ${YELLOW}$current_time${NC}${BOLD} (минута $((SECONDS / 60)))${NC}"
    echo -e "${CYAN}----------------------------------------------------------------${NC}"
    
    # Статус агентов
    if [[ $working_agents -eq $total_agents ]]; then
        echo -e "🤖 Агенты: ${GREEN}✅ $working_agents/$total_agents работают${NC}"
    else
        echo -e "🤖 Агенты: ${YELLOW}⚠️  $working_agents/$total_agents работают${NC}"
    fi
    
    # Статус портов
    local ports_status="🌐 Порты: "
    if [[ $django_active -eq 1 ]]; then
        ports_status+="${GREEN}✅ Django${NC}"
    else
        ports_status+="${RED}❌ Django${NC}"
    fi
    ports_status+=" | "
    if [[ $react_active -eq 1 ]]; then
        ports_status+="${GREEN}✅ React${NC}"
    else
        ports_status+="${RED}❌ React${NC}"
    fi
    echo -e "$ports_status"
    
    # Прогресс TODO
    echo -e "📈 Прогресс: ${BLUE}$completed_tasks/$total_tasks задач ($percentage%)${NC}"
    
    # Новые выполненные задачи
    if [[ $new_tasks -gt 0 ]]; then
        echo -e "${GREEN}🎉 ВЫПОЛНЕНО НОВЫХ ЗАДАЧ: $new_tasks${NC}"
    fi
    
    # Последние события
    echo -e "${PURPLE}📝 Последние события:${NC}"
    local latest_events=($(get_latest_events))
    for event in "${latest_events[@]}"; do
        if [[ -n "$event" ]]; then
            echo -e "  • $event"
        fi
    done
    
    echo -e "${CYAN}----------------------------------------------------------------${NC}"
    echo -e "${YELLOW}⏰ Следующий отчет через $((REPORT_INTERVAL / 60)) минут...${NC}"
    echo ""
}

# Функция мониторинга в реальном времени
monitor_realtime() {
    echo -e "${BOLD}${GREEN}🚀 Запуск живого репортера...${NC}"
    echo -e "${YELLOW}📊 Отчеты каждые $((REPORT_INTERVAL / 60)) минут${NC}"
    echo -e "${YELLOW}🆕 Уведомления о выполненных задачах${NC}"
    echo -e "${YELLOW}🔄 Нажмите Ctrl+C для выхода${NC}"
    echo ""
    
    # Инициализация счетчиков
    LAST_TODO_COUNT=$(grep -c "^- \[x\]" "$TODO_FILE" 2>/dev/null || echo "0")
    
    # Основной цикл
    while true; do
        print_report
        sleep $REPORT_INTERVAL
    done
}

# Обработка сигналов для корректного завершения
trap 'echo -e "\n${YELLOW}🛑 Живой репортер остановлен${NC}"; exit 0' INT TERM

# Запуск мониторинга
monitor_realtime 