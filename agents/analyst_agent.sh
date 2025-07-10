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
