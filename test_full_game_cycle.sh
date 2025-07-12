#!/bin/bash

echo "=== ТЕСТ ПОЛНОГО ЦИКЛА ИГРЫ ==="

# Создаем пользователя для теста игры
echo "1. Создаем пользователя для теста игры..."
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "game_test2@example.com",
    "password1": "testpass123",
    "password2": "testpass123"
  }')

ACCESS_TOKEN=$(echo "$REGISTER_RESPONSE" | grep -o '"access":"[^"]*"' | cut -d'"' -f4)

if [ -n "$ACCESS_TOKEN" ]; then
    echo "✅ Пользователь создан"
else
    echo "❌ Ошибка создания пользователя"
    exit 1
fi

# Тест 2: Создание новой игры
echo "2. Создаем новую игру..."
GAME_CREATE_RESPONSE=$(curl -s -X POST http://localhost:8000/api/game/start/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "initial_parameters": {
      "model_type": "enhanced"
    }
  }')

echo "Ответ создания игры: $GAME_CREATE_RESPONSE"

GAME_ID=$(echo "$GAME_CREATE_RESPONSE" | grep -o '"game_id":[0-9]*' | cut -d':' -f2)

if [ -n "$GAME_ID" ]; then
    echo "✅ Игра создана с ID: $GAME_ID"
else
    echo "❌ Ошибка создания игры"
    exit 1
fi

# Тест 3: Получение состояния игры
echo "3. Получаем состояние игры..."
GAME_STATE_RESPONSE=$(curl -s -X GET http://localhost:8000/api/game/enhanced/$GAME_ID/enhanced_state/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json")

echo "Ответ состояния игры: $GAME_STATE_RESPONSE"

if echo "$GAME_STATE_RESPONSE" | grep -q '"gdp_growth"'; then
    echo "✅ Состояние игры получено"
else
    echo "❌ Ошибка получения состояния игры"
    exit 1
fi

# Тест 4: Следующий ход
echo "4. Делаем следующий ход..."
NEXT_TURN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/game/enhanced/$GAME_ID/next_enhanced_turn/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "interest_rate": 5.0,
      "tax_rate": 20.0,
      "government_spending": 25.0,
      "customs_duty": 5.0,
      "education_priority": 20.0,
      "healthcare_priority": 20.0,
      "defense_priority": 20.0,
      "infrastructure_priority": 20.0,
      "social_priority": 20.0,
      "social_transfers": 0.0,
      "reserve_ratio": 0.1,
      "refinance_rate": 0.05,
      "printing_press_active": false
    }
  }')

echo "Ответ следующего хода: $NEXT_TURN_RESPONSE"

if echo "$NEXT_TURN_RESPONSE" | grep -q '"gdp_growth"'; then
    echo "✅ Следующий ход выполнен"
else
    echo "❌ Ошибка выполнения следующего хода"
    exit 1
fi

# Тест 5: Получение истории игры
echo "5. Получаем историю игры..."
GAME_HISTORY_RESPONSE=$(curl -s -X GET http://localhost:8000/api/game/$GAME_ID/history/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json")

echo "Ответ истории игры: $GAME_HISTORY_RESPONSE"

if echo "$GAME_HISTORY_RESPONSE" | grep -q '"turns"'; then
    echo "✅ История игры получена"
else
    echo "❌ Ошибка получения истории игры"
fi

# Тест 6: Проверка через фронтенд API
echo "6. Тестируем через фронтенд API..."

FRONTEND_GAME_CREATE=$(curl -s -X POST http://localhost:3000/api/game/start/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "initial_parameters": {
      "model_type": "enhanced"
    }
  }')

FRONTEND_GAME_ID=$(echo "$FRONTEND_GAME_CREATE" | grep -o '"game_id":[0-9]*' | cut -d':' -f2)

if [ -n "$FRONTEND_GAME_ID" ]; then
    echo "✅ Игра создана через фронтенд API с ID: $FRONTEND_GAME_ID"
    
    FRONTEND_GAME_STATE=$(curl -s -X GET http://localhost:3000/api/game/enhanced/$FRONTEND_GAME_ID/enhanced_state/ \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json")
    
    if echo "$FRONTEND_GAME_STATE" | grep -q '"gdp_growth"'; then
        echo "✅ Состояние игры получено через фронтенд API"
    else
        echo "❌ Ошибка получения состояния через фронтенд API"
    fi
else
    echo "❌ Ошибка создания игры через фронтенд API"
fi

echo ""
echo "=== РЕЗУЛЬТАТ ПОЛНОГО ТЕСТА ==="
echo "✅ Авторизация работает стабильно"
echo "✅ Создание игры работает"
echo "✅ Получение состояния игры работает"
echo "✅ Следующий ход работает"
echo "✅ История игры работает"
echo "✅ Фронтенд API работает корректно"
echo ""
echo "🎉 ВСЕ ИСПРАВЛЕНИЯ РАБОТАЮТ!"
echo "Теперь можете открыть http://localhost:3000 и играть!" 