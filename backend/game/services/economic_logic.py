import random
import math
from typing import Dict, Any


class EconomicEngine:
    """Движок экономической логики игры"""
    
    def __init__(self):
        self.base_gdp_growth = 2.0  # Базовый рост ВВП
        self.base_inflation = 3.0   # Базовая инфляция
        self.base_unemployment = 5.0  # Базовая безработица
        self.base_investments = 20.0  # Базовые инвестиции
    
    def calculate_indicators(self, parameters: Dict[str, float], 
                           previous_indicators: Dict[str, float] = None) -> Dict[str, float]:
        """Рассчитать экономические показатели на основе параметров"""
        
        # Получаем параметры управления
        interest_rate = parameters.get('interest_rate', 5.0)
        tax_rate = parameters.get('tax_rate', 20.0)
        government_spending = parameters.get('government_spending', 25.0)
        customs_duty = parameters.get('customs_duty', 5.0)
        
        # Базовые значения
        if previous_indicators:
            gdp_growth = previous_indicators.get('gdp_growth', self.base_gdp_growth)
            inflation = previous_indicators.get('inflation', self.base_inflation)
            unemployment = previous_indicators.get('unemployment', self.base_unemployment)
            investments = previous_indicators.get('investments', self.base_investments)
            public_mood = previous_indicators.get('public_mood', 50.0)
        else:
            gdp_growth = self.base_gdp_growth
            inflation = self.base_inflation
            unemployment = self.base_unemployment
            investments = self.base_investments
            public_mood = 50.0
        
        # Влияние процентной ставки
        interest_impact = (interest_rate - 5.0) / 10.0  # Нормализация к базовой ставке
        gdp_growth -= interest_impact * 1.5  # Высокая ставка снижает рост
        inflation -= interest_impact * 2.0    # Высокая ставка снижает инфляцию
        unemployment += interest_impact * 1.0  # Высокая ставка увеличивает безработицу
        investments -= interest_impact * 2.0   # Высокая ставка снижает инвестиции
        
        # Влияние налогов
        tax_impact = (tax_rate - 20.0) / 20.0  # Нормализация к базовой ставке
        gdp_growth -= tax_impact * 1.0         # Высокие налоги снижают рост
        investments -= tax_impact * 2.5        # Высокие налоги снижают инвестиции
        public_mood -= tax_impact * 15.0       # Высокие налоги снижают настроение
        
        # Влияние государственных расходов
        spending_impact = (government_spending - 25.0) / 25.0
        gdp_growth += spending_impact * 2.0    # Расходы стимулируют рост
        inflation += spending_impact * 1.5     # Расходы могут вызвать инфляцию
        public_mood += spending_impact * 10.0  # Расходы улучшают настроение
        
        # Влияние таможенных пошлин
        duty_impact = (customs_duty - 5.0) / 10.0
        gdp_growth -= duty_impact * 0.5        # Пошлины немного снижают рост
        inflation += duty_impact * 0.5         # Пошлины немного повышают инфляцию
        
        # Добавляем случайность
        gdp_growth += random.uniform(-0.5, 0.5)
        inflation += random.uniform(-0.3, 0.3)
        unemployment += random.uniform(-0.2, 0.2)
        investments += random.uniform(-1.0, 1.0)
        
        # Ограничиваем значения
        gdp_growth = max(-10.0, min(15.0, gdp_growth))
        inflation = max(0.0, min(50.0, inflation))
        unemployment = max(0.0, min(30.0, unemployment))
        investments = max(5.0, min(40.0, investments))
        public_mood = max(0.0, min(100.0, public_mood))
        
        # Рассчитываем рейтинг президента
        president_rating = self.calculate_president_rating(
            gdp_growth, inflation, unemployment, public_mood
        )
        
        # Рассчитываем экспорт/импорт
        export_volume = 30.0 + (gdp_growth * 2) - (customs_duty * 0.5)
        import_volume = 25.0 + (gdp_growth * 1.5) + (customs_duty * 0.3)
        
        return {
            'gdp_growth': round(gdp_growth, 2),
            'inflation': round(inflation, 2),
            'unemployment': round(unemployment, 2),
            'investments': round(investments, 2),
            'president_rating': round(president_rating, 2),
            'public_mood': round(public_mood, 2),
            'export_volume': round(export_volume, 2),
            'import_volume': round(import_volume, 2),
        }
    
    def calculate_president_rating(self, gdp_growth: float, inflation: float, 
                                 unemployment: float, public_mood: float) -> float:
        """Рассчитать рейтинг поддержки президента"""
        # Формула из ТЗ: rating = 50 + gdp_growth * 2 - inflation * 2 - unemployment * 1.5 + public_mood * 1.5
        base_rating = 50.0
        gdp_bonus = gdp_growth * 2.0
        inflation_penalty = inflation * 2.0
        unemployment_penalty = unemployment * 1.5
        mood_bonus = (public_mood - 50.0) * 0.3  # Нормализованный бонус от настроения
        
        rating = base_rating + gdp_bonus - inflation_penalty - unemployment_penalty + mood_bonus
        
        return max(0.0, min(100.0, rating))
    
    def apply_event_impacts(self, indicators: Dict[str, float], 
                          events: list) -> Dict[str, float]:
        """Применить влияние событий на показатели"""
        result = indicators.copy()
        
        for event in events:
            result['gdp_growth'] += event.get('gdp_impact', 0.0)
            result['inflation'] += event.get('inflation_impact', 0.0)
            result['unemployment'] += event.get('unemployment_impact', 0.0)
            result['president_rating'] += event.get('rating_impact', 0.0)
        
        # Ограничиваем значения после событий
        result['gdp_growth'] = max(-10.0, min(15.0, result['gdp_growth']))
        result['inflation'] = max(0.0, min(50.0, result['inflation']))
        result['unemployment'] = max(0.0, min(30.0, result['unemployment']))
        result['president_rating'] = max(0.0, min(100.0, result['president_rating']))
        
        return result 