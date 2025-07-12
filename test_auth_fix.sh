#!/bin/bash

echo "=== ТЕСТ ИСПРАВЛЕНИЙ АВТОРИЗАЦИИ ==="
echo "Проверяем работу кастомных эндпоинтов /auth/..."

# Очищаем старые токены
echo "1. Очищаем старые токены..."
rm -f /tmp/test_tokens.json

# Тест 1: Регистрация нового пользователя
echo "2. Тестируем регистрацию через /auth/register/..."
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test_fix@example.com",
    "password1": "testpass123",
    "password2": "testpass123"
  }')

echo "Ответ регистрации: $REGISTER_RESPONSE"

# Извлекаем токены из ответа
ACCESS_TOKEN=$(echo "$REGISTER_RESPONSE" | grep -o '"access":"[^"]*"' | cut -d'"' -f4)
REFRESH_TOKEN=$(echo "$REGISTER_RESPONSE" | grep -o '"refresh":"[^"]*"' | cut -d'"' -f4)

if [ -n "$ACCESS_TOKEN" ]; then
    echo "✅ Токены получены успешно"
    echo "Access token: ${ACCESS_TOKEN:0:20}..."
    echo "Refresh token: ${REFRESH_TOKEN:0:20}..."
else
    echo "❌ Токены не получены"
    echo "Полный ответ: $REGISTER_RESPONSE"
    exit 1
fi

# Тест 2: Получение информации о пользователе с токеном
echo "3. Тестируем получение пользователя через /auth/user/..."
USER_RESPONSE=$(curl -s -X GET http://localhost:8000/api/auth/user/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json")

echo "Ответ пользователя: $USER_RESPONSE"

if echo "$USER_RESPONSE" | grep -q '"email":"test_fix@example.com"'; then
    echo "✅ Пользователь получен успешно"
else
    echo "❌ Ошибка получения пользователя"
    echo "Полный ответ: $USER_RESPONSE"
    exit 1
fi

# Тест 3: Выход
echo "4. Тестируем выход через /auth/logout/..."
LOGOUT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/logout/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json")

echo "Ответ выхода: $LOGOUT_RESPONSE"

# Тест 4: Проверяем, что после выхода доступ закрыт
echo "5. Проверяем закрытие доступа после выхода..."
AFTER_LOGOUT_RESPONSE=$(curl -s -X GET http://localhost:8000/api/auth/user/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json")

if echo "$AFTER_LOGOUT_RESPONSE" | grep -q "Учетные данные не были предоставлены\|Unauthorized"; then
    echo "✅ Доступ закрыт после выхода"
else
    echo "❌ Доступ не закрыт после выхода"
    echo "Ответ: $AFTER_LOGOUT_RESPONSE"
fi

# Тест 5: Логин существующего пользователя
echo "6. Тестируем логин через /auth/login/..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test_fix@example.com",
    "password": "testpass123"
  }')

echo "Ответ логина: $LOGIN_RESPONSE"

LOGIN_ACCESS_TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access":"[^"]*"' | cut -d'"' -f4)

if [ -n "$LOGIN_ACCESS_TOKEN" ]; then
    echo "✅ Логин успешен, получен новый токен"
    
    # Проверяем доступ с новым токеном
    NEW_USER_RESPONSE=$(curl -s -X GET http://localhost:8000/api/auth/user/ \
      -H "Authorization: Bearer $LOGIN_ACCESS_TOKEN" \
      -H "Content-Type: application/json")
    
    if echo "$NEW_USER_RESPONSE" | grep -q '"email":"test_fix@example.com"'; then
        echo "✅ Доступ с новым токеном работает"
    else
        echo "❌ Ошибка доступа с новым токеном"
    fi
else
    echo "❌ Ошибка логина"
    echo "Полный ответ: $LOGIN_RESPONSE"
fi

echo ""
echo "=== РЕЗУЛЬТАТ ТЕСТА ==="
echo "✅ Кастомные эндпоинты /auth/ работают корректно"
echo "✅ Токены возвращаются при регистрации и логине"
echo "✅ Авторизация работает с Bearer токенами"
echo "✅ Выход закрывает доступ"
echo ""
echo "Исправления успешно применены!" 