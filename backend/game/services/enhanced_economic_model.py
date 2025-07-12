import math
import random
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from ..config.economic_config import *


@dataclass
class SectorData:
    """Данные сектора экономики"""
    capital: float
    labor: float
    technology: float
    output: float
    alpha: float  # капиталоёмкость


@dataclass
class EconomicParameters:
    """Параметры управления экономикой"""
    # Реальный сектор
    interest_rate: float = 5.0
    tax_rate: float = 20.0
    government_spending: float = 25.0
    customs_duty: float = 5.0
    
    # Бюджетные приоритеты
    education_priority: float = 20.0
    healthcare_priority: float = 20.0
    defense_priority: float = 20.0
    infrastructure_priority: float = 20.0
    social_priority: float = 20.0
    
    # Новая модель
    social_transfers: float = 0.0
    reserve_ratio: float = 0.1
    refinance_rate: float = 0.05
    printing_press_active: bool = False


class EnhancedEconomicModel:
    """Расширенная макроэкономическая модель с двухсекторной структурой"""
    
    def __init__(self):
        # Используем параметры из конфигурационного файла
        self.base_gdp_growth = TECHNOLOGY_GROWTH_RATE
        self.base_inflation = INITIAL_INFLATION
        self.base_unemployment = INITIAL_UNEMPLOYMENT
        self.natural_unemployment = INITIAL_UNEMPLOYMENT
        
        # Параметры закона Оукена
        self.okun_coefficient = 2.0
        
        # Параметры кривой Филлипса
        self.inflation_expectations_weight = 0.7
        self.output_gap_sensitivity = INFLATION_SENSITIVITY
        self.exchange_rate_sensitivity = 0.3
        
        # Параметры правила Тейлора
        self.inflation_target = INFLATION_TARGET
        self.neutral_rate = INITIAL_INTEREST_RATE
        self.taylor_pi_weight = 0.5
        self.taylor_y_weight = 0.5
        
        # Параметры внешней торговли
        self.base_export_share = 0.3
        self.base_import_share = 0.25
        self.exchange_rate_sensitivity_trade = EXCHANGE_RATE_VOLATILITY
        self.interest_rate_sensitivity_exchange = 0.1
        
        # Параметры демографии
        self.base_population_growth = POPULATION_GROWTH_RATE / 100
        self.base_migration = 0.005
        self.demographic_transition = 0.001
        self.migration_gdp_sensitivity = 0.1
        self.migration_unemployment_sensitivity = 0.05
        
        # Параметры кризисов
        self.crisis_probability = CRISIS_PROBABILITY_BASE
        
        # Начальные значения из конфига
        self.initial_capital_industry = INITIAL_GDP * INDUSTRY_SHARE
        self.initial_capital_services = INITIAL_GDP * SERVICES_SHARE
        self.initial_labor_industry = INDUSTRY_SHARE
        self.initial_labor_services = SERVICES_SHARE
        self.initial_technology_industry = 1.0
        self.initial_technology_services = 1.0
        self.initial_population = INITIAL_POPULATION
        self.initial_exchange_rate = 1.0
        self.initial_money_supply = INITIAL_GDP
        self.initial_gold_reserves = 100.0
        self.initial_external_debt = 0.0
        
    def calculate_sectoral_gdp(self, sector_data: Dict[str, SectorData]) -> Dict[str, float]:
        """Рассчитать ВВП по секторам (промышленность и услуги)"""
        results = {}
        
        for sector_name, sector in sector_data.items():
            # Производственная функция Кобба-Дугласа
            if sector.capital > 0 and sector.labor > 0 and sector.technology > 0:
                output = sector.technology * (sector.capital ** sector.alpha) * (sector.labor ** (1 - sector.alpha))
            else:
                output = 0.0
            results[f"{sector_name}_output"] = output
            
        # Общий ВВП
        total_gdp = sum(results.values())
        results['total_gdp'] = total_gdp
        
        return results
    
    def calculate_okun_law(self, gdp_growth: float, natural_unemployment: float) -> float:
        """Закон Оукена: связь между безработицей и ростом ВВП"""
        # y_gap = (Y - Y_pot) / Y_pot
        # u - u_nat = -θ * y_gap
        # где θ ≈ 2
        
        output_gap = gdp_growth / 100  # Преобразуем в долю
        unemployment = natural_unemployment - self.okun_coefficient * output_gap
        
        return max(0.0, min(30.0, unemployment))
    
    def calculate_phillips_curve(self, previous_inflation: float, output_gap: float, 
                                exchange_rate_change: float) -> float:
        """Кривая Филлипса с ожиданиями"""
        # π_t = β * π_{t-1} + κ * y_gap + γ * Δe + ε
        inflation = (self.inflation_expectations_weight * previous_inflation +
                    self.output_gap_sensitivity * output_gap +
                    self.exchange_rate_sensitivity * exchange_rate_change)
        
        # Добавляем случайный шок
        inflation += random.uniform(-0.5, 0.5)
        
        return max(0.0, min(50.0, inflation))
    
    def calculate_taylor_rule(self, current_inflation: float, output_gap: float) -> float:
        """Правило Тейлора для ключевой ставки"""
        # i_t = π_t + r* + φ_π(π_t - π*) + φ_y * y_gap
        interest_rate = (current_inflation + self.neutral_rate +
                        self.taylor_pi_weight * (current_inflation - self.inflation_target) +
                        self.taylor_y_weight * output_gap)
        
        return max(0.0, min(20.0, interest_rate))
    
    def calculate_exchange_rate(self, domestic_rate: float, world_rate: float, 
                               trade_balance: float, previous_rate: float) -> float:
        """Динамика обменного курса"""
        # Δe = ψ(i_dom - i_world) - η * TB + ε
        rate_differential = domestic_rate - world_rate
        exchange_rate_change = (self.interest_rate_sensitivity_exchange * rate_differential -
                               self.exchange_rate_sensitivity_trade * trade_balance)
        
        # Добавляем случайный шок
        exchange_rate_change += random.uniform(-0.05, 0.05)
        
        new_rate = previous_rate * (1 + exchange_rate_change)
        return max(0.1, min(10.0, new_rate))
    
    def calculate_trade_balance(self, gdp: float, exchange_rate: float, 
                               customs_duty: float, export_markup: float = 0.0, 
                               import_markup: float = 0.0) -> Dict[str, float]:
        """Торговый баланс"""
        # Экспорт и импорт зависят от ВВП и политики
        exports = self.base_export_share * gdp * (1 + export_markup) * (1 / exchange_rate)
        imports = self.base_import_share * gdp * (1 + import_markup) * exchange_rate
        
        # Таможенные поступления
        customs_revenue = (exports + imports) * (customs_duty / 100)
        
        trade_balance = exports - imports
        
        return {
            'exports': exports,
            'imports': imports,
            'trade_balance': trade_balance,
            'customs_revenue': customs_revenue
        }
    
    def calculate_budget(self, gdp: float, tax_rate: float, trade_data: Dict[str, float],
                        government_spending: float, social_transfers: float,
                        spending_priorities: Dict[str, float]) -> Dict[str, Any]:
        """Бюджетные показатели"""
        # Доходы
        tax_revenue = gdp * (tax_rate / 100)
        total_revenue = tax_revenue + trade_data['customs_revenue']
        
        # Расходы
        total_spending = gdp * (government_spending / 100) + social_transfers
        
        # Распределение по приоритетам
        total_priority = sum(spending_priorities.values()) or 1
        spending = {k: total_spending * (v / total_priority) for k, v in spending_priorities.items()}
        
        budget_balance = total_revenue - total_spending
        
        return {
            'tax_revenue': tax_revenue,
            'total_revenue': total_revenue,
            'total_spending': total_spending,
            'budget_balance': budget_balance,
            'spending_breakdown': spending,
            'social_transfers': social_transfers
        }
    
    def calculate_demographics(self, population: float, gdp_per_capita: float, 
                             unemployment: float, healthcare_quality: float) -> Dict[str, float]:
        """Демографические показатели"""
        # Естественный прирост зависит от дохода на душу населения
        natural_growth = self.base_population_growth * (1 - self.demographic_transition * gdp_per_capita)
        
        # Миграция зависит от экономических условий
        migration_growth = self.base_migration * (1 + self.migration_gdp_sensitivity * (gdp_per_capita / 1000) -
                                                self.migration_unemployment_sensitivity * unemployment)
        
        # Общий рост населения
        total_growth = natural_growth + migration_growth
        new_population = population * (1 + total_growth)
        
        # Ожидаемая продолжительность жизни зависит от качества здравоохранения
        life_expectancy = 70 + (healthcare_quality - 50) * 0.2
        
        return {
            'population': new_population,
            'natural_growth': natural_growth * 100,  # в процентах
            'migration_growth': migration_growth * 100,  # в процентах
            'total_growth': total_growth * 100,  # в процентах
            'life_expectancy': life_expectancy
        }
    
    def calculate_public_mood(self, previous_mood: float, gdp_growth: float, 
                            social_transfers_per_capita: float, unemployment: float) -> float:
        """Настроение населения"""
        # Настроение зависит от роста ВВП, социальных трансфертов и безработицы
        mood_change = (gdp_growth * 0.5 +  # рост ВВП улучшает настроение
                      social_transfers_per_capita * 0.1 -  # трансферты улучшают настроение
                      unemployment * 0.3)  # безработица ухудшает настроение
        
        new_mood = previous_mood + mood_change
        return max(0.0, min(100.0, new_mood))
    
    def generate_crisis(self) -> Optional[Dict[str, float]]:
        """Генерация кризиса или шока"""
        if random.random() < self.crisis_probability:
            crisis_types = [
                # Шок предложения
                {'name': 'supply_shock', 'gdp_impact': -1.0, 'inflation_impact': 3.0, 'unemployment_impact': 1.0},
                # Финансовый кризис
                {'name': 'financial_crisis', 'gdp_impact': -2.0, 'unemployment_impact': 2.0, 'debt_impact': 5.0},
                # Санкции
                {'name': 'sanctions', 'export_impact': -10.0, 'exchange_rate_impact': 5.0, 'gdp_impact': -0.5},
                # Природная катастрофа
                {'name': 'natural_disaster', 'gdp_impact': -1.5, 'budget_impact': -50.0, 'population_impact': -0.1},
                # Социальные протесты
                {'name': 'social_protests', 'mood_impact': -10.0, 'gdp_impact': -0.5, 'unemployment_impact': 1.0}
            ]
            
            crisis = random.choice(crisis_types)
            return crisis
        
        return None
    
    def calculate_indicators(self, parameters: EconomicParameters,
                           previous_indicators: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Основной метод расчета всех экономических показателей"""
        
        # Инициализируем предыдущие значения
        if previous_indicators:
            prev_gdp = previous_indicators.get('total_gdp', 1000.0)
            prev_inflation = previous_indicators.get('inflation', self.base_inflation)
            prev_unemployment = previous_indicators.get('unemployment', self.base_unemployment)
            prev_exchange_rate = previous_indicators.get('exchange_rate', self.initial_exchange_rate)
            prev_money_supply = previous_indicators.get('money_supply', self.initial_money_supply)
            prev_gold_reserves = previous_indicators.get('gold_reserves', self.initial_gold_reserves)
            prev_external_debt = previous_indicators.get('external_debt', self.initial_external_debt)
            prev_population = previous_indicators.get('population', self.initial_population)
            prev_mood = previous_indicators.get('public_mood', 50.0)
            
            # Секторальные данные
            prev_industry_capital = previous_indicators.get('industry_capital', self.initial_capital_industry)
            prev_services_capital = previous_indicators.get('services_capital', self.initial_capital_services)
            prev_industry_labor = previous_indicators.get('industry_labor', self.initial_labor_industry)
            prev_services_labor = previous_indicators.get('services_labor', self.initial_labor_services)
            prev_industry_tech = previous_indicators.get('industry_technology', self.initial_technology_industry)
            prev_services_tech = previous_indicators.get('services_technology', self.initial_technology_services)
        else:
            # Начальные значения
            prev_gdp = 1000.0
            prev_inflation = self.base_inflation
            prev_unemployment = self.base_unemployment
            prev_exchange_rate = self.initial_exchange_rate
            prev_money_supply = self.initial_money_supply
            prev_gold_reserves = self.initial_gold_reserves
            prev_external_debt = self.initial_external_debt
            prev_population = self.initial_population
            prev_mood = 50.0
            
            prev_industry_capital = self.initial_capital_industry
            prev_services_capital = self.initial_capital_services
            prev_industry_labor = self.initial_labor_industry
            prev_services_labor = self.initial_labor_services
            prev_industry_tech = self.initial_technology_industry
            prev_services_tech = self.initial_technology_services
        
        # 1. Рассчитываем секторальный ВВП
        sector_data = {
            'industry': SectorData(
                capital=prev_industry_capital,
                labor=prev_industry_labor * prev_population,  # Абсолютная численность
                technology=prev_industry_tech,
                output=0.0,
                alpha=0.3
            ),
            'services': SectorData(
                capital=prev_services_capital,
                labor=prev_services_labor * prev_population,  # Абсолютная численность
                technology=prev_services_tech,
                output=0.0,
                alpha=0.4
            )
        }
        
        sectoral_output = self.calculate_sectoral_gdp(sector_data)
        total_gdp = sectoral_output['total_gdp']
        
        # 2. Рассчитываем рост ВВП
        gdp_growth = ((total_gdp / prev_gdp) - 1) * 100 if prev_gdp > 0 else 0
        
        # 3. Закон Оукена
        unemployment = self.calculate_okun_law(gdp_growth, self.natural_unemployment)
        
        # 4. Output gap для кривой Филлипса
        output_gap = gdp_growth / 100
        
        # 5. Кривая Филлипса
        inflation = self.calculate_phillips_curve(prev_inflation, output_gap, 0.0)  # Пока без изменения курса
        
        # 6. Правило Тейлора
        interest_rate = self.calculate_taylor_rule(inflation, output_gap)
        
        # 7. Внешняя торговля
        trade_data = self.calculate_trade_balance(total_gdp, prev_exchange_rate, parameters.customs_duty)
        
        # 8. Обменный курс
        world_rate = 3.0  # Фиксированная мировая ставка
        exchange_rate = self.calculate_exchange_rate(interest_rate, world_rate, 
                                                   trade_data['trade_balance'] / total_gdp, 
                                                   prev_exchange_rate)
        
        # 9. Бюджет
        spending_priorities = {
            'education': parameters.education_priority,
            'healthcare': parameters.healthcare_priority,
            'defense': parameters.defense_priority,
            'infrastructure': parameters.infrastructure_priority,
            'social': parameters.social_priority
        }
        
        budget_data = self.calculate_budget(total_gdp, parameters.tax_rate, trade_data,
                                          parameters.government_spending, parameters.social_transfers,
                                          spending_priorities)
        
        # 10. Демография
        gdp_per_capita = total_gdp / prev_population if prev_population > 0 else 0
        healthcare_spending = budget_data['spending_breakdown']['healthcare'] if isinstance(budget_data['spending_breakdown'], dict) else 50.0
        demographic_data = self.calculate_demographics(prev_population, gdp_per_capita, 
                                                     unemployment, healthcare_spending)
        
        # 11. Настроение населения
        social_transfers_per_capita = parameters.social_transfers / prev_population if prev_population > 0 else 0
        public_mood = self.calculate_public_mood(prev_mood, gdp_growth, social_transfers_per_capita, unemployment)
        
        # 12. Денежная масса и инфляция
        money_supply = prev_money_supply
        if parameters.printing_press_active:
            emission = money_supply * 0.02 + max(0, -budget_data['budget_balance'])
            money_supply += emission
            inflation += emission / (money_supply + 1) * 10
        
        # 13. Внешний долг и золото
        gold_reserves = prev_gold_reserves
        external_debt = prev_external_debt
        
        # Компенсация дефицита бюджета
        deficit = -budget_data['budget_balance'] if budget_data['budget_balance'] < 0 else 0
        if deficit > 0:
            if gold_reserves >= deficit:
                gold_reserves -= deficit
            else:
                debt_increase = deficit - gold_reserves
                gold_reserves = 0
                external_debt += debt_increase
        
        # Обслуживание долга
        debt_repayment = external_debt * 0.05
        debt_interest = external_debt * 0.02
        external_debt = max(0.0, external_debt - debt_repayment + debt_interest)
        
        # 14. Генерируем кризис
        crisis = self.generate_crisis()
        if crisis:
            # Применяем эффекты кризиса
            gdp_growth += crisis.get('gdp_impact', 0.0)
            inflation += crisis.get('inflation_impact', 0.0)
            unemployment += crisis.get('unemployment_impact', 0.0)
            public_mood += crisis.get('mood_impact', 0.0)
            external_debt += crisis.get('debt_impact', 0.0)
            demographic_data['population'] += crisis.get('population_impact', 0.0)
        
        # 15. Рейтинг президента
        healthcare_quality = budget_data['spending_breakdown']['healthcare'] if isinstance(budget_data['spending_breakdown'], dict) else 50.0
        president_rating = self.calculate_president_rating(gdp_growth, inflation, unemployment, 
                                                         public_mood, budget_data['budget_balance'], 
                                                         healthcare_quality)
        
        # Возвращаем все показатели
        return {
            # Основные экономические показатели
            'gdp_growth': round(gdp_growth, 2),
            'gdp_absolute': round(total_gdp, 2),
            'total_gdp': round(total_gdp, 2),
            'inflation': round(inflation, 2),
            'unemployment': round(unemployment, 2),
            'interest_rate': round(interest_rate, 2),
            'president_rating': round(president_rating, 2),
            'public_mood': round(public_mood, 2),
            
            # Секторальные данные
            'industry_output': round(sectoral_output['industry_output'], 2),
            'services_output': round(sectoral_output['services_output'], 2),
            'industry_capital': round(prev_industry_capital * 1.02, 2),  # Простой рост капитала
            'services_capital': round(prev_services_capital * 1.02, 2),
            'industry_labor': round(prev_industry_labor, 3),
            'services_labor': round(prev_services_labor, 3),
            'industry_technology': round(prev_industry_tech * 1.005, 3),
            'services_technology': round(prev_services_tech * 1.005, 3),
            
            # Внешняя торговля и курс
            'exports': round(trade_data['exports'], 2),
            'imports': round(trade_data['imports'], 2),
            'export_volume': round(trade_data['exports'], 2),
            'import_volume': round(trade_data['imports'], 2),
            'trade_balance': round(trade_data['trade_balance'], 2),
            'exchange_rate': round(exchange_rate, 3),
            
            # Бюджетные данные
            'tax_revenue': round(budget_data['tax_revenue'], 2),
            'total_revenue': round(budget_data['total_revenue'], 2),
            'total_spending': round(budget_data['total_spending'], 2),
            'budget_balance': round(budget_data['budget_balance'], 2),
            'social_transfers': round(budget_data['social_transfers'], 2),
            'education_spending': round(budget_data['spending_breakdown']['education'], 2) if isinstance(budget_data['spending_breakdown'], dict) else 0.0,
            'healthcare_spending': round(budget_data['spending_breakdown']['healthcare'], 2) if isinstance(budget_data['spending_breakdown'], dict) else 0.0,
            'defense_spending': round(budget_data['spending_breakdown']['defense'], 2) if isinstance(budget_data['spending_breakdown'], dict) else 0.0,
            'infrastructure_spending': round(budget_data['spending_breakdown']['infrastructure'], 2) if isinstance(budget_data['spending_breakdown'], dict) else 0.0,
            'social_spending': round(budget_data['spending_breakdown']['social'], 2) if isinstance(budget_data['spending_breakdown'], dict) else 0.0,
            
            # Демографические данные
            'population': round(demographic_data['population'], 2),
            'natural_growth': round(demographic_data['natural_growth'], 2),
            'migration_growth': round(demographic_data['migration_growth'], 2),
            'life_expectancy': round(demographic_data['life_expectancy'], 1),
            'gdp_per_capita': round(gdp_per_capita, 2),
            
            # Финансовые данные
            'money_supply': round(money_supply, 2),
            'gold_reserves': round(gold_reserves, 2),
            'external_debt': round(external_debt, 2),
            'debt_repayment': round(debt_repayment, 2),
            'debt_interest': round(debt_interest, 2),
            
            # Кризисные данные
            'crisis': crisis,
            # Параметры модели
            'model_type': 'enhanced',
            # Инвестиции (сумма прироста капитала)
            'investments': round((prev_industry_capital * 0.02) + (prev_services_capital * 0.02), 2),
            # Бюджет для API
            'budget': {
                'total_revenue': round(budget_data['total_revenue'], 2),
                'total_spending': round(budget_data['total_spending'], 2),
                'budget_balance': round(budget_data['budget_balance'], 2),
                'accumulated_reserves': round(budget_data.get('accumulated_reserves', 0.0), 2),
                'social_transfers': round(budget_data['social_transfers'], 2),
                'external_debt': round(external_debt, 2),
            }
        
        } 

    def calculate_president_rating(self, gdp_growth: float, inflation: float, 
                                 unemployment: float, public_mood: float,
                                 budget_balance: float, healthcare_quality: float) -> float:
        """Рассчитать рейтинг президента"""
        # Базовый рейтинг
        base_rating = 50.0
        
        # Влияние экономических показателей
        gdp_impact = gdp_growth * 2.0  # Рост ВВП положительно влияет
        inflation_impact = -inflation * 1.5  # Инфляция отрицательно влияет
        unemployment_impact = -unemployment * 2.0  # Безработица отрицательно влияет
        
        # Влияние настроения населения
        mood_impact = (public_mood - 50.0) * 0.5
        
        # Влияние бюджета
        budget_impact = 0.0
        if budget_balance > 0:
            budget_impact = 5.0  # Профицит положительно влияет
        elif budget_balance < -10:
            budget_impact = -10.0  # Большой дефицит отрицательно влияет
        
        # Влияние качества здравоохранения
        healthcare_impact = (healthcare_quality - 50.0) * 0.3
        
        # Итоговый рейтинг
        rating = (base_rating + gdp_impact + inflation_impact + unemployment_impact + 
                 mood_impact + budget_impact + healthcare_impact)
        
        return max(0.0, min(100.0, rating)) 

    def initialize_economy(self, initial_params: Dict[str, float]) -> Dict[str, float]:
        """Инициализация экономики с начальными параметрами"""
        gdp = initial_params.get('gdp', 1000000)
        population = initial_params.get('population', 100000) / 1000000  # Конвертируем в миллионы
        inflation = initial_params.get('inflation', 2.0)
        unemployment = initial_params.get('unemployment', 5.0)
        budget_deficit = initial_params.get('budget_deficit', 0.0)
        
        # Создаем начальные сектора
        sector_data = {
            'industry': SectorData(
                capital=gdp * 0.6,
                labor=0.35,
                technology=1.0,
                output=gdp * 0.6,
                alpha=0.4
            ),
            'services': SectorData(
                capital=gdp * 0.4,
                labor=0.65,
                technology=1.0,
                output=gdp * 0.4,
                alpha=0.3
            )
        }
        
        # Рассчитываем секторальный ВВП
        sectoral_gdp = self.calculate_sectoral_gdp(sector_data)
        
        # Рассчитываем торговый баланс
        trade_data = self.calculate_trade_balance(gdp, 1.0, 5.0)
        
        # Рассчитываем бюджет
        spending_priorities = {
            'education': 20.0,
            'healthcare': 20.0,
            'defense': 20.0,
            'infrastructure': 20.0,
            'social': 20.0
        }
        
        budget_data = self.calculate_budget(
            gdp, 20.0, trade_data, 25.0, gdp * 0.1, spending_priorities
        )
        
        # Рассчитываем демографию
        gdp_per_capita = gdp / population
        demographics = self.calculate_demographics(population, gdp_per_capita, unemployment, 50.0)
        
        # Рассчитываем настроение населения
        public_mood = self.calculate_public_mood(50.0, 0.0, gdp * 0.1 / population, unemployment)
        
        # Рассчитываем рейтинг президента
        president_rating = self.calculate_president_rating(0.0, inflation, unemployment, public_mood, budget_data['budget_balance'], 50.0)
        
        # Возвращаем все показатели
        return {
            'gdp_absolute': gdp,
            'gdp_growth': 0.0,  # Начальный рост
            'inflation': inflation,
            'unemployment': unemployment,
            'interest_rate': 5.0,
            'exchange_rate': 1.0,
            'president_rating': president_rating,
            'public_mood': public_mood,
            'industry_output': sectoral_gdp['industry_output'],
            'services_output': sectoral_gdp['services_output'],
            'exports': trade_data['exports'],
            'imports': trade_data['imports'],
            'trade_balance': trade_data['trade_balance'],
            'tax_revenue': budget_data['tax_revenue'],
            'total_revenue': budget_data['total_revenue'],
            'total_spending': budget_data['total_spending'],
            'budget_balance': budget_data['budget_balance'],
            'social_transfers': gdp * 0.1,
            'population': population,
            'money_supply': gdp * 0.8,
            'gold_reserves': 100.0,
            'reserve_ratio': 0.1,
            'refinance_rate': 0.05,
            'external_debt': 0.0,
            'investments': 20.0,
            'education_spending': budget_data['total_spending'] * 0.2,
            'healthcare_spending': budget_data['total_spending'] * 0.2,
            'defense_spending': budget_data['total_spending'] * 0.2,
            'infrastructure_spending': budget_data['total_spending'] * 0.2,
            'social_spending': budget_data['total_spending'] * 0.2,
            'accumulated_reserves': gdp * 0.05
        } 