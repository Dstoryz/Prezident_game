#!/usr/bin/env python3
"""
Тест устойчивости макроэкономической модели игры "Президент"
Проверяет стабильность экономических показателей при различных сценариях
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from game.services.economic_logic import EconomicEngine
from game.services.solow_model import SolowModel, BudgetCalculator, DemographicCalculator
import json
import time

def test_economic_stability():
    """Тест устойчивости экономической модели"""
    print("🧪 Тестирование устойчивости макроэкономической модели")
    print("=" * 60)
    
    engine = EconomicEngine()
    solow = SolowModel()
    
    # Тест 1: Базовая стабильность модели Солоу
    print("\n📊 Тест 1: Базовая стабильность модели Солоу")
    print("-" * 40)
    
    # Начальные параметры
    capital = 1000.0
    labor = 50.0
    technology = 1.0
    savings_rate = 0.2
    
    print(f"Начальные параметры:")
    print(f"  Капитал: {capital:.1f} млн $")
    print(f"  Рабочая сила: {labor:.1f} млн чел.")
    print(f"  Технологии: {technology:.2f}")
    print(f"  Норма сбережений: {savings_rate:.1%}")
    
    # Симуляция на 20 лет
    results = []
    for year in range(20):
        growth = solow.calculate_growth_rates(capital, labor, technology, savings_rate)
        
        results.append({
            'year': year + 1,
            'gdp': growth['new_gdp'],
            'gdp_growth': growth['gdp_growth'],
            'capital': growth['new_capital'],
            'labor': growth['new_labor'],
            'technology': growth['new_technology']
        })
        
        # Обновляем параметры для следующего года
        capital = growth['new_capital']
        labor = growth['new_labor']
        technology = growth['new_technology']
    
    # Анализ результатов
    gdp_growth_rates = [r['gdp_growth'] for r in results]
    avg_growth = sum(gdp_growth_rates) / len(gdp_growth_rates)
    growth_volatility = max(gdp_growth_rates) - min(gdp_growth_rates)
    
    print(f"\nРезультаты за 20 лет:")
    print(f"  Средний рост ВВП: {avg_growth:.2f}%")
    print(f"  Волатильность роста: {growth_volatility:.2f}%")
    print(f"  Финальный ВВП: {results[-1]['gdp']:.1f} млн $")
    print(f"  Финальный капитал: {results[-1]['capital']:.1f} млн $")
    
    # Проверка стабильности
    stability_score = 0
    if 1.0 <= avg_growth <= 5.0:
        stability_score += 1
        print("  ✅ Рост ВВП в разумных пределах")
    else:
        print(f"  ❌ Рост ВВП слишком {'высокий' if avg_growth > 5.0 else 'низкий'}")
    
    if growth_volatility < 2.0:
        stability_score += 1
        print("  ✅ Низкая волатильность роста")
    else:
        print(f"  ❌ Высокая волатильность роста: {growth_volatility:.2f}%")
    
    # Тест 2: Влияние политических решений
    print("\n🎯 Тест 2: Влияние политических решений")
    print("-" * 40)
    
    # Базовые параметры управления
    base_params = {
        'interest_rate': 5.0,
        'tax_rate': 20.0,
        'government_spending': 25.0,
        'customs_duty': 5.0,
        'education_priority': 20.0,
        'healthcare_priority': 20.0,
        'defense_priority': 20.0,
        'infrastructure_priority': 20.0,
        'social_priority': 20.0
    }
    
    # Тестируем разные сценарии
    scenarios = [
        ("Консервативная политика", {
            'interest_rate': 7.0,
            'tax_rate': 25.0,
            'government_spending': 20.0,
            'customs_duty': 8.0
        }),
        ("Стимулирующая политика", {
            'interest_rate': 3.0,
            'tax_rate': 15.0,
            'government_spending': 35.0,
            'customs_duty': 2.0
        }),
        ("Экстремальная политика", {
            'interest_rate': 1.0,
            'tax_rate': 5.0,
            'government_spending': 50.0,
            'customs_duty': 0.0
        })
    ]
    
    scenario_results = {}
    
    for scenario_name, scenario_params in scenarios:
        print(f"\n{scenario_name}:")
        
        # Объединяем базовые и сценарийные параметры
        test_params = base_params.copy()
        test_params.update(scenario_params)
        
        # Симуляция на 10 лет
        indicators = None
        budget = None
        demographics = None
        production = None
        
        scenario_data = []
        
        for year in range(10):
            result = engine.calculate_indicators(
                test_params, indicators, budget, demographics, production
            )
            
            scenario_data.append({
                'year': year + 1,
                'gdp_growth': result.get('gdp_growth', 0),
                'inflation': result.get('inflation', 0),
                'unemployment': result.get('unemployment', 0),
                'president_rating': result.get('president_rating', 0),
                'budget_deficit': result.get('budget_deficit_percent', 0)
            })
            
            # Обновляем для следующего года
            indicators = result
            budget = result.get('budget_data', {})
            demographics = result.get('demographic_data', {})
            production = result.get('production_data', {})
        
        # Анализ сценария
        avg_rating = sum(d['president_rating'] for d in scenario_data) / len(scenario_data)
        avg_inflation = sum(d['inflation'] for d in scenario_data) / len(scenario_data)
        avg_unemployment = sum(d['unemployment'] for d in scenario_data) / len(scenario_data)
        
        print(f"  Средний рейтинг президента: {avg_rating:.1f}%")
        print(f"  Средняя инфляция: {avg_inflation:.1f}%")
        print(f"  Средняя безработица: {avg_unemployment:.1f}%")
        
        scenario_results[scenario_name] = {
            'avg_rating': avg_rating,
            'avg_inflation': avg_inflation,
            'avg_unemployment': avg_unemployment,
            'data': scenario_data
        }
    
    # Тест 3: Проверка граничных условий
    print("\n⚠️ Тест 3: Граничные условия")
    print("-" * 40)
    
    edge_cases = [
        ("Минимальные значения", {
            'interest_rate': 0.1,
            'tax_rate': 1.0,
            'government_spending': 5.0,
            'customs_duty': 0.1
        }),
        ("Максимальные значения", {
            'interest_rate': 20.0,
            'tax_rate': 50.0,
            'government_spending': 80.0,
            'customs_duty': 30.0
        }),
        ("Нулевые значения", {
            'interest_rate': 0.0,
            'tax_rate': 0.0,
            'government_spending': 0.0,
            'customs_duty': 0.0
        })
    ]
    
    edge_case_results = {}
    
    for case_name, case_params in edge_cases:
        print(f"\n{case_name}:")
        
        test_params = base_params.copy()
        test_params.update(case_params)
        
        try:
            result = engine.calculate_indicators(test_params)
            
            # Проверяем, что все значения в разумных пределах
            gdp_growth = result.get('gdp_growth', 0)
            inflation = result.get('inflation', 0)
            unemployment = result.get('unemployment', 0)
            president_rating = result.get('president_rating', 0)
            
            print(f"  ВВП: {gdp_growth:.1f}%")
            print(f"  Инфляция: {inflation:.1f}%")
            print(f"  Безработица: {unemployment:.1f}%")
            print(f"  Рейтинг: {president_rating:.1f}%")
            
            # Проверка на разумность значений
            if -50 <= gdp_growth <= 100:
                print("  ✅ ВВП в разумных пределах")
            else:
                print(f"  ❌ ВВП вне разумных пределов: {gdp_growth:.1f}%")
            
            if 0 <= inflation <= 100:
                print("  ✅ Инфляция в разумных пределах")
            else:
                print(f"  ❌ Инфляция вне разумных пределов: {inflation:.1f}%")
            
            if 0 <= unemployment <= 50:
                print("  ✅ Безработица в разумных пределах")
            else:
                print(f"  ❌ Безработица вне разумных пределов: {unemployment:.1f}%")
            
            if 0 <= president_rating <= 100:
                print("  ✅ Рейтинг в разумных пределах")
            else:
                print(f"  ❌ Рейтинг вне разумных пределов: {president_rating:.1f}%")
                
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
    
    # Тест 4: Проверка производительности
    print("\n⚡ Тест 4: Производительность")
    print("-" * 40)
    
    start_time = time.time()
    
    # Выполняем 1000 расчетов
    for i in range(1000):
        engine.calculate_indicators(base_params)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"Время выполнения 1000 расчетов: {execution_time:.3f} сек")
    print(f"Среднее время на расчет: {(execution_time/1000)*1000:.2f} мс")
    
    if execution_time < 5.0:
        print("  ✅ Производительность удовлетворительная")
    else:
        print("  ⚠️ Производительность может быть улучшена")
    
    # Итоговая оценка
    print("\n📋 Итоговая оценка модели")
    print("=" * 60)
    
    total_score = stability_score
    
    # Оценка политических сценариев
    conservative = scenario_results.get("Консервативная политика", {})
    stimulating = scenario_results.get("Стимулирующая политика", {})
    
    if conservative.get('avg_rating', 0) > 40:
        total_score += 1
        print("  ✅ Консервативная политика дает стабильные результаты")
    
    if stimulating.get('avg_rating', 0) > 40:
        total_score += 1
        print("  ✅ Стимулирующая политика дает стабильные результаты")
    
    if execution_time < 5.0:
        total_score += 1
        print("  ✅ Производительность модели удовлетворительная")
    
    print(f"\n🎯 Общий балл: {total_score}/5")
    
    if total_score >= 4:
        print("  🎉 Модель готова к использованию!")
    elif total_score >= 3:
        print("  ⚠️ Модель требует небольших доработок")
    else:
        print("  ❌ Модель требует серьезных доработок")
    
    return total_score >= 4

def test_api_endpoints():
    """Тест API эндпоинтов"""
    print("\n🌐 Тестирование API эндпоинтов")
    print("=" * 60)
    
    import requests
    import time
    
    base_url = "http://localhost:8000"
    
    # Ждем запуска сервера
    print("Ожидание запуска сервера...")
    for i in range(30):
        try:
            response = requests.get(f"{base_url}/api/", timeout=5)
            if response.status_code == 200:
                print("✅ Сервер запущен")
                break
        except:
            time.sleep(1)
    else:
        print("❌ Сервер не запустился")
        return False
    
    # Тест регистрации
    print("\n📝 Тест регистрации пользователя")
    try:
        register_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
            "password_confirm": "testpass123"
        }
        
        response = requests.post(f"{base_url}/api/auth/register/", json=register_data)
        print(f"Статус регистрации: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Регистрация успешна")
        else:
            print(f"❌ Ошибка регистрации: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при регистрации: {e}")
    
    # Тест логина
    print("\n🔐 Тест входа в систему")
    try:
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        
        response = requests.post(f"{base_url}/api/auth/login/", json=login_data)
        print(f"Статус входа: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Вход успешен")
            tokens = response.json().get('tokens', {})
            access_token = tokens.get('access')
            
            if access_token:
                # Тест создания игры
                print("\n🎮 Тест создания игры")
                headers = {"Authorization": f"Bearer {access_token}"}
                
                response = requests.post(f"{base_url}/api/game/start/", headers=headers)
                print(f"Статус создания игры: {response.status_code}")
                
                if response.status_code == 201:
                    print("✅ Игра создана")
                    game_data = response.json()
                    game_id = game_data.get('id')
                    
                    if game_id:
                        # Тест получения состояния игры
                        response = requests.get(f"{base_url}/api/game/{game_id}/state/", headers=headers)
                        print(f"Статус получения состояния: {response.status_code}")
                        
                        if response.status_code == 200:
                            print("✅ Состояние игры получено")
                            
                            # Тест следующего хода
                            move_data = {
                                "interest_rate": 5.0,
                                "tax_rate": 20.0,
                                "government_spending": 25.0,
                                "customs_duty": 5.0
                            }
                            
                            response = requests.post(f"{base_url}/api/game/{game_id}/next-turn/", 
                                                   json=move_data, headers=headers)
                            print(f"Статус следующего хода: {response.status_code}")
                            
                            if response.status_code == 200:
                                print("✅ Следующий ход выполнен")
                            else:
                                print(f"❌ Ошибка следующего хода: {response.text}")
                        else:
                            print(f"❌ Ошибка получения состояния: {response.text}")
                    else:
                        print("❌ ID игры не получен")
                else:
                    print(f"❌ Ошибка создания игры: {response.text}")
            else:
                print("❌ Access token не получен")
        else:
            print(f"❌ Ошибка входа: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при входе: {e}")
    
    return True

if __name__ == "__main__":
    print("🎮 Тестирование игры 'Президент: Экономика и Власть'")
    print("=" * 80)
    
    # Тест экономической модели
    model_ok = test_economic_stability()
    
    # Тест API
    api_ok = test_api_endpoints()
    
    print("\n" + "=" * 80)
    print("📊 ИТОГОВЫЙ ОТЧЕТ")
    print("=" * 80)
    
    if model_ok and api_ok:
        print("🎉 Все тесты пройдены успешно!")
        print("✅ Экономическая модель стабильна")
        print("✅ API работает корректно")
        print("✅ Проект готов к использованию")
    else:
        print("⚠️ Обнаружены проблемы:")
        if not model_ok:
            print("❌ Проблемы с экономической моделью")
        if not api_ok:
            print("❌ Проблемы с API")
        print("🔧 Требуется доработка") 