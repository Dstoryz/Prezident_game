#!/bin/bash

# 🎯 МОНИТОРИНГ АГЕНТОВ В РЕАЛЬНОМ ВРЕМЕНИ
# Автор: AI Assistant
# Дата: 12.07.2025

echo "🎯 МОНИТОРИНГ АГЕНТОВ - РЕАЛЬНОЕ ВРЕМЯ"
echo "========================================"
echo ""

# Функция для получения статуса агентов
get_agent_status() {
    echo "📊 СТАТУС АГЕНТОВ ($(date '+%H:%M:%S'))"
    echo "----------------------------------------"
    
    # Проверяем каждый агент
    agents=("architect" "backend" "frontend" "testing" "devops" "analyst")
    
    for agent in "${agents[@]}"; do
        if pgrep -f "${agent}_agent.sh" > /dev/null; then
            pid=$(pgrep -f "${agent}_agent.sh" | head -1)
            echo "✅ $agent: работает (PID: $pid)"
        else
            echo "❌ $agent: остановлен"
        fi
    done
    echo ""
}

# Функция для показа последних логов
show_recent_logs() {
    echo "📝 ПОСЛЕДНИЕ СОБЫТИЯ (последние 5 строк каждого агента)"
    echo "--------------------------------------------------------"
    
    agents=("architect" "backend" "frontend" "testing" "devops" "analyst")
    
    for agent in "${agents[@]}"; do
        latest_log=$(ls -t agents/logs/${agent}_*.log 2>/dev/null | head -1)
        if [ -n "$latest_log" ]; then
            echo "🤖 $agent:"
            tail -5 "$latest_log" | sed 's/^/  /'
            echo ""
        fi
    done
}

# Функция для показа активных процессов
show_active_processes() {
    echo "⚡ АКТИВНЫЕ ПРОЦЕССЫ РАЗРАБОТКИ"
    echo "-------------------------------"
    
    # Django процессы
    django_pids=$(pgrep -f "manage.py" 2>/dev/null)
    if [ -n "$django_pids" ]; then
        echo "🐍 Django процессы:"
        for pid in $django_pids; do
            ps -p $pid -o pid,cmd --no-headers | sed 's/^/  /'
        done
        echo ""
    fi
    
    # Node.js процессы
    node_pids=$(pgrep -f "react-scripts\|node.*build" 2>/dev/null)
    if [ -n "$node_pids" ]; then
        echo "🟢 Node.js процессы:"
        for pid in $node_pids; do
            ps -p $pid -o pid,cmd --no-headers | sed 's/^/  /'
        done
        echo ""
    fi
    
    # Тестовые процессы
    test_pids=$(pgrep -f "test.*game" 2>/dev/null)
    if [ -n "$test_pids" ]; then
        echo "🧪 Тестовые процессы:"
        for pid in $test_pids; do
            ps -p $pid -o pid,cmd --no-headers | sed 's/^/  /'
        done
        echo ""
    fi
}

# Функция для показа портов
show_ports() {
    echo "🌐 ЗАНЯТЫЕ ПОРТЫ"
    echo "----------------"
    
    # Проверяем порт 8000 (Django)
    if lsof -i :8000 >/dev/null 2>&1; then
        echo "✅ Порт 8000: Django API активен"
    else
        echo "❌ Порт 8000: Django API не запущен"
    fi
    
    # Проверяем порт 3000 (React)
    if lsof -i :3000 >/dev/null 2>&1; then
        echo "✅ Порт 3000: React Dev Server активен"
    else
        echo "❌ Порт 3000: React Dev Server не запущен"
    fi
    echo ""
}

# Функция для показа прогресса
show_progress() {
    echo "📈 ПРОГРЕСС РАЗРАБОТКИ"
    echo "----------------------"
    
    # Проверяем TODO лист
    if [ -f "TODO_CHECKLIST.md" ]; then
        total_tasks=$(grep -c "^- \[ \]" TODO_CHECKLIST.md 2>/dev/null || echo "0")
        completed_tasks=$(grep -c "^- \[x\]" TODO_CHECKLIST.md 2>/dev/null || echo "0")
        
        if [ "$total_tasks" -gt 0 ]; then
            progress=$((completed_tasks * 100 / total_tasks))
            echo "📋 TODO лист: $completed_tasks/$total_tasks задач выполнено ($progress%)"
        else
            echo "📋 TODO лист: задачи не найдены"
        fi
    fi
    
    # Проверяем статус сборки
    if [ -d "frontend/build" ]; then
        echo "🏗️ Frontend: production build готов"
    else
        echo "🏗️ Frontend: сборка в процессе..."
    fi
    
    # Проверяем миграции
    if [ -f "backend/game/migrations/0001_initial.py" ]; then
        echo "🗄️ База данных: миграции применены"
    else
        echo "🗄️ База данных: миграции не найдены"
    fi
    echo ""
}

# Основной цикл мониторинга
main() {
    clear
    echo "🎯 МОНИТОРИНГ АГЕНТОВ - РЕАЛЬНОЕ ВРЕМЯ"
    echo "========================================"
    echo "Нажмите Ctrl+C для выхода"
    echo ""
    
    while true; do
        get_agent_status
        show_ports
        show_progress
        show_active_processes
        show_recent_logs
        
        echo "🔄 Обновление через 30 секунд... ($(date '+%H:%M:%S'))"
        echo "========================================"
        sleep 30
        clear
        echo "🎯 МОНИТОРИНГ АГЕНТОВ - РЕАЛЬНОЕ ВРЕМЯ"
        echo "========================================"
        echo "Нажмите Ctrl+C для выхода"
        echo ""
    done
}

# Запуск мониторинга
main 