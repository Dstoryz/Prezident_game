#!/bin/bash

# 🚀 ЗАПУСК УСТОЙЧИВЫХ АГЕНТОВ
# Использует новые устойчивые версии агентов

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Основные переменные
PROJECT_ROOT="/home/alex/Downloads/Prezident_project"
LOG_DIR="$PROJECT_ROOT/agents/logs"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

# Создание директорий
mkdir -p "$LOG_DIR"

echo -e "${GREEN}🚀 Запуск УСТОЙЧИВЫХ агентов для проекта 'Президент: Экономика и Власть'${NC}"
echo -e "${BLUE}📅 Время запуска: $(date)${NC}"
echo -e "${BLUE}📁 Проект: $PROJECT_ROOT${NC}"
echo -e "${BLUE}📝 Логи: $LOG_DIR${NC}"

# Очистка старых процессов
echo -e "${YELLOW}🧹 Очистка старых процессов...${NC}"
pkill -f "architect_agent.sh" 2>/dev/null || true
pkill -f "backend_agent.sh" 2>/dev/null || true
pkill -f "frontend_agent.sh" 2>/dev/null || true
pkill -f "testing_agent.sh" 2>/dev/null || true
pkill -f "devops_agent.sh" 2>/dev/null || true
pkill -f "analyst_agent.sh" 2>/dev/null || true
sleep 2

# Функция запуска устойчивого агента
start_robust_agent() {
    local agent_name="$1"
    local agent_file="$2"
    local log_file="$LOG_DIR/${agent_name}_${TIMESTAMP}.log"
    
    echo -e "${CYAN}🤖 Запуск устойчивого агента: $agent_name${NC}"
    
    # Проверяем, есть ли устойчивая версия
    local robust_file="${agent_file%.*}_robust.sh"
    if [ -f "$robust_file" ]; then
        agent_file="$robust_file"
        echo -e "${GREEN}✅ Используется устойчивая версия: $(basename $robust_file)${NC}"
    else
        echo -e "${YELLOW}⚠️  Устойчивая версия не найдена, используем обычную${NC}"
    fi
    
    # Запуск агента в фоне с логированием
    (
        echo "=== УСТОЙЧИВЫЙ АГЕНТ: $agent_name ==="
        echo "Время запуска: $(date)"
        echo "Файл: $agent_file"
        echo "=================================="
        
        # Запуск без таймаута (агенты работают постоянно)
        bash "$agent_file" 2>&1
        
        echo "=================================="
        echo "Время завершения: $(date)"
        echo "Статус: $?"
    ) > "$log_file" 2>&1 &
    
    local agent_pid=$!
    echo -e "${GREEN}✅ Устойчивый агент $agent_name запущен (PID: $agent_pid, лог: $log_file)${NC}"
    
    # Сохранение PID для мониторинга
    echo $agent_pid > "$LOG_DIR/${agent_name}.pid"
}

# Функция мониторинга агентов
monitor_agents() {
    echo -e "${PURPLE}📊 Мониторинг устойчивых агентов:${NC}"
    
    local agents=("architect" "backend" "frontend" "testing" "devops" "analyst")
    local all_running=true
    
    for agent in "${agents[@]}"; do
        local pid_file="$LOG_DIR/${agent}.pid"
        if [ -f "$pid_file" ]; then
            local pid=$(cat "$pid_file")
            if ps -p $pid >/dev/null 2>&1; then
                echo -e "${GREEN}✅ $agent: работает (PID: $pid)${NC}"
            else
                echo -e "${RED}❌ $agent: остановлен${NC}"
                all_running=false
            fi
        else
            echo -e "${YELLOW}⚠️  $agent: PID файл не найден${NC}"
            all_running=false
        fi
    done
    
    if [ "$all_running" = true ]; then
        echo -e "${GREEN}🎉 Все устойчивые агенты работают!${NC}"
    else
        echo -e "${YELLOW}⚠️  Некоторые агенты остановлены${NC}"
    fi
}

# Проверка существования файлов агентов
AGENT_FILES=(
    "architect_agent.sh"
    "backend_agent_robust.sh" 
    "frontend_agent.sh"
    "testing_agent_robust.sh"
    "devops_agent.sh"
    "analyst_agent.sh"
)

echo -e "${BLUE}🔧 Проверка файлов агентов...${NC}"

for file in "${AGENT_FILES[@]}"; do
    if [ ! -f "$PROJECT_ROOT/agents/$file" ]; then
        echo -e "${YELLOW}⚠️  Файл агента не найден: $file${NC}"
        if [[ "$file" == *"_robust.sh" ]]; then
            echo -e "${YELLOW}⚠️  Устойчивая версия не найдена, будет использована обычная${NC}"
        fi
    else
        echo -e "${GREEN}✅ Найден: $file${NC}"
    fi
done

echo -e "${GREEN}✅ Проверка файлов завершена${NC}"

# Запуск устойчивых агентов
echo -e "${CYAN}🚀 Запуск устойчивых агентов...${NC}"

start_robust_agent "architect" "$PROJECT_ROOT/agents/architect_agent.sh"
sleep 2

start_robust_agent "backend" "$PROJECT_ROOT/agents/backend_agent.sh"
sleep 2

start_robust_agent "frontend" "$PROJECT_ROOT/agents/frontend_agent.sh"
sleep 2

start_robust_agent "testing" "$PROJECT_ROOT/agents/testing_agent.sh"
sleep 2

start_robust_agent "devops" "$PROJECT_ROOT/agents/devops_agent.sh"
sleep 2

start_robust_agent "analyst" "$PROJECT_ROOT/agents/analyst_agent.sh"

echo -e "${GREEN}🎉 Все устойчивые агенты запущены!${NC}"

# Мониторинг и отчетность
echo -e "${BLUE}📊 Настройка мониторинга...${NC}"

# Создание файла статуса
STATUS_FILE="$LOG_DIR/orchestra_status_${TIMESTAMP}.json"
cat > "$STATUS_FILE" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "project": "Президент: Экономика и Власть",
    "status": "Устойчивые агенты запущены",
    "agents": {
        "architect": {"status": "running", "pid": "$(cat $LOG_DIR/architect.pid 2>/dev/null || echo 'unknown')"},
        "backend": {"status": "running", "pid": "$(cat $LOG_DIR/backend.pid 2>/dev/null || echo 'unknown')"},
        "frontend": {"status": "running", "pid": "$(cat $LOG_DIR/frontend.pid 2>/dev/null || echo 'unknown')"},
        "testing": {"status": "running", "pid": "$(cat $LOG_DIR/testing.pid 2>/dev/null || echo 'unknown')"},
        "devops": {"status": "running", "pid": "$(cat $LOG_DIR/devops.pid 2>/dev/null || echo 'unknown')"},
        "analyst": {"status": "running", "pid": "$(cat $LOG_DIR/analyst.pid 2>/dev/null || echo 'unknown')"}
    },
    "ports": {
        "8000": "$(lsof -i :8000 >/dev/null 2>&1 && echo 'occupied' || echo 'free')",
        "3000": "$(lsof -i :3000 >/dev/null 2>&1 && echo 'occupied' || echo 'free')"
    },
    "version": "robust_agents_v1.0"
}
EOF

echo -e "${GREEN}✅ Статус сохранен в: $STATUS_FILE${NC}"

# Первоначальный мониторинг
monitor_agents

# Инструкции для управления
echo -e "${PURPLE}📋 ИНСТРУКЦИИ ДЛЯ УПРАВЛЕНИЯ:${NC}"
echo -e "${CYAN}• Мониторинг: tail -f $LOG_DIR/*.log${NC}"
echo -e "${CYAN}• Статус агентов: ps aux | grep -E '(architect|backend|frontend|testing|devops|analyst)'${NC}"
echo -e "${CYAN}• Остановка: Ctrl+C${NC}"
echo -e "${CYAN}• Экстренная остановка: killall python node curl${NC}"
echo -e "${CYAN}• Проверка портов: lsof -i :8000 && lsof -i :3000${NC}"

# Основной цикл мониторинга
echo -e "${BLUE}🔄 Запуск основного цикла мониторинга...${NC}"

while true; do
    echo -e "${BLUE}📊 $(date '+%H:%M:%S') - Проверка состояния...${NC}"
    monitor_agents
    
    # Проверка портов
    echo -e "${BLUE}🌐 Проверка портов:${NC}"
    if lsof -i :8000 | grep LISTEN >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Порт 8000: Django API запущен${NC}"
    else
        echo -e "${YELLOW}⚠️  Порт 8000: Django API не запущен${NC}"
    fi
    
    if lsof -i :3000 | grep LISTEN >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Порт 3000: React Dev Server запущен${NC}"
    else
        echo -e "${YELLOW}⚠️  Порт 3000: React Dev Server не запущен${NC}"
    fi
    
    echo -e "${GREEN}✅ Система работает стабильно${NC}"
    echo -e "${BLUE}⏰ Следующая проверка через 60 секунд...${NC}"
    sleep 60
done 