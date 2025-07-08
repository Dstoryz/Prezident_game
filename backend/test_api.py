#!/usr/bin/env python
"""
Скрипт для тестирования API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_registration():
    """Тест регистрации пользователя"""
    print("=== Тест регистрации ===")
    
    data = {
        "email": "test@example.com",
        "password1": "testpass123",
        "password2": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/dj-rest-auth/registration/", json=data)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Response text: {response.text}")
    return response

def test_login():
    """Тест входа пользователя"""
    print("\n=== Тест входа ===")
    
    data = {
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/dj-rest-auth/login/", json=data)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Response text: {response.text}")
    return response

def test_start_enhanced_game(token):
    """Тест запуска расширенной игры"""
    print("\n=== Тест запуска расширенной игры ===")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{BASE_URL}/api/game/enhanced/start_enhanced_game/", headers=headers)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Response text: {response.text}")
    return response

def test_next_enhanced_turn(token, game_id):
    """Тест следующего хода"""
    print("\n=== Тест следующего хода ===")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
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
            "printing_press_active": False
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/game/enhanced/{game_id}/next_enhanced_turn/", 
                           headers=headers, json=data)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Response text: {response.text}")
    return response

def test_get_enhanced_state(token, game_id):
    """Тест получения состояния игры"""
    print("\n=== Тест получения состояния ===")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(f"{BASE_URL}/api/game/enhanced/{game_id}/enhanced_state/", headers=headers)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {response.json()}")
    except:
        print(f"Response text: {response.text}")
    return response

def main():
    """Основная функция тестирования"""
    print("Начинаем тестирование API...")
    
    # Тест регистрации
    reg_response = test_registration()
    
    # Тест входа
    login_response = test_login()
    
    if login_response.status_code == 200:
        token = login_response.json().get('access')
        
        if token:
            # Тест запуска игры
            game_response = test_start_enhanced_game(token)
            
            if game_response.status_code == 200:
                game_id = game_response.json().get('game', {}).get('id')
                
                if game_id:
                    # Тест получения состояния
                    test_get_enhanced_state(token, game_id)
                    
                    # Тест следующего хода
                    test_next_enhanced_turn(token, game_id)
                    
                    # Тест получения состояния после хода
                    test_get_enhanced_state(token, game_id)
                else:
                    print("Не удалось получить ID игры")
            else:
                print("Не удалось запустить игру")
        else:
            print("Не удалось получить токен доступа")
    else:
        print("Не удалось войти в систему")

if __name__ == "__main__":
    main() 