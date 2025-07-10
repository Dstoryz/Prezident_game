#!/usr/bin/env python3
"""
Тест расширенной экономической модели EnhancedEconomicModel
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from game.services.enhanced_economic_model import EnhancedEconomicModel, EconomicParameters
import time

def test_enhanced_economic_model():
    """Тест расширенной экономической модели"""
    print("🧪 Тестирование расширенной экономической модели")
    print("=" * 60)
    
    model = EnhancedEconomicModel()
    
    # Тест 1: Базовые параметры
    print("\n📊 Тест 1: Базовые параметры")
    print("-" * 40)
    
    basic_params = EconomicParameters(
        interest_rate=5.0,
        tax_rate=20.0,
        government_spending=25.0,
        customs_duty=5.0
    )
    
    try:
        result = model.calculate_indicators(basic_params)
        print("✅ Базовые параметры обработаны успешно")
        print(f"  ВВП: {result.get('gdp_growth', 0):.1f}%")
        print(f"  Инфляция: {result.get('inflation', 0):.1f}%")
        print(f"  Безработица: {result.get('unemployment', 0):.1f}%")
        print(f"  Рейтинг: {result.get('president_rating', 0):.1f}%")
        print(f"  Промышленность: {result.get('industry_output', 0):.1f}")
        print(f"  Услуги: {result.get('services_output', 0):.1f}")
    except Exception as e:
        print(f"❌ Ошибка при обработке базовых параметров: {e}")
        return False
    
    # Тест 2: Экстремальные параметры
    print("\n⚠️ Тест 2: Экстремальные параметры")
    print("-" * 40)
    
    extreme_params = EconomicParameters(
        interest_rate=0.1,
        tax_rate=0.1,
        government_spending=0.1,
        customs_duty=0.1,
        reserve_ratio=0.001,
        refinance_rate=0.001,
        printing_press_active=True,
        social_transfers=1000.0
    )
    
    try:
        result = model.calculate_indicators(extreme_params)
        print("✅ Экстремальные параметры обработаны успешно")
        print(f"  ВВП: {result.get('gdp_growth', 0):.1f}%")
        print(f"  Инфляция: {result.get('inflation', 0):.1f}%")
        print(f"  Безработица: {result.get('unemployment', 0):.1f}%")
        print(f"  Рейтинг: {result.get('president_rating', 0):.1f}%")
    except Exception as e:
        print(f"❌ Ошибка при обработке экстремальных параметров: {e}")
        return False
    
    # Тест 3: Нулевые параметры
    print("\n🔧 Тест 3: Нулевые параметры")
    print("-" * 40)
    
    zero_params = EconomicParameters(
        interest_rate=0.0,
        tax_rate=0.0,
        government_spending=0.0,
        customs_duty=0.0,
        reserve_ratio=0.0,
        refinance_rate=0.0,
        printing_press_active=False,
        social_transfers=0.0
    )
    
    try:
        result = model.calculate_indicators(zero_params)
        print("✅ Нулевые параметры обработаны успешно")
        print(f"  ВВП: {result.get('gdp_growth', 0):.1f}%")
        print(f"  Инфляция: {result.get('inflation', 0):.1f}%")
        print(f"  Безработица: {result.get('unemployment', 0):.1f}%")
        print(f"  Рейтинг: {result.get('president_rating', 0):.1f}%")
    except Exception as e:
        print(f"❌ Ошибка при обработке нулевых параметров: {e}")
        return False
    
    # Тест 4: Производительность
    print("\n⚡ Тест 4: Производительность")
    print("-" * 40)
    
    start_time = time.time()
    
    # Выполняем 1000 расчетов
    for i in range(1000):
        model.calculate_indicators(basic_params)
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"Время выполнения 1000 расчетов: {execution_time:.3f} сек")
    print(f"Среднее время на расчет: {(execution_time/1000)*1000:.2f} мс")
    
    if execution_time < 5.0:
        print("  ✅ Производительность удовлетворительная")
    else:
        print("  ⚠️ Производительность может быть улучшена")
    
    # Тест 5: Проверка всех полей результата
    print("\n📋 Тест 5: Проверка полей результата")
    print("-" * 40)
    
    result = model.calculate_indicators(basic_params)
    
    required_fields = [
        'gdp_growth', 'gdp_absolute', 'inflation', 'unemployment', 
        'president_rating', 'public_mood', 'industry_output', 'services_output',
        'exports', 'imports', 'trade_balance', 'exchange_rate',
        'tax_revenue', 'total_revenue', 'total_spending', 'budget_balance',
        'population', 'money_supply', 'gold_reserves', 'external_debt'
    ]
    
    missing_fields = []
    for field in required_fields:
        if field not in result:
            missing_fields.append(field)
    
    if missing_fields:
        print(f"❌ Отсутствуют поля: {missing_fields}")
        return False
    else:
        print("✅ Все необходимые поля присутствуют")
    
    # Тест 6: Симуляция нескольких ходов
    print("\n🔄 Тест 6: Симуляция нескольких ходов")
    print("-" * 40)
    
    previous_indicators = None
    for turn in range(5):
        result = model.calculate_indicators(basic_params, previous_indicators)
        print(f"  Ход {turn + 1}: ВВП {result.get('gdp_growth', 0):.1f}%, "
              f"Рейтинг {result.get('president_rating', 0):.1f}%")
        previous_indicators = result
    
    print("\n🎉 Все тесты расширенной модели прошли успешно!")
    return True

if __name__ == "__main__":
    success = test_enhanced_economic_model()
    if success:
        print("\n✅ Расширенная модель готова к использованию!")
    else:
        print("\n❌ Обнаружены проблемы в расширенной модели") 