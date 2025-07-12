#!/bin/bash

# 🚀 БЫСТРЫЙ ПРОСМОТР ЛОГОВ АГЕНТОВ
# Использование: ./quick_logs.sh [agent_name]

AGENT=${1:-"all"}

echo "📝 ЛОГИ АГЕНТОВ - $(date '+%H:%M:%S')"
echo "====================================="
echo ""

if [ "$AGENT" = "all" ]; then
    # Показываем последние логи всех агентов
    agents=("architect" "backend" "frontend" "testing" "devops" "analyst")
    
    for agent in "${agents[@]}"; do
        latest_log=$(ls -t agents/logs/${agent}_*.log 2>/dev/null | head -1)
        if [ -n "$latest_log" ]; then
            echo "🤖 $agent (последние 3 строки):"
            echo "--------------------------------"
            tail -3 "$latest_log" | sed 's/^/  /'
            echo ""
        fi
    done
else
    # Показываем логи конкретного агента
    latest_log=$(ls -t agents/logs/${AGENT}_*.log 2>/dev/null | head -1)
    if [ -n "$latest_log" ]; then
        echo "🤖 $AGENT (последние 10 строк):"
        echo "--------------------------------"
        tail -10 "$latest_log"
    else
        echo "❌ Логи для агента '$AGENT' не найдены"
    fi
fi 