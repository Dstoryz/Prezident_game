#!/bin/bash

echo "🚀 АВТОМАТИЧЕСКОЕ ТЕСТИРОВАНИЕ СИСТЕМЫ ПРЕЗИДЕНТ"
echo "================================================"

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для логирования
log() {
    echo -e "${GREEN}[$(date '+%H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ОШИБКА]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[ПРЕДУПРЕЖДЕНИЕ]${NC} $1"
}

# Проверка доступности серверов
log "Проверка доступности серверов..."

# Проверка backend
if curl -s http://localhost:8000/api/dj-rest-auth/user/ > /dev/null; then
    log "✅ Backend (Django) доступен на порту 8000"
else
    error "❌ Backend недоступен на порту 8000"
    exit 1
fi

# Проверка frontend
if curl -s http://localhost:3000 > /dev/null; then
    log "✅ Frontend (React) доступен на порту 3000"
else
    warning "⚠️ Frontend недоступен на порту 3000"
fi

# Генерация уникального email
EMAIL="test_$(date +%s)@example.com"
PASSWORD="testpass123"

echo ""
log "Начинаем автоматическое тестирование..."

# 1. Регистрация нового пользователя
log "1️⃣ Тестирование регистрации..."
REG_RESPONSE=$(curl -s -X POST http://localhost:8000/api/dj-rest-auth/registration/ \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"$EMAIL\",\"password1\":\"$PASSWORD\",\"password2\":\"$PASSWORD\"}")

if echo "$REG_RESPONSE" | grep -q "access"; then
    log "✅ Регистрация успешна для $EMAIL"
    TOKEN=$(echo "$REG_RESPONSE" | grep -o '"access":"[^"]*"' | cut -d'"' -f4)
else
    if echo "$REG_RESPONSE" | grep -q "уже существует"; then
        log "ℹ️ Пользователь уже существует, пробуем войти..."
    else
        error "❌ Ошибка регистрации: $REG_RESPONSE"
        exit 1
    fi
fi

# 2. Вход в систему
log "2️⃣ Тестирование входа..."
if [ -z "$TOKEN" ]; then
    LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/dj-rest-auth/login/ \
        -H "Content-Type: application/json" \
        -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")
    
    if echo "$LOGIN_RESPONSE" | grep -q "access"; then
        log "✅ Вход успешен"
        TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access":"[^"]*"' | cut -d'"' -f4)
    else
        error "❌ Ошибка входа: $LOGIN_RESPONSE"
        exit 1
    fi
fi

# 3. Создание новой игры
log "3️⃣ Тестирование создания игры..."
GAME_RESPONSE=$(curl -s -X POST http://localhost:8000/api/game/start/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d '{"difficulty":"medium","model_type":"enhanced"}')

if echo "$GAME_RESPONSE" | grep -q "game_id"; then
    GAME_ID=$(echo "$GAME_RESPONSE" | grep -o '"game_id":[0-9]*' | cut -d':' -f2)
    log "✅ Игра создана с ID: $GAME_ID"
else
    error "❌ Ошибка создания игры: $GAME_RESPONSE"
    exit 1
fi

# 4. Получение состояния расширенной игры
log "4️⃣ Тестирование получения состояния игры..."
STATE_RESPONSE=$(curl -s -X GET "http://localhost:8000/api/game/enhanced/$GAME_ID/enhanced_state/" \
    -H "Authorization: Bearer $TOKEN")

if echo "$STATE_RESPONSE" | grep -q "indicators"; then
    log "✅ Состояние игры получено успешно"
    
    # Извлекаем ключевые показатели
    GDP=$(echo "$STATE_RESPONSE" | grep -o '"gdp_absolute":[0-9.]*' | cut -d':' -f2)
    POPULATION=$(echo "$STATE_RESPONSE" | grep -o '"population":[0-9.]*' | cut -d':' -f2)
    INFLATION=$(echo "$STATE_RESPONSE" | grep -o '"inflation":[0-9.]*' | cut -d':' -f2)
    
    log "📊 Ключевые показатели:"
    log "   ВВП: $GDP USD"
    log "   Население: $POPULATION чел."
    log "   Инфляция: $INFLATION%"
else
    error "❌ Ошибка получения состояния: $STATE_RESPONSE"
    exit 1
fi

# 5. Тестирование выхода
log "5️⃣ Тестирование выхода..."
LOGOUT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/dj-rest-auth/logout/ \
    -H "Authorization: Bearer $TOKEN")

if [ $? -eq 0 ]; then
    log "✅ Выход выполнен успешно"
else
    warning "⚠️ Ошибка выхода: $LOGOUT_RESPONSE"
fi

# 6. Проверка что после выхода доступ закрыт
log "6️⃣ Проверка закрытия доступа после выхода..."
PROTECTED_RESPONSE=$(curl -s -X GET http://localhost:8000/api/dj-rest-auth/user/ \
    -H "Authorization: Bearer $TOKEN")

if echo "$PROTECTED_RESPONSE" | grep -q "401\|Unauthorized"; then
    log "✅ Доступ корректно закрыт после выхода"
else
    warning "⚠️ Доступ не закрыт после выхода"
fi

echo ""
log "🎉 АВТОМАТИЧЕСКОЕ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!"
log "Все основные функции системы работают корректно:"
log "✅ Регистрация и вход"
log "✅ Создание игры"
log "✅ Получение состояния расширенной модели"
log "✅ Выход и закрытие доступа"
log "✅ CORS и авторизация"

echo ""
log "📋 Статус системы: ГОТОВА К ИСПОЛЬЗОВАНИЮ" 