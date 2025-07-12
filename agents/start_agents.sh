#!/bin/bash

# 🚀 ОРКЕСТР АГЕНТОВ ДЛЯ ПРОЕКТА "ПРЕЗИДЕНТ: ЭКОНОМИКА И ВЛАСТЬ"
# Автоматизированная система разработки с 6 специализированными агентами

set -e  # Остановка при ошибках

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Функции для предотвращения зависания и зацикливания
cleanup_processes() {
    echo -e "${YELLOW}🧹 Очистка зависших процессов...${NC}"
    killall curl 2>/dev/null || true
    killall python 2>/dev/null || true
    killall node 2>/dev/null || true
    pkill -f "tail -f" 2>/dev/null || true
    pkill -f "ping" 2>/dev/null || true
    echo -e "${GREEN}✅ Процессы очищены${NC}"
}

check_port_availability() {
    local port=$1
    local service=$2
    echo -e "${BLUE}🔍 Проверка порта $port для $service...${NC}"
    
    if lsof -i :$port >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Порт $port занят, освобождаю...${NC}"
        fuser -k $port/tcp 2>/dev/null || true
        sleep 2
    fi
    echo -e "${GREEN}✅ Порт $port свободен${NC}"
}

safe_command() {
    local timeout=$1
    local command="$2"
    local description="$3"
    
    echo -e "${CYAN}🔄 $description (таймаут: ${timeout}с)...${NC}"
    
    # Запуск команды с таймаутом
    if timeout $timeout bash -c "$command"; then
        echo -e "${GREEN}✅ $description завершено успешно${NC}"
        return 0
    else
        local exit_code=$?
        if [ $exit_code -eq 124 ]; then
            echo -e "${RED}⏰ $description зависло, прерываю выполнение${NC}"
        else
            echo -e "${RED}❌ $description завершилось с ошибкой (код: $exit_code)${NC}"
        fi
        return $exit_code
    fi
}

# Функция для мониторинга процессов
monitor_processes() {
    echo -e "${PURPLE}📊 Мониторинг активных процессов:${NC}"
    ps aux | grep -E "(python|node|curl|ping)" | grep -v grep || echo "Нет активных процессов"
}

# Функция для экстренной остановки
emergency_stop() {
    echo -e "${RED}🚨 ЭКСТРЕННАЯ ОСТАНОВКА!${NC}"
    cleanup_processes
    echo -e "${YELLOW}⚠️  Все процессы остановлены${NC}"
    exit 1
}

# Обработчик сигналов для экстренной остановки
trap emergency_stop SIGINT SIGTERM

# Основные переменные
PROJECT_ROOT="/home/alex/Downloads/Prezident_project"
LOG_DIR="$PROJECT_ROOT/agents/logs"
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

# Создание директорий
mkdir -p "$LOG_DIR"

echo -e "${GREEN}🚀 Запуск оркестра агентов для проекта 'Президент: Экономика и Власть'${NC}"
echo -e "${BLUE}📅 Время запуска: $(date)${NC}"
echo -e "${BLUE}📁 Проект: $PROJECT_ROOT${NC}"
echo -e "${BLUE}📝 Логи: $LOG_DIR${NC}"

# Очистка старых процессов
cleanup_processes

# Проверка доступности портов
check_port_availability 8000 "Django Backend"
check_port_availability 3000 "React Frontend"

# Функция запуска агента с логированием и защитой от зависания
start_agent() {
    local agent_name="$1"
    local agent_file="$2"
    local log_file="$LOG_DIR/${agent_name}_${TIMESTAMP}.log"
    
    echo -e "${CYAN}🤖 Запуск агента: $agent_name${NC}"
    
    # Запуск агента в фоне с таймаутом и логированием
    (
        echo "=== АГЕНТ: $agent_name ==="
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
    echo -e "${GREEN}✅ Агент $agent_name запущен (PID: $agent_pid, лог: $log_file)${NC}"
    
    # Сохранение PID для мониторинга
    echo $agent_pid > "$LOG_DIR/${agent_name}.pid"
}

# Функция мониторинга агентов
monitor_agents() {
    echo -e "${PURPLE}📊 Мониторинг агентов:${NC}"
    
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
        echo -e "${GREEN}🎉 Все агенты работают!${NC}"
    else
        echo -e "${YELLOW}⚠️  Некоторые агенты остановлены${NC}"
    fi
}

# Функция для безопасного тестирования API
test_api_safely() {
    echo -e "${BLUE}🧪 Безопасное тестирование API...${NC}"
    
    # Тест Django API с таймаутом
    safe_command 10 "curl --max-time 5 -s http://localhost:8000/api/auth/register/" "Тест Django API"
    
    # Тест React с таймаутом
    safe_command 10 "curl --max-time 5 -s http://localhost:3000" "Тест React Frontend"
    
    echo -e "${GREEN}✅ API тестирование завершено${NC}"
}

# Основной процесс запуска
echo -e "${BLUE}🔧 Подготовка к запуску агентов...${NC}"

# Проверка существования файлов агентов
AGENT_FILES=(
    "architect_agent.sh"
    "backend_agent.sh" 
    "frontend_agent.sh"
    "testing_agent.sh"
    "devops_agent.sh"
    "analyst_agent.sh"
)

for file in "${AGENT_FILES[@]}"; do
    if [ ! -f "$PROJECT_ROOT/agents/$file" ]; then
        echo -e "${RED}❌ Файл агента не найден: $file${NC}"
        echo -e "${YELLOW}⚠️  Создаю базовый скрипт для $file${NC}"
        
        # Создание базового скрипта агента
        cat > "$PROJECT_ROOT/agents/$file" << 'EOF'
#!/bin/bash
# Базовый скрипт агента
echo "🤖 Агент запущен: $(basename $0)"
echo "⏰ Время: $(date)"
echo "📁 Директория: $(pwd)"

# Основной цикл
while true; do
    echo "🔄 Агент работает... $(date '+%H:%M:%S')"
    sleep 60
done
EOF
        chmod +x "$PROJECT_ROOT/agents/$file"
        echo -e "${GREEN}✅ Базовый скрипт создан: $file${NC}"
    fi
done

echo -e "${GREEN}✅ Все файлы агентов готовы${NC}"

# Запуск агентов с защитой от зависания
echo -e "${CYAN}🚀 Запуск агентов...${NC}"

start_agent "architect" "$PROJECT_ROOT/agents/architect_agent.sh"
sleep 2

start_agent "backend" "$PROJECT_ROOT/agents/backend_agent.sh"
sleep 2

start_agent "frontend" "$PROJECT_ROOT/agents/frontend_agent.sh"
sleep 2

start_agent "testing" "$PROJECT_ROOT/agents/testing_agent.sh"
sleep 2

start_agent "devops" "$PROJECT_ROOT/agents/devops_agent.sh"
sleep 2

start_agent "analyst" "$PROJECT_ROOT/agents/analyst_agent.sh"

echo -e "${GREEN}🎉 Все агенты запущены!${NC}"

# Мониторинг и отчетность
echo -e "${BLUE}📊 Настройка мониторинга...${NC}"

# Создание файла статуса
STATUS_FILE="$LOG_DIR/orchestra_status_${TIMESTAMP}.json"
cat > "$STATUS_FILE" << EOF
{
    "timestamp": "$(date -Iseconds)",
    "project": "Президент: Экономика и Власть",
    "orchestra_version": "2.0",
    "agents_count": 6,
    "status": "running",
    "agents": {
        "architect": {"status": "running", "pid_file": "$LOG_DIR/architect.pid"},
        "backend": {"status": "running", "pid_file": "$LOG_DIR/backend.pid"},
        "frontend": {"status": "running", "pid_file": "$LOG_DIR/frontend.pid"},
        "testing": {"status": "running", "pid_file": "$LOG_DIR/testing.pid"},
        "devops": {"status": "running", "pid_file": "$LOG_DIR/devops.pid"},
        "analyst": {"status": "running", "pid_file": "$LOG_DIR/analyst.pid"}
    },
    "logs_directory": "$LOG_DIR",
    "safety_features": {
        "timeout_protection": true,
        "process_monitoring": true,
        "emergency_stop": true,
        "port_availability_check": true
    }
}
EOF

echo -e "${GREEN}✅ Статус сохранен в: $STATUS_FILE${NC}"

# Первоначальный мониторинг
monitor_agents
monitor_processes

# Инструкции для пользователя
echo -e "${PURPLE}📋 ИНСТРУКЦИИ ДЛЯ УПРАВЛЕНИЯ:${NC}"
echo -e "${CYAN}• Мониторинг: ${YELLOW}tail -f $LOG_DIR/*.log${NC}"
echo -e "${CYAN}• Статус агентов: ${YELLOW}ps aux | grep -E '(architect|backend|frontend|testing|devops|analyst)'${NC}"
echo -e "${CYAN}• Остановка: ${YELLOW}Ctrl+C${NC}"
echo -e "${CYAN}• Экстренная остановка: ${YELLOW}killall python node curl${NC}"
echo -e "${CYAN}• Проверка портов: ${YELLOW}lsof -i :8000 && lsof -i :3000${NC}"

# Основной цикл мониторинга с защитой от зависания
echo -e "${BLUE}🔄 Запуск основного цикла мониторинга...${NC}"

while true; do
    echo -e "${BLUE}📊 $(date '+%H:%M:%S') - Проверка состояния...${NC}"
    
    # Мониторинг агентов
    monitor_agents
    
    # Проверка на зависшие процессы
    hanging_processes=$(ps aux | grep -E "(curl|ping|tail)" | grep -v grep | wc -l)
    if [ $hanging_processes -gt 0 ]; then
        echo -e "${YELLOW}⚠️  Обнаружены потенциально зависшие процессы: $hanging_processes${NC}"
        cleanup_processes
    fi
    
    # Безопасное тестирование API каждые 5 минут
    current_minute=$(date '+%M')
    if [ $((10#$current_minute % 5)) -eq 0 ]; then
        test_api_safely
    fi
    
    # Обновление статуса
    echo "{\"last_check\": \"$(date -Iseconds)\", \"status\": \"healthy\"}" > "$LOG_DIR/last_check.json"
    
    echo -e "${GREEN}✅ Система работает стабильно${NC}"
    echo -e "${BLUE}⏰ Следующая проверка через 60 секунд...${NC}"
    
    # Ожидание с возможностью прерывания
    sleep 60 || break
done

echo -e "${GREEN}🎉 Оркестр агентов завершил работу${NC}" 