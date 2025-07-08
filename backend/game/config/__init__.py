"""
Пакет конфигурации экономической модели

Содержит все внешние параметры и настройки модели для легкого изменения
без модификации основного кода.
"""

from .economic_config import *
from .difficulty_profiles import (
    EASY_PROFILE, 
    NORMAL_PROFILE, 
    HARD_PROFILE, 
    EXTREME_PROFILE,
    apply_difficulty_profile,
    get_profile_description
)

__all__ = [
    # Основные параметры
    'INITIAL_GDP',
    'INITIAL_POPULATION', 
    'INITIAL_INFLATION',
    'INITIAL_UNEMPLOYMENT',
    'INITIAL_INTEREST_RATE',
    'POPULATION_GROWTH_RATE',
    'TECHNOLOGY_GROWTH_RATE',
    'CAPITAL_DEPRECIATION_RATE',
    
    # Секторальные параметры
    'INDUSTRY_SHARE',
    'SERVICES_SHARE',
    'INDUSTRY_CAPITAL_ELASTICITY',
    'SERVICES_CAPITAL_ELASTICITY',
    'INDUSTRY_LABOR_ELASTICITY',
    'SERVICES_LABOR_ELASTICITY',
    
    # Бюджетные параметры
    'CORPORATE_TAX_RATE',
    'INCOME_TAX_RATE',
    'VAT_RATE',
    'SOCIAL_SPENDING_RATIO',
    'HEALTHCARE_SPENDING_RATIO',
    'EDUCATION_SPENDING_RATIO',
    
    # Монетарные параметры
    'MONEY_MULTIPLIER',
    'RESERVE_RATIO',
    'INFLATION_TARGET',
    'INFLATION_SENSITIVITY',
    
    # Внешнеэкономические параметры
    'EXCHANGE_RATE_VOLATILITY',
    'EXTERNAL_DEBT_LIMIT',
    
    # Политические параметры
    'PRESIDENT_RATING_BASE',
    'RATING_INFLATION_WEIGHT',
    'RATING_GROWTH_WEIGHT',
    'RATING_UNEMPLOYMENT_WEIGHT',
    'PUBLIC_MOOD_BASE',
    'MOOD_ECONOMIC_WEIGHT',
    'MOOD_POLITICAL_WEIGHT',
    
    # Кризисные параметры
    'CRISIS_PROBABILITY_BASE',
    'ECONOMIC_CRISIS_PROBABILITY',
    'POLITICAL_CRISIS_PROBABILITY',
    'CRISIS_GDP_IMPACT',
    'CRISIS_INFLATION_IMPACT',
    'CRISIS_RATING_IMPACT',
    
    # Игровые параметры
    'MAX_TURNS',
    'EVENT_PROBABILITY',
    'MAX_EVENTS_PER_TURN',
    
    # Настройки модели
    'MODEL_TYPES',
    'DIFFICULTY_LEVELS',
    'DEFAULT_MODEL_TYPE',
    'DEFAULT_DIFFICULTY',
    
    # Профили сложности
    'EASY_PROFILE',
    'NORMAL_PROFILE', 
    'HARD_PROFILE',
    'EXTREME_PROFILE',
    'apply_difficulty_profile',
    'get_profile_description'
] 