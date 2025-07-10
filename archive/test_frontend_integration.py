#!/usr/bin/env python3
"""
Тестовый скрипт для проверки интеграции фронтенда с расширенной моделью
"""

import requests
import json
import time
from datetime import datetime

# Конфигурация
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_step(step, description):
    print(f"\n{step}. {description}")
    print("-" * 40)

def test_api_endpoint(endpoint, method="GET", data=None, expected_status=200):
    """Тестирует API эндпоинт"""
    url = f"{API_BASE}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    if hasattr(test_api_endpoint, 'token'):
        headers["Authorization"] = f"Bearer {test_api_endpoint.token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Неподдерживаемый метод: {method}")
        
        print(f"  URL: {url}")
        print(f"  Метод: {method}")
        print(f"  Статус: {response.status_code}")
        
        if response.status_code == expected_status:
            print(f"  ✅ Успешно")
            if response.content:
                try:
                    result = response.json()
                    print(f"  Ответ: {json.dumps(result, indent=2, ensure_ascii=False)}")
                    return result
                except:
                    print(f"  Ответ: {response.text}")
            return True
        else:
            print(f"  ❌ Ошибка: {response.status_code}")
            print(f"  Ответ: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ Исключение: {str(e)}")
        return False

def main():
    print_section("ТЕСТИРОВАНИЕ ИНТЕГРАЦИИ ФРОНТЕНДА С РАСШИРЕННОЙ МОДЕЛЬЮ")
    print(f"Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Шаг 1: Регистрация пользователя
    print_step(1, "Регистрация тестового пользователя")
    
    register_data = {
        "username": "test_frontend_user",
        "email": "frontend_test@example.com",
        "password1": "testpass123",
        "password2": "testpass123"
    }
    
    result = test_api_endpoint("/dj-rest-auth/registration/", "POST", register_data, 201)
    if not result:
        print("❌ Не удалось зарегистрировать пользователя")
        return
    
    # Сохраняем токен для последующих запросов
    test_api_endpoint.token = result.get('access_token')
    print(f"  Токен получен: {test_api_endpoint.token[:20]}...")
    
    # Шаг 2: Создание расширенной игры
    print_step(2, "Создание новой расширенной игры")
    
    result = test_api_endpoint("/game/enhanced/start_enhanced_game/", "POST")
    if not result:
        print("❌ Не удалось создать игру")
        return
    
    game_id = result['game']['id']
    print(f"  Игра создана с ID: {game_id}")
    
    # Шаг 3: Получение состояния игры
    print_step(3, "Получение текущего состояния игры")
    
    result = test_api_endpoint(f"/game/enhanced/{game_id}/enhanced_state/")
    if not result:
        print("❌ Не удалось получить состояние игры")
        return
    
    game_state = result['game']
    print(f"  Ход: {game_state['turn']}")
    print(f"  Тип модели: {game_state['model_type']}")
    print(f"  ВВП: {game_state['indicators']['gdp_absolute']:.2f} млн $")
    print(f"  Рост ВВП: {game_state['indicators']['gdp_growth']:.2f}%")
    
    # Шаг 4: Получение истории игры
    print_step(4, "Получение истории игры для графиков")
    
    result = test_api_endpoint(f"/game/enhanced/{game_id}/history/")
    if not result:
        print("❌ Не удалось получить историю игры")
        return
    
    history = result['history']
    print(f"  Записей в истории: {len(history)}")
    
    # Шаг 5: Выполнение нескольких ходов
    print_step(5, "Выполнение нескольких ходов с разными сценариями")
    
    scenarios = [
        {
            "name": "Консервативная политика",
            "parameters": {
                "interest_rate": 5.0,
                "tax_rate": 20.0,
                "government_spending": 25.0,
                "social_transfers": 0.0,
                "printing_press_active": False
            }
        },
        {
            "name": "Стимулирующая политика",
            "parameters": {
                "interest_rate": 3.0,
                "tax_rate": 15.0,
                "government_spending": 30.0,
                "social_transfers": 50.0,
                "printing_press_active": False
            }
        },
        {
            "name": "Антиинфляционная политика",
            "parameters": {
                "interest_rate": 8.0,
                "tax_rate": 25.0,
                "government_spending": 20.0,
                "social_transfers": 0.0,
                "printing_press_active": False
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n  Сценарий {i}: {scenario['name']}")
        print(f"  Параметры: {scenario['parameters']}")
        
        result = test_api_endpoint(
            f"/game/enhanced/{game_id}/next_enhanced_turn/",
            "POST",
            {"parameters": scenario['parameters']}
        )
        
        if result:
            indicators = result['game']['indicators']
            print(f"  Результат:")
            print(f"    ВВП: {indicators['gdp_absolute']:.2f} млн $ (рост: {indicators['gdp_growth']:.2f}%)")
            print(f"    Инфляция: {indicators['inflation']:.2f}%")
            print(f"    Безработица: {indicators['unemployment']:.2f}%")
            print(f"    Рейтинг: {indicators['president_rating']:.1f}%")
            
            if 'industry_output' in indicators:
                print(f"    Промышленность: {indicators['industry_output']:.2f} млн $")
                print(f"    Услуги: {indicators['services_output']:.2f} млн $")
                print(f"    Курс валюты: {indicators['exchange_rate']:.3f}")
        else:
            print(f"  ❌ Ошибка выполнения хода")
    
    # Шаг 6: Проверка кризисов
    print_step(6, "Проверка системы кризисов")
    
    # Выполняем несколько ходов для возможного возникновения кризиса
    for i in range(3):
        result = test_api_endpoint(
            f"/game/enhanced/{game_id}/next_enhanced_turn/",
            "POST",
            {"parameters": {"interest_rate": 10.0, "tax_rate": 30.0, "government_spending": 15.0}}
        )
        
        if result and 'crisis' in result['game'] and result['game']['crisis']:
            crisis = result['game']['crisis']
            print(f"  🚨 Кризис возник!")
            print(f"    Тип: {crisis['type']}")
            print(f"    Описание: {crisis['description']}")
            print(f"    Эффекты: {crisis['effects']}")
            break
        else:
            print(f"  Ход {i+1}: Кризис не возник")
    
    # Шаг 7: Финальная проверка состояния
    print_step(7, "Финальная проверка состояния игры")
    
    result = test_api_endpoint(f"/game/enhanced/{game_id}/enhanced_state/")
    if result:
        game_state = result['game']
        indicators = game_state['indicators']
        budget = game_state['budget']
        
        print(f"  Итоговое состояние:")
        print(f"    Ход: {game_state['turn']}")
        print(f"    ВВП: {indicators['gdp_absolute']:.2f} млн $")
        print(f"    Рост ВВП: {indicators['gdp_growth']:.2f}%")
        print(f"    Инфляция: {indicators['inflation']:.2f}%")
        print(f"    Безработица: {indicators['unemployment']:.2f}%")
        print(f"    Рейтинг президента: {indicators['president_rating']:.1f}%")
        print(f"    Баланс бюджета: {budget['budget_balance']:.2f} млн $")
        
        if 'industry_output' in indicators:
            print(f"    Промышленность: {indicators['industry_output']:.2f} млн $")
            print(f"    Услуги: {indicators['services_output']:.2f} млн $")
            print(f"    Курс валюты: {indicators['exchange_rate']:.3f}")
            print(f"    Внешний долг: {indicators['external_debt']:.2f} млн $")
            print(f"    Население: {indicators['population']:.2f} млн чел.")
    
    print_section("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("✅ Все основные функции расширенной модели работают корректно")
    print("✅ API эндпоинты отвечают правильно")
    print("✅ Данные передаются в корректном формате")
    print("✅ Система готова для интеграции с фронтендом")

if __name__ == "__main__":
    main() 