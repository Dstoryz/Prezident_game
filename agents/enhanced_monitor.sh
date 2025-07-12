#!/bin/bash

# 🎯 УЛУЧШЕННЫЙ МОНИТОРИНГ АГЕНТОВ С АВТОМАТИЧЕСКИМИ ОТЧЕТАМИ
# Выводит отчет каждую минуту и после выполнения каждой задачи

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
LOG_DIR="$PROJECT_DIR/agents/logs"
TODO_FILE="$PROJECT_DIR/TODO_CHECKLIST.md"
REPORT_INTERVAL=60  # секунд
LAST_TODO_COUNT=0

# Функция очистки экрана
clear_screen() {
    clear
    echo -e "${BOLD}${CYAN}🎯 УЛУЧШЕННЫЙ МОНИТОРИНГ АГЕНТОВ - АВТОМАТИЧЕСКИЕ ОТЧЕТЫ${NC}"
    echo -e "${CYAN}========================================================${NC}"
    echo -e "${YELLOW}📅 Время: $(date '+%a %d %b %Y %H:%M:%S MSK')${NC}"
    echo -e "${YELLOW}📁 Проект: $PROJECT_DIR${NC}"
    echo -e "${CYAN}========================================================${NC}"
    echo ""
}

# Функция получения статуса агентов
get_agent_status() {
    local agents=("architect" "backend" "frontend" "testing" "devops" "analyst")
    local status=()
    
    for agent in "${agents[@]}"; do
        local pid=$(ps aux | grep -E ".*${agent}_agent.*sh" | grep -v grep | awk '{print $2}' | head -1)
        if [[ -n "$pid" ]]; then
            status+=("✅ $agent: работает (PID: $pid)")
        else
            status+=("❌ $agent: остановлен")
        fi
    done
    
    echo "${status[@]}"
}

# Функция проверки портов
check_ports() {
    local ports=()
    
    # Проверка Django API
    if lsof -i :8000 >/dev/null 2>&1; then
        ports+=("✅ Порт 8000: Django API активен")
    else
        ports+=("❌ Порт 8000: Django API не запущен")
    fi
    
    # Проверка React Dev Server
    if lsof -i :3000 >/dev/null 2>&1; then
        ports+=("✅ Порт 3000: React Dev Server активен")
    else
        ports+=("❌ Порт 3000: React Dev Server не запущен")
    fi
    
    echo "${ports[@]}"
}

# Функция подсчета прогресса TODO
get_todo_progress() {
    if [[ -f "$TODO_FILE" ]]; then
        local total=$(grep -c "^- \[" "$TODO_FILE" 2>/dev/null || echo "0")
        local completed=$(grep -c "^- \[x\]" "$TODO_FILE" 2>/dev/null || echo "0")
        local percentage=$((completed * 100 / (total + 1)))
        echo "$completed/$total задач выполнено ($percentage%)"
    else
        echo "Файл TODO не найден"
    fi
}

# Функция получения последних событий агентов
get_recent_events() {
    local events=()
    
    for log_file in "$LOG_DIR"/*.log; do
        if [[ -f "$log_file" ]]; then
            local agent=$(basename "$log_file" | cut -d'_' -f1)
            local last_line=$(tail -1 "$log_file" 2>/dev/null | sed 's/^[[:space:]]*//')
            if [[ -n "$last_line" ]]; then
                events+=("🤖 $agent: $last_line")
            fi
        fi
    done
    
    echo "${events[@]}"
}

# Функция проверки новых выполненных задач
check_new_completed_tasks() {
    if [[ -f "$TODO_FILE" ]]; then
        local current_count=$(grep -c "^- \[x\]" "$TODO_FILE" 2>/dev/null || echo "0")
        if [[ $current_count -gt $LAST_TODO_COUNT ]]; then
            local new_tasks=$((current_count - LAST_TODO_COUNT))
            echo -e "${GREEN}🎉 ВЫПОЛНЕНО НОВЫХ ЗАДАЧ: $new_tasks${NC}"
            LAST_TODO_COUNT=$current_count
            return 0
        fi
    fi
    return 1
}

# Функция вывода полного отчета
print_full_report() {
    clear_screen
    
    echo -e "${BOLD}📊 СТАТУС АГЕНТОВ${NC}"
    echo -e "${CYAN}----------------------------------------${NC}"
    local agent_status=($(get_agent_status))
    for status in "${agent_status[@]}"; do
        echo -e "  $status"
    done
    echo ""
    
    echo -e "${BOLD}🌐 ЗАНЯТЫЕ ПОРТЫ${NC}"
    echo -e "${CYAN}----------------${NC}"
    local port_status=($(check_ports))
    for port in "${port_status[@]}"; do
        echo -e "  $port"
    done
    echo ""
    
    echo -e "${BOLD}📈 ПРОГРЕСС РАЗРАБОТКИ${NC}"
    echo -e "${CYAN}----------------------${NC}"
    echo -e "  📋 TODO лист: $(get_todo_progress)"
    
    # Проверка новых выполненных задач
    if check_new_completed_tasks; then
        echo ""
    fi
    echo ""
    
    echo -e "${BOLD}⚡ АКТИВНЫЕ ПРОЦЕССЫ РАЗРАБОТКИ${NC}"
    echo -e "${CYAN}-------------------------------${NC}"
    
    # Django процессы
    local django_procs=$(ps aux | grep "manage.py runserver" | grep -v grep | wc -l)
    if [[ $django_procs -gt 0 ]]; then
        echo -e "  🐍 Django процессы: $django_procs активных"
    fi
    
    # Node процессы
    local node_procs=$(ps aux | grep "react-scripts" | grep -v grep | wc -l)
    if [[ $node_procs -gt 0 ]]; then
        echo -e "  ⚛️  React процессы: $node_procs активных"
    fi
    
    # Python тесты
    local test_procs=$(ps aux | grep "manage.py test" | grep -v grep | wc -l)
    if [[ $test_procs -gt 0 ]]; then
        echo -e "  🧪 Тестовые процессы: $test_procs активных"
    fi
    echo ""
    
    echo -e "${BOLD}📝 ПОСЛЕДНИЕ СОБЫТИЯ АГЕНТОВ${NC}"
    echo -e "${CYAN}----------------------------------------${NC}"
    local recent_events=($(get_recent_events))
    for event in "${recent_events[@]:0:10}"; do  # Показываем только последние 10 событий
        echo -e "  $event"
    done
    echo ""
    
    echo -e "${CYAN}========================================================${NC}"
    echo -e "${YELLOW}⏰ Следующий отчет через $((REPORT_INTERVAL / 60)) минут...${NC}"
    echo -e "${YELLOW}🔄 Нажмите Ctrl+C для выхода${NC}"
    echo -e "${CYAN}========================================================${NC}"
}

# Функция мониторинга логов в реальном времени
monitor_logs_realtime() {
    local log_pattern="$LOG_DIR/*.log"
    
    # Создаем временный файл для отслеживания изменений
    local temp_file=$(mktemp)
    
    # Инициализируем счетчики выполненных задач
    LAST_TODO_COUNT=$(grep -c "^- \[x\]" "$TODO_FILE" 2>/dev/null || echo "0")
    
    # Основной цикл мониторинга
    while true; do
        # Выводим полный отчет
        print_full_report
        
        # Ждем указанное время
        sleep $REPORT_INTERVAL
        
        # Проверяем изменения в логах
        for log_file in $log_pattern; do
            if [[ -f "$log_file" ]]; then
                local current_size=$(stat -c%s "$log_file" 2>/dev/null || echo "0")
                local last_size=$(cat "$temp_file" 2>/dev/null | grep "$log_file" | cut -d' ' -f2 || echo "0")
                
                if [[ $current_size -gt $last_size ]]; then
                    # Лог изменился - проверяем новые строки
                    local new_lines=$(tail -5 "$log_file" 2>/dev/null | grep -E "(✅|❌|🎉|⚠️|🔄)" | tail -1)
                    if [[ -n "$new_lines" ]]; then
                        echo -e "${GREEN}🆕 НОВОЕ СОБЫТИЕ:${NC} $new_lines"
                    fi
                    
                    # Обновляем размер в временном файле
                    echo "$log_file $current_size" >> "$temp_file.new"
                fi
            fi
        done
        
        # Обновляем временный файл
        mv "$temp_file.new" "$temp_file" 2>/dev/null || true
    done
}

# Обработка сигналов для корректного завершения
trap 'echo -e "\n${YELLOW}🛑 Мониторинг остановлен${NC}"; rm -f "$temp_file" 2>/dev/null; exit 0' INT TERM

# Запуск мониторинга
echo -e "${BOLD}${GREEN}🚀 Запуск улучшенного мониторинга агентов...${NC}"
echo -e "${YELLOW}📊 Отчеты каждые $((REPORT_INTERVAL / 60)) минут${NC}"
echo -e "${YELLOW}🆕 Уведомления о новых событиях в реальном времени${NC}"
echo ""

monitor_logs_realtime 