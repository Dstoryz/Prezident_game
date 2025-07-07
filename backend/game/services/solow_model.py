import math
from typing import Dict, Any


class SolowModel:
    """Модель Солоу для расчета экономического роста"""
    
    def __init__(self):
        # Параметры модели Солоу
        self.alpha = 0.3  # Доля капитала в производстве (обычно 0.3-0.4)
        self.depreciation_rate = 0.05  # Норма амортизации (5% в год)
        self.technology_growth = 0.02  # Экзогенный рост технологий (2% в год)
        self.population_growth = 0.01  # Рост населения (1% в год)
        
        # Базовые значения
        self.base_capital = 1000.0  # Базовый капитал (млн $)
        self.base_labor = 50.0      # Базовая рабочая сила (млн человек)
        self.base_technology = 1.0  # Базовый технологический уровень
        
    def production_function(self, capital: float, labor: float, technology: float) -> float:
        """
        Производственная функция Кобба-Дугласа: Y = A * K^α * L^(1-α)
        
        Args:
            capital: Капитал (млн $)
            labor: Рабочая сила (млн человек)
            technology: Технологический прогресс (фактор A)
            
        Returns:
            ВВП (млн $)
        """
        if capital <= 0 or labor <= 0 or technology <= 0:
            return 0.0
            
        return technology * (capital ** self.alpha) * (labor ** (1 - self.alpha))
    
    def capital_dynamics(self, capital: float, output: float, savings_rate: float) -> float:
        """
        Динамика капитала: dK/dt = s*Y - δ*K
        
        Args:
            capital: Текущий капитал (млн $)
            output: ВВП (млн $)
            savings_rate: Норма сбережений (доля от 0 до 1)
            
        Returns:
            Изменение капитала (млн $)
        """
        investment = savings_rate * output
        depreciation = self.depreciation_rate * capital
        return investment - depreciation
    
    def calculate_steady_state(self, savings_rate: float, population_growth: float) -> Dict[str, float]:
        """
        Расчет устойчивого состояния модели Солоу
        
        Args:
            savings_rate: Норма сбережений
            population_growth: Рост населения
            
        Returns:
            Словарь с параметрами устойчивого состояния
        """
        # В устойчивом состоянии: s*f(k) = (δ+n)*k
        # где k = K/L - капиталовооруженность
        # f(k) = A*k^α - производственная функция на душу населения
        
        # Решаем уравнение: s*A*k^α = (δ+n)*k
        # k^(α-1) = s*A/(δ+n)
        # k = (s*A/(δ+n))^(1/(1-α))
        
        effective_depreciation = self.depreciation_rate + population_growth
        
        if effective_depreciation <= 0:
            return {
                'capital_intensity': 0.0,
                'output_per_capita': 0.0,
                'consumption_per_capita': 0.0
            }
        
        capital_intensity = (savings_rate * self.base_technology / effective_depreciation) ** (1 / (1 - self.alpha))
        output_per_capita = self.base_technology * (capital_intensity ** self.alpha)
        consumption_per_capita = (1 - savings_rate) * output_per_capita
        
        return {
            'capital_intensity': capital_intensity,
            'output_per_capita': output_per_capita,
            'consumption_per_capita': consumption_per_capita
        }
    
    def calculate_growth_rates(self, current_capital: float, current_labor: float, 
                             current_technology: float, savings_rate: float) -> Dict[str, float]:
        """
        Расчет темпов роста экономических показателей
        
        Args:
            current_capital: Текущий капитал
            current_labor: Текущая рабочая сила
            current_technology: Текущий технологический уровень
            savings_rate: Норма сбережений
            
        Returns:
            Словарь с темпами роста
        """
        # Текущий ВВП
        current_gdp = self.production_function(current_capital, current_labor, current_technology)
        
        # Изменение капитала
        capital_change = self.capital_dynamics(current_capital, current_gdp, savings_rate)
        new_capital = current_capital + capital_change
        
        # Рост технологий
        new_technology = current_technology * (1 + self.technology_growth)
        
        # Рост населения
        new_labor = current_labor * (1 + self.population_growth)
        
        # Новый ВВП
        new_gdp = self.production_function(new_capital, new_labor, new_technology)
        
        # Темпы роста
        gdp_growth = ((new_gdp / current_gdp) - 1) * 100 if current_gdp > 0 else 0
        capital_growth = ((new_capital / current_capital) - 1) * 100 if current_capital > 0 else 0
        labor_growth = self.population_growth * 100
        technology_growth = self.technology_growth * 100
        
        return {
            'gdp_growth': gdp_growth,
            'capital_growth': capital_growth,
            'labor_growth': labor_growth,
            'technology_growth': technology_growth,
            'new_capital': new_capital,
            'new_labor': new_labor,
            'new_technology': new_technology,
            'new_gdp': new_gdp
        }
    
    def calculate_productivity_indicators(self, capital: float, labor: float, 
                                        technology: float, gdp: float) -> Dict[str, float]:
        """
        Расчет показателей производительности
        
        Args:
            capital: Капитал
            labor: Рабочая сила
            technology: Технологический уровень
            gdp: ВВП
            
        Returns:
            Словарь с показателями производительности
        """
        capital_intensity = capital / labor if labor > 0 else 0
        labor_productivity = gdp / labor if labor > 0 else 0
        capital_productivity = gdp / capital if capital > 0 else 0
        
        return {
            'capital_intensity': capital_intensity,
            'labor_productivity': labor_productivity,
            'capital_productivity': capital_productivity,
            'technology_level': technology
        }


class BudgetCalculator:
    """Калькулятор бюджетных показателей"""
    
    def __init__(self):
        self.base_tax_rate = 0.20  # Базовая налоговая ставка
        self.base_customs_rate = 0.05  # Базовая ставка таможенных пошлин
        
    def calculate_revenue(self, gdp: float, tax_rate: float, 
                         exports: float, imports: float, customs_duty: float) -> Dict[str, float]:
        """
        Расчет доходов бюджета
        
        Args:
            gdp: ВВП (млн $)
            tax_rate: Налоговая ставка (%)
            exports: Экспорт (% от ВВП)
            imports: Импорт (% от ВВП)
            customs_duty: Таможенные пошлины (%)
            
        Returns:
            Словарь с доходами бюджета
        """
        # Налоговые поступления
        tax_revenue = gdp * (tax_rate / 100)
        
        # Таможенные поступления
        trade_volume = (exports + imports) * gdp / 100
        customs_revenue = trade_volume * (customs_duty / 100)
        
        # Общие доходы
        total_revenue = tax_revenue + customs_revenue
        
        return {
            'tax_revenue': tax_revenue,
            'customs_revenue': customs_revenue,
            'total_revenue': total_revenue
        }
    
    def calculate_spending(self, total_revenue: float, priorities: Dict[str, float]) -> Dict[str, float]:
        """
        Расчет расходов бюджета по приоритетам
        
        Args:
            total_revenue: Общие доходы
            priorities: Словарь с приоритетами расходов (%)
            
        Returns:
            Словарь с расходами бюджета
        """
        # Нормализуем приоритеты (сумма должна быть 100%)
        total_priority = sum(priorities.values())
        if total_priority > 0:
            normalized_priorities = {k: v / total_priority for k, v in priorities.items()}
        else:
            normalized_priorities = {k: 0.0 for k in priorities.keys()}
        
        # Рассчитываем расходы
        spending = {}
        for category, priority in normalized_priorities.items():
            spending[category] = total_revenue * priority
        
        # Общие расходы
        total_spending = sum(spending.values())
        spending['total_spending'] = total_spending
        
        return spending
    
    def calculate_budget_balance(self, revenue: Dict[str, float], 
                               spending: Dict[str, float]) -> Dict[str, float]:
        """
        Расчет бюджетного баланса
        
        Args:
            revenue: Доходы бюджета
            spending: Расходы бюджета
            
        Returns:
            Словарь с бюджетным балансом
        """
        total_revenue = revenue.get('total_revenue', 0)
        total_spending = spending.get('total_spending', 0)
        
        budget_balance = total_revenue - total_spending
        budget_deficit_percent = (budget_balance / total_revenue * 100) if total_revenue > 0 else 0
        
        return {
            'budget_balance': budget_balance,
            'budget_deficit_percent': budget_deficit_percent,
            'is_deficit': budget_balance < 0
        }


class DemographicCalculator:
    """Калькулятор демографических показателей"""
    
    def __init__(self):
        self.base_natural_growth = 0.5  # Базовый естественный прирост (%)
        self.base_life_expectancy = 70.0  # Базовая продолжительность жизни (лет)
        self.base_migration = 0.1  # Базовая миграция (%)
        
    def calculate_population_growth(self, current_population: float, 
                                  healthcare_quality: float, gdp_growth: float, 
                                  unemployment: float) -> Dict[str, float]:
        """
        Расчет роста населения
        
        Args:
            current_population: Текущая численность населения
            healthcare_quality: Качество здравоохранения (0-100)
            gdp_growth: Рост ВВП (%)
            unemployment: Безработица (%)
            
        Returns:
            Словарь с демографическими показателями
        """
        # Естественный прирост зависит от качества здравоохранения
        natural_growth = self.base_natural_growth * (1 + (healthcare_quality - 50) * 0.01)
        
        # Миграционный прирост зависит от экономических условий
        migration_growth = self.base_migration * (1 + gdp_growth * 0.1 - unemployment * 0.05)
        
        # Общий прирост
        total_growth = natural_growth + migration_growth
        
        # Изменение населения
        population_change = current_population * total_growth / 100
        new_population = current_population + population_change
        
        # Продолжительность жизни
        life_expectancy = self.base_life_expectancy + healthcare_quality * 0.1
        
        return {
            'natural_growth': natural_growth,
            'migration_growth': migration_growth,
            'total_growth': total_growth,
            'population_change': population_change,
            'new_population': new_population,
            'life_expectancy': life_expectancy
        }
    
    def calculate_labor_force(self, population: float, age_structure: Dict[str, float] = None) -> float:
        """
        Расчет рабочей силы
        
        Args:
            population: Население
            age_structure: Возрастная структура (опционально)
            
        Returns:
            Рабочая сила (млн человек)
        """
        if age_structure:
            # Если есть возрастная структура, используем её
            working_age_share = age_structure.get('working_age', 0.65)
            labor_force_participation = age_structure.get('participation_rate', 0.75)
            return population * working_age_share * labor_force_participation
        else:
            # Упрощенный расчет: 65% населения в трудоспособном возрасте, 75% участвуют в экономике
            return population * 0.65 * 0.75 