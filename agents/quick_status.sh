#!/bin/bash

# ⚡ БЫСТРЫЙ СТАТУС АГЕНТОВ И ПРОГРЕССА
# Быстрый просмотр текущего состояния

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

echo -e "${BOLD}${CYAN}⚡ БЫСТРЫЙ СТАТУС ПРОЕКТА${NC}"
echo -e "${CYAN}==============================${NC}"
echo -e "${YELLOW}📅 Время: $(date '+%H:%M:%S')${NC}"
echo ""

# Статус агентов
echo -e "${BOLD}🤖 СТАТУС АГЕНТОВ:${NC}"
agents=("architect" "backend" "frontend" "testing" "devops" "analyst")
for agent in "${agents[@]}"; do
    pid=$(ps aux | grep -E ".*${agent}_agent.*sh" | grep -v grep | awk '{print $2}' | head -1)
    if [[ -n "$pid" ]]; then
        echo -e "  ✅ $agent: работает (PID: $pid)"
    else
        echo -e "  ❌ $agent: остановлен"
    fi
done
echo ""

# Статус портов
echo -e "${BOLD}🌐 СТАТУС ПОРТОВ:${NC}"
if lsof -i :8000 >/dev/null 2>&1; then
    echo -e "  ✅ Порт 8000: Django API активен"
else
    echo -e "  ❌ Порт 8000: Django API не запущен"
fi

if lsof -i :3000 >/dev/null 2>&1; then
    echo -e "  ✅ Порт 3000: React Dev Server активен"
else
    echo -e "  ❌ Порт 3000: React Dev Server не запущен"
fi
echo ""

# Прогресс TODO
echo -e "${BOLD}📈 ПРОГРЕСС РАЗРАБОТКИ:${NC}"
if [[ -f "$TODO_FILE" ]]; then
    total=$(grep -c "^- \[" "$TODO_FILE" 2>/dev/null || echo "0")
    completed=$(grep -c "^- \[x\]" "$TODO_FILE" 2>/dev/null || echo "0")
    pending=$((total - completed))
    percentage=$((completed * 100 / (total + 1)))
    
    echo -e "  📋 Всего задач: $total"
    echo -e "  ✅ Выполнено: $completed"
    echo -e "  ⏳ Осталось: $pending"
    echo -e "  📈 Прогресс: $percentage%"
else
    echo -e "  ❌ Файл TODO не найден"
fi
echo ""

# Активные процессы
echo -e "${BOLD}⚡ АКТИВНЫЕ ПРОЦЕССЫ:${NC}"
django_procs=$(ps aux | grep "manage.py runserver" | grep -v grep | wc -l)
node_procs=$(ps aux | grep "react-scripts" | grep -v grep | wc -l)
test_procs=$(ps aux | grep "manage.py test" | grep -v grep | wc -l)

if [[ $django_procs -gt 0 ]]; then
    echo -e "  🐍 Django: $django_procs процессов"
fi
if [[ $node_procs -gt 0 ]]; then
    echo -e "  ⚛️  React: $node_procs процессов"
fi
if [[ $test_procs -gt 0 ]]; then
    echo -e "  🧪 Тесты: $test_procs процессов"
fi
echo ""

# Последние события
echo -e "${BOLD}📝 ПОСЛЕДНИЕ СОБЫТИЯ:${NC}"
log_dir="$PROJECT_DIR/agents/logs"
if [[ -d "$log_dir" ]]; then
    for log_file in "$log_dir"/*.log; do
        if [[ -f "$log_file" ]]; then
            agent=$(basename "$log_file" | cut -d'_' -f1)
            last_line=$(tail -1 "$log_file" 2>/dev/null | sed 's/^[[:space:]]*//' | cut -c1-50)
            if [[ -n "$last_line" ]]; then
                echo -e "  🤖 $agent: $last_line..."
            fi
        fi
    done
fi
echo ""

echo -e "${CYAN}==============================${NC}"
echo -e "${YELLOW}💡 Для подробного мониторинга: ./agents/enhanced_monitor.sh${NC}"
echo -e "${YELLOW}🔔 Для уведомлений о задачах: ./agents/task_notifier.sh${NC}" 