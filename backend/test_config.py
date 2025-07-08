#!/usr/bin/env python
"""
Тестовый скрипт для проверки конфигурации экономической модели
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.config import *
from game.config.difficulty_profiles import apply_difficulty_profile, get_profile_description

def test_basic_config():
    """Тест основных параметров конфигурации"""
    print("=== Тест основных параметров конфигурации ===")
    print(f"Начальный ВВП: {INITIAL_GDP} млрд $")
    print(f"Начальная численность населения: {INITIAL_POPULATION} млн чел.")
    print(f"Начальная инфляция: {INITIAL_INFLATION}%")
    print(f"Начальная безработица: {INITIAL_UNEMPLOYMENT}%")
    print(f"Доля промышленности: {INDUSTRY_SHARE * 100}%")
    print(f"Доля услуг: {SERVICES_SHARE * 100}%")
    print(f"Целевая инфляция: {INFLATION_TARGET}%")
    print(f"Базовый рейтинг президента: {PRESIDENT_RATING_BASE}")
    print(f"Вероятность кризиса: {CRISIS_PROBABILITY_BASE * 100}%")
    print()

def test_difficulty_profiles():
    """Тест профилей сложности"""
    print("=== Тест профилей сложности ===")
    
    profiles = ['easy', 'normal', 'hard', 'extreme']
    
    for profile in profiles:
        print(f"\n--- {profile.upper()} ---")
        print(get_profile_description(profile))
        
        config = apply_difficulty_profile(profile)
        print(f"Начальный ВВП: {config['INITIAL_GDP']} млрд $")
        print(f"Начальная инфляция: {config['INITIAL_INFLATION']}%")
        print(f"Начальная безработица: {config['INITIAL_UNEMPLOYMENT']}%")
        print(f"Базовый рейтинг: {config['PRESIDENT_RATING_BASE']}")
        print(f"Вероятность кризиса: {config['CRISIS_PROBABILITY_BASE'] * 100}%")
    
    print()

def test_model_parameters():
    """Тест параметров модели"""
    print("=== Тест параметров модели ===")
    
    # Проверяем, что все параметры доступны
    required_params = [
        'INITIAL_GDP', 'INITIAL_POPULATION', 'INITIAL_INFLATION',
        'INITIAL_UNEMPLOYMENT', 'INITIAL_INTEREST_RATE',
        'INDUSTRY_SHARE', 'SERVICES_SHARE',
        'CORPORATE_TAX_RATE', 'INCOME_TAX_RATE', 'VAT_RATE',
        'INFLATION_TARGET', 'PRESIDENT_RATING_BASE',
        'CRISIS_PROBABILITY_BASE'
    ]
    
    missing_params = []
    for param in required_params:
        if not hasattr(sys.modules[__name__], param):
            missing_params.append(param)
    
    if missing_params:
        print(f"❌ Отсутствуют параметры: {missing_params}")
    else:
        print("✅ Все основные параметры доступны")
    
    # Проверяем логичность значений
    print("\nПроверка логичности значений:")
    
    if INDUSTRY_SHARE + SERVICES_SHARE == 1.0:
        print("✅ Доли секторов в сумме дают 100%")
    else:
        print(f"❌ Доли секторов: {INDUSTRY_SHARE + SERVICES_SHARE}")
    
    if RATING_GROWTH_WEIGHT + RATING_INFLATION_WEIGHT + RATING_UNEMPLOYMENT_WEIGHT == 1.0:
        print("✅ Веса рейтинга в сумме дают 100%")
    else:
        print(f"❌ Веса рейтинга: {RATING_GROWTH_WEIGHT + RATING_INFLATION_WEIGHT + RATING_UNEMPLOYMENT_WEIGHT}")
    
    if INITIAL_GDP > 0:
        print("✅ Начальный ВВП положительный")
    else:
        print("❌ Начальный ВВП отрицательный")
    
    print()

def main():
    """Основная функция тестирования"""
    print("Тестирование конфигурации экономической модели")
    print("=" * 50)
    
    try:
        test_basic_config()
        test_difficulty_profiles()
        test_model_parameters()
        
        print("🎉 Все тесты конфигурации пройдены успешно!")
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 