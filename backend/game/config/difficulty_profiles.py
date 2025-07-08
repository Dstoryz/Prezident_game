"""
Профили настроек для разных уровней сложности игры

Этот файл содержит предустановленные конфигурации для легкого, нормального и сложного уровней.
"""

# =============================================================================
# ЛЕГКИЙ УРОВЕНЬ - для начинающих игроков
# =============================================================================

EASY_PROFILE = {
    # Экономические параметры
    'INITIAL_GDP': 1500.0,  # Больше начальный ВВП
    'INITIAL_POPULATION': 150.0,
    'INITIAL_INFLATION': 2.0,  # Низкая инфляция
    'INITIAL_UNEMPLOYMENT': 4.0,  # Низкая безработица
    'INITIAL_INTEREST_RATE': 3.0,  # Низкие ставки
    
    # Параметры роста
    'POPULATION_GROWTH_RATE': 1.0,  # Стабильный рост населения
    'TECHNOLOGY_GROWTH_RATE': 2.0,  # Высокий технологический рост
    'CAPITAL_DEPRECIATION_RATE': 0.03,  # Медленная амортизация
    
    # Секторальные параметры
    'INDUSTRY_SHARE': 0.30,  # Современная структура
    'SERVICES_SHARE': 0.70,
    
    # Бюджетные параметры
    'CORPORATE_TAX_RATE': 0.15,  # Низкие налоги
    'INCOME_TAX_RATE': 0.10,
    'VAT_RATE': 0.15,
    'SOCIAL_SPENDING_RATIO': 0.30,  # Высокие социальные расходы
    
    # Монетарные параметры
    'INFLATION_TARGET': 2.0,
    'INFLATION_SENSITIVITY': 0.3,  # Низкая чувствительность
    
    # Политические параметры
    'PRESIDENT_RATING_BASE': 60.0,  # Высокий базовый рейтинг
    'RATING_GROWTH_WEIGHT': 0.5,  # Больше внимания росту
    'RATING_INFLATION_WEIGHT': 0.2,  # Меньше внимания инфляции
    'RATING_UNEMPLOYMENT_WEIGHT': 0.3,
    
    # Кризисные параметры
    'CRISIS_PROBABILITY_BASE': 0.02,  # Редкие кризисы
    'ECONOMIC_CRISIS_PROBABILITY': 0.01,
    'POLITICAL_CRISIS_PROBABILITY': 0.01,
    'CRISIS_GDP_IMPACT': -0.03,  # Слабые кризисы
    'CRISIS_INFLATION_IMPACT': 0.02,
    'CRISIS_RATING_IMPACT': -5.0,
}

# =============================================================================
# НОРМАЛЬНЫЙ УРОВЕНЬ - стандартная игра
# =============================================================================

NORMAL_PROFILE = {
    # Экономические параметры
    'INITIAL_GDP': 1000.0,
    'INITIAL_POPULATION': 150.0,
    'INITIAL_INFLATION': 2.5,
    'INITIAL_UNEMPLOYMENT': 5.0,
    'INITIAL_INTEREST_RATE': 4.0,
    
    # Параметры роста
    'POPULATION_GROWTH_RATE': 0.8,
    'TECHNOLOGY_GROWTH_RATE': 1.5,
    'CAPITAL_DEPRECIATION_RATE': 0.05,
    
    # Секторальные параметры
    'INDUSTRY_SHARE': 0.35,
    'SERVICES_SHARE': 0.65,
    
    # Бюджетные параметры
    'CORPORATE_TAX_RATE': 0.20,
    'INCOME_TAX_RATE': 0.15,
    'VAT_RATE': 0.18,
    'SOCIAL_SPENDING_RATIO': 0.25,
    
    # Монетарные параметры
    'INFLATION_TARGET': 2.0,
    'INFLATION_SENSITIVITY': 0.5,
    
    # Политические параметры
    'PRESIDENT_RATING_BASE': 50.0,
    'RATING_GROWTH_WEIGHT': 0.4,
    'RATING_INFLATION_WEIGHT': 0.3,
    'RATING_UNEMPLOYMENT_WEIGHT': 0.3,
    
    # Кризисные параметры
    'CRISIS_PROBABILITY_BASE': 0.05,
    'ECONOMIC_CRISIS_PROBABILITY': 0.03,
    'POLITICAL_CRISIS_PROBABILITY': 0.02,
    'CRISIS_GDP_IMPACT': -0.05,
    'CRISIS_INFLATION_IMPACT': 0.03,
    'CRISIS_RATING_IMPACT': -10.0,
}

# =============================================================================
# СЛОЖНЫЙ УРОВЕНЬ - для опытных игроков
# =============================================================================

HARD_PROFILE = {
    # Экономические параметры
    'INITIAL_GDP': 500.0,  # Меньше начальный ВВП
    'INITIAL_POPULATION': 150.0,
    'INITIAL_INFLATION': 5.0,  # Высокая инфляция
    'INITIAL_UNEMPLOYMENT': 8.0,  # Высокая безработица
    'INITIAL_INTEREST_RATE': 8.0,  # Высокие ставки
    
    # Параметры роста
    'POPULATION_GROWTH_RATE': 0.5,  # Медленный рост населения
    'TECHNOLOGY_GROWTH_RATE': 1.0,  # Медленный технологический рост
    'CAPITAL_DEPRECIATION_RATE': 0.08,  # Быстрая амортизация
    
    # Секторальные параметры
    'INDUSTRY_SHARE': 0.50,  # Индустриальная структура
    'SERVICES_SHARE': 0.50,
    
    # Бюджетные параметры
    'CORPORATE_TAX_RATE': 0.25,  # Высокие налоги
    'INCOME_TAX_RATE': 0.20,
    'VAT_RATE': 0.22,
    'SOCIAL_SPENDING_RATIO': 0.20,  # Низкие социальные расходы
    
    # Монетарные параметры
    'INFLATION_TARGET': 2.0,
    'INFLATION_SENSITIVITY': 0.8,  # Высокая чувствительность
    
    # Политические параметры
    'PRESIDENT_RATING_BASE': 40.0,  # Низкий базовый рейтинг
    'RATING_GROWTH_WEIGHT': 0.3,  # Меньше внимания росту
    'RATING_INFLATION_WEIGHT': 0.5,  # Больше внимания инфляции
    'RATING_UNEMPLOYMENT_WEIGHT': 0.2,
    
    # Кризисные параметры
    'CRISIS_PROBABILITY_BASE': 0.10,  # Частые кризисы
    'ECONOMIC_CRISIS_PROBABILITY': 0.06,
    'POLITICAL_CRISIS_PROBABILITY': 0.04,
    'CRISIS_GDP_IMPACT': -0.08,  # Сильные кризисы
    'CRISIS_INFLATION_IMPACT': 0.05,
    'CRISIS_RATING_IMPACT': -15.0,
}

# =============================================================================
# ЭКСТРЕМАЛЬНЫЙ УРОВЕНЬ - для экспертов
# =============================================================================

EXTREME_PROFILE = {
    # Экономические параметры
    'INITIAL_GDP': 200.0,  # Очень мало начального ВВП
    'INITIAL_POPULATION': 150.0,
    'INITIAL_INFLATION': 15.0,  # Гиперинфляция
    'INITIAL_UNEMPLOYMENT': 15.0,  # Массовая безработица
    'INITIAL_INTEREST_RATE': 20.0,  # Экстремальные ставки
    
    # Параметры роста
    'POPULATION_GROWTH_RATE': 0.0,  # Стагнация населения
    'TECHNOLOGY_GROWTH_RATE': 0.5,  # Очень медленный рост
    'CAPITAL_DEPRECIATION_RATE': 0.15,  # Очень быстрая амортизация
    
    # Секторальные параметры
    'INDUSTRY_SHARE': 0.70,  # Примитивная структура
    'SERVICES_SHARE': 0.30,
    
    # Бюджетные параметры
    'CORPORATE_TAX_RATE': 0.35,  # Экстремальные налоги
    'INCOME_TAX_RATE': 0.30,
    'VAT_RATE': 0.25,
    'SOCIAL_SPENDING_RATIO': 0.10,  # Минимальные социальные расходы
    
    # Монетарные параметры
    'INFLATION_TARGET': 2.0,
    'INFLATION_SENSITIVITY': 1.0,  # Максимальная чувствительность
    
    # Политические параметры
    'PRESIDENT_RATING_BASE': 20.0,  # Очень низкий рейтинг
    'RATING_GROWTH_WEIGHT': 0.2,
    'RATING_INFLATION_WEIGHT': 0.6,  # Максимальное внимание инфляции
    'RATING_UNEMPLOYMENT_WEIGHT': 0.2,
    
    # Кризисные параметры
    'CRISIS_PROBABILITY_BASE': 0.20,  # Постоянные кризисы
    'ECONOMIC_CRISIS_PROBABILITY': 0.12,
    'POLITICAL_CRISIS_PROBABILITY': 0.08,
    'CRISIS_GDP_IMPACT': -0.15,  # Катастрофические кризисы
    'CRISIS_INFLATION_IMPACT': 0.10,
    'CRISIS_RATING_IMPACT': -25.0,
}

# =============================================================================
# ФУНКЦИИ ДЛЯ ПРИМЕНЕНИЯ ПРОФИЛЕЙ
# =============================================================================

def apply_difficulty_profile(profile_name: str) -> dict:
    """
    Применить профиль сложности к конфигурации
    
    Args:
        profile_name: Название профиля ('easy', 'normal', 'hard', 'extreme')
    
    Returns:
        Словарь с параметрами профиля
    """
    profiles = {
        'easy': EASY_PROFILE,
        'normal': NORMAL_PROFILE,
        'hard': HARD_PROFILE,
        'extreme': EXTREME_PROFILE
    }
    
    if profile_name not in profiles:
        raise ValueError(f"Неизвестный профиль: {profile_name}")
    
    return profiles[profile_name]

def get_profile_description(profile_name: str) -> str:
    """
    Получить описание профиля сложности
    
    Args:
        profile_name: Название профиля
    
    Returns:
        Описание профиля
    """
    descriptions = {
        'easy': "Легкий уровень - для начинающих игроков. Стабильная экономика, редкие кризисы, высокий базовый рейтинг.",
        'normal': "Нормальный уровень - стандартная игра. Сбалансированные параметры для большинства игроков.",
        'hard': "Сложный уровень - для опытных игроков. Нестабильная экономика, частые кризисы, низкий базовый рейтинг.",
        'extreme': "Экстремальный уровень - для экспертов. Катастрофическая экономика, постоянные кризисы, экстремальные условия."
    }
    
    return descriptions.get(profile_name, "Неизвестный профиль") 