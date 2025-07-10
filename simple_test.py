#!/usr/bin/env python3
"""
Простой тест для проверки исправлений деления на ноль
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from game.services.economic_logic import EconomicEngine

def test_zero_division_fix():
    """Тест исправления деления на ноль"""
    print("🔧 Тестирование исправления деления на ноль")
    print("=" * 50)
    
    engine = EconomicEngine()
    
    # Тест с нулевыми значениями
    zero_params = {
        'interest_rate': 0.0,
        'tax_rate': 0.0,
        'government_spending': 0.0,
        'customs_duty': 0.0,
        'education_priority': 0.0,
        'healthcare_priority': 0.0,
        'defense_priority': 0.0,
        'infrastructure_priority': 0.0,
        'social_priority': 0.0,
        'reserve_ratio': 0.0,
        'refinance_rate': 0.0,
        'printing_press_active': False,
        'social_transfers': 0.0
    }
    
    try:
        result = engine.calculate_indicators(zero_params)
        print("✅ Тест с нулевыми значениями прошел успешно")
        print(f"  ВВП: {result.get('gdp_growth', 0):.1f}%")
        print(f"  Инфляция: {result.get('inflation', 0):.1f}%")
        print(f"  Безработица: {result.get('unemployment', 0):.1f}%")
        print(f"  Рейтинг: {result.get('president_rating', 0):.1f}%")
        return True
    except Exception as e:
        print(f"❌ Ошибка при тестировании нулевых значений: {e}")
        return False
    
    # Тест с минимальными значениями
    min_params = {
        'interest_rate': 0.1,
        'tax_rate': 0.1,
        'government_spending': 0.1,
        'customs_duty': 0.1,
        'education_priority': 0.1,
        'healthcare_priority': 0.1,
        'defense_priority': 0.1,
        'infrastructure_priority': 0.1,
        'social_priority': 0.1,
        'reserve_ratio': 0.001,
        'refinance_rate': 0.001,
        'printing_press_active': False,
        'social_transfers': 0.1
    }
    
    try:
        result = engine.calculate_indicators(min_params)
        print("✅ Тест с минимальными значениями прошел успешно")
        print(f"  ВВП: {result.get('gdp_growth', 0):.1f}%")
        print(f"  Инфляция: {result.get('inflation', 0):.1f}%")
        print(f"  Безработица: {result.get('unemployment', 0):.1f}%")
        print(f"  Рейтинг: {result.get('president_rating', 0):.1f}%")
        return True
    except Exception as e:
        print(f"❌ Ошибка при тестировании минимальных значений: {e}")
        return False

if __name__ == "__main__":
    success = test_zero_division_fix()
    if success:
        print("\n🎉 Все тесты прошли успешно!")
    else:
        print("\n❌ Обнаружены проблемы") 