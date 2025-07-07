import random
import math
from typing import Dict, Any
from .solow_model import SolowModel, BudgetCalculator, DemographicCalculator


class EconomicEngine:
    """Движок экономической логики игры с моделью Солоу"""
    
    def __init__(self):
        self.base_gdp_growth = 2.0  # Базовый рост ВВП
        self.base_inflation = 3.0   # Базовая инфляция
        self.base_unemployment = 5.0  # Базовая безработица
        self.base_investments = 20.0  # Базовые инвестиции
        
        # Инициализируем модели
        self.solow_model = SolowModel()
        self.budget_calculator = BudgetCalculator()
        self.demographic_calculator = DemographicCalculator()
        
        # Базовые значения для новой игры
        self.initial_capital = 1000.0  # Начальный капитал (млн $)
        self.initial_population = 50.0  # Начальное население (млн человек)
        self.initial_technology = 1.0   # Начальный технологический уровень
        
    def calculate_indicators(self, parameters: Dict[str, float], 
                           previous_indicators: Dict[str, Any] = None,
                           previous_budget: Dict[str, Any] = None,
                           previous_demographics: Dict[str, Any] = None,
                           previous_production: Dict[str, Any] = None) -> Dict[str, Any]:
        """Рассчитать экономические показатели на основе параметров и модели Солоу"""
        
        # Получаем параметры управления
        interest_rate = parameters.get('interest_rate', 5.0)
        tax_rate = parameters.get('tax_rate', 20.0)
        government_spending = parameters.get('government_spending', 25.0)
        customs_duty = parameters.get('customs_duty', 5.0)
        
        # Бюджетные приоритеты
        education_priority = parameters.get('education_priority', 20.0)
        healthcare_priority = parameters.get('healthcare_priority', 20.0)
        defense_priority = parameters.get('defense_priority', 20.0)
        infrastructure_priority = parameters.get('infrastructure_priority', 20.0)
        social_priority = parameters.get('social_priority', 20.0)
        
        # Инициализируем базовые значения
        if previous_indicators:
            gdp_absolute = previous_indicators.get('gdp_absolute', 1000.0)
            inflation = previous_indicators.get('inflation', self.base_inflation)
            unemployment = previous_indicators.get('unemployment', self.base_unemployment)
            investments = previous_indicators.get('investments', self.base_investments)
            public_mood = previous_indicators.get('public_mood', 50.0)
            export_volume = previous_indicators.get('export_volume', 30.0)
            import_volume = previous_indicators.get('import_volume', 25.0)
        else:
            gdp_absolute = 1000.0
            inflation = self.base_inflation
            unemployment = self.base_unemployment
            investments = self.base_investments
            public_mood = 50.0
            export_volume = 30.0
            import_volume = 25.0
        
        # Получаем предыдущие данные для модели Солоу
        if previous_production:
            capital = previous_production.get('capital_stock', self.initial_capital)
            labor = previous_production.get('labor_force', self.initial_population * 0.65 * 0.75)
            technology = previous_production.get('technology_progress', self.initial_technology)
        else:
            capital = self.initial_capital
            labor = self.initial_population * 0.65 * 0.75  # 65% населения в трудоспособном возрасте, 75% участвуют
            technology = self.initial_technology
        
        # Получаем предыдущие демографические данные
        if previous_demographics:
            population = previous_demographics.get('population', self.initial_population)
            healthcare_quality = previous_demographics.get('healthcare_quality', 50.0)
        else:
            population = self.initial_population
            healthcare_quality = 50.0
        
        # Рассчитываем ВВП по модели Солоу
        gdp_absolute = self.solow_model.production_function(capital, labor, technology)
        
        # Рассчитываем рост по модели Солоу
        savings_rate = investments / 100  # Норма сбережений из инвестиций
        growth_data = self.solow_model.calculate_growth_rates(
            capital, labor, technology, savings_rate
        )
        
        # Обновляем капитал, труд и технологии
        new_capital = growth_data['new_capital']
        new_labor = growth_data['new_labor']
        new_technology = growth_data['new_technology']
        new_gdp = growth_data['new_gdp']
        
        # Рассчитываем темп роста ВВП
        gdp_growth = ((new_gdp / gdp_absolute) - 1) * 100 if gdp_absolute > 0 else 0
        
        # Рассчитываем демографические показатели
        demographic_data = self.demographic_calculator.calculate_population_growth(
            population, healthcare_quality, gdp_growth, unemployment
        )
        
        # Рассчитываем бюджетные показатели
        revenue = self.budget_calculator.calculate_revenue(
            gdp_absolute, tax_rate, export_volume, import_volume, customs_duty
        )
        
        # Расходы бюджета: government_spending (%) от ВВП
        total_spending = gdp_absolute * (government_spending / 100)
        # Распределяем по приоритетам (education, healthcare, defense, infrastructure, social)
        spending_priorities = {
            'education': education_priority,
            'healthcare': healthcare_priority,
            'defense': defense_priority,
            'infrastructure': infrastructure_priority,
            'social': social_priority
        }
        total_priority = sum(spending_priorities.values()) or 1
        spending = {k: total_spending * (v / total_priority) for k, v in spending_priorities.items()}
        spending['total_spending'] = total_spending

        # Баланс бюджета
        budget_balance = revenue['total_revenue'] - total_spending
        budget_deficit_percent = (budget_balance / revenue['total_revenue'] * 100) if revenue['total_revenue'] > 0 else 0
        
        # Влияние параметров управления на показатели
        self._apply_policy_effects(
            interest_rate, tax_rate, government_spending, customs_duty,
            inflation, unemployment, investments, public_mood
        )
        
        # Добавляем случайность
        inflation += random.uniform(-0.3, 0.3)
        unemployment += random.uniform(-0.2, 0.2)
        investments += random.uniform(-1.0, 1.0)
        
        # Ограничиваем значения
        inflation = max(0.0, min(50.0, inflation))
        unemployment = max(0.0, min(30.0, unemployment))
        investments = max(5.0, min(40.0, investments))
        public_mood = max(0.0, min(100.0, public_mood))
        
        # Рассчитываем рейтинг президента
        president_rating = self.calculate_president_rating(
            gdp_growth, inflation, unemployment, public_mood, 
            budget_deficit_percent, healthcare_quality
        )
        
        # Рассчитываем экспорт/импорт
        export_volume = 30.0 + (gdp_growth * 2) - (customs_duty * 0.5)
        import_volume = 25.0 + (gdp_growth * 1.5) + (customs_duty * 0.3)
        
        # Рассчитываем показатели производительности
        productivity = self.solow_model.calculate_productivity_indicators(
            new_capital, new_labor, new_technology, new_gdp
        )
        
        # Рассчитываем ВВП на душу населения
        gdp_per_capita = new_gdp / demographic_data['new_population'] if demographic_data['new_population'] > 0 else 0
        
        # Социальные показатели
        education_level = 10.0 + (spending.get('education', 0) / revenue['total_revenue'] * 100) * 0.1
        healthcare_quality = 50.0 + (spending.get('healthcare', 0) / revenue['total_revenue'] * 100) * 0.5
        social_stability = 70.0 + public_mood * 0.3 - unemployment * 0.5
        income_inequality = 30.0 + (tax_rate - 20.0) * 0.5  # Упрощенный расчет неравенства
        
        # Бюджетные данные
        budget_data = {
            'tax_revenue': round(revenue['tax_revenue'], 2),
            'customs_revenue': round(revenue['customs_revenue'], 2),
            'total_revenue': round(revenue['total_revenue'], 2),
            'education_spending': round(spending.get('education', 0), 2),
            'healthcare_spending': round(spending.get('healthcare', 0), 2),
            'defense_spending': round(spending.get('defense', 0), 2),
            'infrastructure_spending': round(spending.get('infrastructure', 0), 2),
            'social_spending': round(spending.get('social', 0), 2),
            'total_spending': round(total_spending, 2),
            'budget_balance': round(budget_balance, 2),
            'accumulated_reserves': 0.0  # TODO: рассчитать корректно
        }
        
        # --- Новые параметры банковской системы и денежной массы ---
        reserve_ratio = parameters.get('reserve_ratio', 0.1)
        refinance_rate = parameters.get('refinance_rate', 0.05)
        printing_press_active = parameters.get('printing_press_active', False)
        gold_reserves = previous_indicators.get('gold_reserves', 100.0) if previous_indicators else 100.0
        money_supply = previous_indicators.get('money_supply', 1000.0) if previous_indicators else 1000.0
        # --- Социальные трансферты ---
        social_transfers = parameters.get('social_transfers', 0.0)

        # --- Логика денежной массы и печатного станка ---
        # Если печатный станок включён, денежная масса увеличивается на 2% + дефицит бюджета
        if printing_press_active:
            emission = money_supply * 0.02 + max(0, -budget_balance)
            # Золотой запас снижает инфляционный эффект эмиссии
            gold_factor = 1.0 - min(gold_reserves / (money_supply + 1), 0.5)
            money_supply += emission
            inflation += emission / (money_supply + 1) * 10 * gold_factor
        else:
            # Без эмиссии денежная масса растёт медленно
            money_supply += money_supply * 0.005

        # --- Влияние резервных требований и ставки рефинансирования ---
        # Чем ниже reserve_ratio, тем выше мультипликатор кредитования
        credit_multiplier = 1 / reserve_ratio if reserve_ratio > 0 else 10
        # Ставка рефинансирования влияет на инвестиции и инфляцию
        investments += (0.05 - refinance_rate) * 10
        inflation += (0.05 - refinance_rate) * 2
        # Кредитование увеличивает инвестиции
        investments += (credit_multiplier - 10) * 0.5

        # --- Социальные трансферты ---
        # Увеличивают расходы бюджета, поддерживают настроение населения
        total_spending += social_transfers
        public_mood += social_transfers / (gdp_absolute + 1) * 100
        # Влияют на инфляцию при большом объёме
        if social_transfers > gdp_absolute * 0.2:
            inflation += (social_transfers - gdp_absolute * 0.2) / (gdp_absolute + 1) * 10

        # --- Обновляем бюджетные данные ---
        budget_data['social_transfers'] = round(social_transfers, 2)
        budget_data['total_spending'] = round(total_spending, 2)
        budget_data['budget_balance'] = round(revenue['total_revenue'] - total_spending, 2)

        # --- Демография: соц. трансферты на душу населения ---
        social_transfers_per_capita = social_transfers / (demographic_data['new_population'] + 1)

        # --- Возвращаем все новые параметры ---
        return {
            # Экономические показатели
            'gdp_growth': round(gdp_growth, 2),
            'gdp_absolute': round(new_gdp, 2),
            'inflation': round(inflation, 2),
            'unemployment': round(unemployment, 2),
            'investments': round(investments, 2),
            'president_rating': round(president_rating, 2),
            'public_mood': round(public_mood, 2),
            'export_volume': round(export_volume, 2),
            'import_volume': round(import_volume, 2),
            'money_supply': round(money_supply, 2),
            'gold_reserves': round(gold_reserves, 2),
            'reserve_ratio': round(reserve_ratio, 3),
            'refinance_rate': round(refinance_rate, 3),
            'printing_press_active': printing_press_active,
            'budget_data': budget_data,
            
            # Демографические данные
            'demographic_data': {
                'population': round(demographic_data['new_population'], 2),
                'natural_growth': round(demographic_data['natural_growth'], 2),
                'migration_growth': round(demographic_data['migration_growth'], 2),
                'life_expectancy': round(demographic_data['life_expectancy'], 2),
                'gdp_per_capita': round(gdp_per_capita, 2),
                'social_transfers_per_capita': round(social_transfers_per_capita, 2),
            },
            
            # Производственные данные (модель Солоу)
            'production_data': {
                'capital_stock': round(new_capital, 2),
                'labor_force': round(new_labor, 2),
                'technology_progress': round(new_technology, 2),
                'capital_intensity': round(productivity['capital_intensity'], 2),
                'labor_productivity': round(productivity['labor_productivity'], 2),
                'savings_rate': round(savings_rate * 100, 2),
                'depreciation_rate': round(self.solow_model.depreciation_rate * 100, 2),
                'capital_share': round(self.solow_model.alpha * 100, 2)
            },
            
            # Социальные данные
            'social_data': {
                'education_level': round(education_level, 2),
                'healthcare_quality': round(healthcare_quality, 2),
                'social_stability': round(social_stability, 2),
                'income_inequality': round(income_inequality, 2)
            }
        }
    
    def _apply_policy_effects(self, interest_rate: float, tax_rate: float, 
                            government_spending: float, customs_duty: float,
                            inflation: float, unemployment: float, 
                            investments: float, public_mood: float):
        """Применить влияние политических решений на показатели"""
        
        # Влияние процентной ставки
        interest_impact = (interest_rate - 5.0) / 10.0
        inflation -= interest_impact * 2.0
        unemployment += interest_impact * 1.0
        investments -= interest_impact * 2.0
        
        # Влияние налогов
        tax_impact = (tax_rate - 20.0) / 20.0
        investments -= tax_impact * 2.5
        public_mood -= tax_impact * 15.0
        
        # Влияние государственных расходов
        spending_impact = (government_spending - 25.0) / 25.0
        inflation += spending_impact * 1.5
        public_mood += spending_impact * 10.0
        
        # Влияние таможенных пошлин
        duty_impact = (customs_duty - 5.0) / 10.0
        inflation += duty_impact * 0.5
    
    def calculate_president_rating(self, gdp_growth: float, inflation: float, 
                                 unemployment: float, public_mood: float,
                                 budget_deficit: float, healthcare_quality: float) -> float:
        """Рассчитать рейтинг поддержки президента с учетом новых факторов"""
        base_rating = 50.0
        gdp_bonus = gdp_growth * 2.0
        inflation_penalty = inflation * 2.0
        unemployment_penalty = unemployment * 1.5
        mood_bonus = (public_mood - 50.0) * 0.3
        budget_bonus = -budget_deficit * 0.5  # Дефицит снижает рейтинг
        healthcare_bonus = (healthcare_quality - 50.0) * 0.2
        
        rating = (base_rating + gdp_bonus - inflation_penalty - unemployment_penalty + 
                 mood_bonus + budget_bonus + healthcare_bonus)
        
        return max(0.0, min(100.0, rating))
    
    def apply_event_impacts(self, indicators: Dict[str, Any], 
                          events: list) -> Dict[str, Any]:
        """Применить влияние событий на показатели"""
        result = indicators.copy()
        
        for event in events:
            # Влияние на экономические показатели
            result['gdp_growth'] += event.get('gdp_impact', 0.0)
            result['inflation'] += event.get('inflation_impact', 0.0)
            result['unemployment'] += event.get('unemployment_impact', 0.0)
            result['president_rating'] += event.get('rating_impact', 0.0)
            
            # Влияние на бюджет
            if 'budget_data' in result:
                result['budget_data']['budget_balance'] += event.get('budget_impact', 0.0)
            
            # Влияние на демографию
            if 'demographic_data' in result:
                population_change = event.get('population_impact', 0.0)
                result['demographic_data']['population'] += population_change
        
        # Ограничиваем значения после событий
        result['gdp_growth'] = max(-10.0, min(15.0, result['gdp_growth']))
        result['inflation'] = max(0.0, min(50.0, result['inflation']))
        result['unemployment'] = max(0.0, min(30.0, result['unemployment']))
        result['president_rating'] = max(0.0, min(100.0, result['president_rating']))
        
        return result 