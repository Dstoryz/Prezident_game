from django.db import models
import json


class GameSession(models.Model):
    """Игровая сессия"""
    user = models.ForeignKey('auth_app.User', on_delete=models.CASCADE, related_name='game_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    current_turn = models.IntegerField(default=1)
    current_year = models.IntegerField(default=2024)
    current_quarter = models.IntegerField(default=1)
    elections_passed = models.IntegerField(default=0)
    
    # Новые поля для бюджета и накоплений
    budget = models.FloatField(default=1000.0)  # Текущий бюджет (млн $)
    accumulated_reserves = models.FloatField(default=500.0)  # Накопления (млн $)
    
    def __str__(self):
        return f"Игра #{self.id} - Ход {self.current_turn}"


class GameParameters(models.Model):
    """Параметры управления игрока"""
    game_session = models.OneToOneField(GameSession, on_delete=models.CASCADE, related_name='parameters')
    
    # Управляемые параметры
    interest_rate = models.FloatField(default=5.0)  # Процентная ставка
    tax_rate = models.FloatField(default=20.0)      # Налоговая нагрузка
    government_spending = models.FloatField(default=25.0)  # Государственные расходы (% от ВВП)
    customs_duty = models.FloatField(default=5.0)   # Таможенные пошлины
    
    # Новые параметры - бюджетные приоритеты
    education_priority = models.FloatField(default=20.0)    # Образование и наука (% от бюджета)
    healthcare_priority = models.FloatField(default=20.0)   # Здравоохранение (% от бюджета)
    defense_priority = models.FloatField(default=20.0)      # Оборона (% от бюджета)
    infrastructure_priority = models.FloatField(default=20.0)  # Инфраструктура (% от бюджета)
    social_priority = models.FloatField(default=20.0)       # Социальная защита (% от бюджета)
    
    def __str__(self):
        return f"Параметры игры #{self.game_session.id}"


class EconomicIndicators(models.Model):
    """Экономические показатели"""
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='indicators')
    turn = models.IntegerField()
    
    # Рассчитываемые показатели
    gdp_growth = models.FloatField()        # Темп роста ВВП (%)
    gdp_absolute = models.FloatField(default=1000.0)  # Абсолютное значение ВВП (млн $)
    inflation = models.FloatField()         # Инфляция (%)
    unemployment = models.FloatField()      # Уровень безработицы (%)
    investments = models.FloatField()       # Объем инвестиций (% от ВВП)
    president_rating = models.FloatField()  # Рейтинг поддержки президента (%)
    
    # Дополнительные показатели
    public_mood = models.FloatField(default=50.0)  # Настроение населения
    export_volume = models.FloatField(default=30.0)  # Объем экспорта
    import_volume = models.FloatField(default=25.0)  # Объем импорта

    # Новые поля для банковской системы и денежной массы
    money_supply = models.FloatField(default=1000.0)  # Денежная масса (млн $)
    gold_reserves = models.FloatField(default=100.0)   # Золотой запас (млн $)
    reserve_ratio = models.FloatField(default=0.1)     # Резервные требования (доля)
    refinance_rate = models.FloatField(default=0.05)   # Ставка рефинансирования
    printing_press_active = models.BooleanField(default=False)  # Печатный станок

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['game_session', 'turn']
    
    def __str__(self):
        return f"Показатели игры #{self.game_session.id}, ход {self.turn}"


class BudgetData(models.Model):
    """Бюджетные данные"""
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='budget_data')
    turn = models.IntegerField()
    
    # Доходы бюджета
    tax_revenue = models.FloatField()        # Налоговые поступления (млн $)
    customs_revenue = models.FloatField()    # Таможенные поступления (млн $)
    total_revenue = models.FloatField()      # Общие доходы (млн $)
    
    # Расходы бюджета
    education_spending = models.FloatField()     # Расходы на образование (млн $)
    healthcare_spending = models.FloatField()    # Расходы на здравоохранение (млн $)
    defense_spending = models.FloatField()       # Расходы на оборону (млн $)
    infrastructure_spending = models.FloatField()  # Расходы на инфраструктуру (млн $)
    social_spending = models.FloatField()        # Расходы на социальную защиту (млн $)
    total_spending = models.FloatField()         # Общие расходы (млн $)
    
    # Новое поле: социальные трансферты
    social_transfers = models.FloatField(default=0.0)  # Социальные трансферты (млн $)

    # Бюджетный баланс
    budget_balance = models.FloatField()         # Дефицит/профицит (млн $)
    accumulated_reserves = models.FloatField()   # Накопления на конец периода (млн $)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['game_session', 'turn']
    
    def __str__(self):
        return f"Бюджет игры #{self.game_session.id}, ход {self.turn}"


class DemographicData(models.Model):
    """Демографические данные"""
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='demographic_data')
    turn = models.IntegerField()
    
    population = models.FloatField()           # Численность населения (млн человек)
    natural_growth = models.FloatField()       # Естественный прирост (%)
    migration_growth = models.FloatField()     # Миграционный прирост (%)
    life_expectancy = models.FloatField()      # Средняя продолжительность жизни (лет)
    gdp_per_capita = models.FloatField()       # ВВП на душу населения ($)

    # Новое поле: соц. трансферты на душу населения
    social_transfers_per_capita = models.FloatField(default=0.0)  # Соц. трансферты на человека ($)

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['game_session', 'turn']
    
    def __str__(self):
        return f"Демография игры #{self.game_session.id}, ход {self.turn}"


class ProductionData(models.Model):
    """Производственные данные (модель Солоу)"""
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='production_data')
    turn = models.IntegerField()
    
    # Модель Солоу
    capital_stock = models.FloatField()        # Капитал (млн $)
    labor_force = models.FloatField()          # Рабочая сила (млн человек)
    technology_progress = models.FloatField()  # Технологический прогресс (фактор A)
    capital_intensity = models.FloatField()    # Капиталовооруженность ($/чел)
    labor_productivity = models.FloatField()   # Производительность труда ($/чел)
    
    # Параметры модели
    savings_rate = models.FloatField()         # Норма сбережений (%)
    depreciation_rate = models.FloatField()    # Норма амортизации (%)
    capital_share = models.FloatField()        # Доля капитала в производстве (%)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['game_session', 'turn']
    
    def __str__(self):
        return f"Производство игры #{self.game_session.id}, ход {self.turn}"


class SocialData(models.Model):
    """Социальные показатели"""
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='social_data')
    turn = models.IntegerField()
    
    education_level = models.FloatField()      # Уровень образования (среднее количество лет обучения)
    healthcare_quality = models.FloatField()   # Качество здравоохранения (индекс 0-100)
    social_stability = models.FloatField()     # Социальная стабильность (индекс 0-100)
    income_inequality = models.FloatField()    # Неравенство доходов (коэффициент Джини)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['game_session', 'turn']
    
    def __str__(self):
        return f"Социальные показатели игры #{self.game_session.id}, ход {self.turn}"


class GameEvent(models.Model):
    """Игровые события"""
    EVENT_TYPES = [
        ('natural_disaster', 'Природная катастрофа'),
        ('economic_crisis', 'Экономический кризис'),
        ('sanctions', 'Санкции/торговые ограничения'),
        ('international_conflict', 'Международный конфликт'),
        ('commodity_price_change', 'Изменение цен на сырье'),
        ('social_protest', 'Социальные протесты'),
        ('technology_breakthrough', 'Технологический прорыв'),
        ('demographic_change', 'Демографические изменения'),
    ]
    
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='events')
    turn = models.IntegerField()
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Влияние события на показатели
    gdp_impact = models.FloatField(default=0.0)
    inflation_impact = models.FloatField(default=0.0)
    unemployment_impact = models.FloatField(default=0.0)
    rating_impact = models.FloatField(default=0.0)
    budget_impact = models.FloatField(default=0.0)
    population_impact = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} (ход {self.turn})"


class GameHistory(models.Model):
    """История игры для анализа"""
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='history')
    turn = models.IntegerField()
    
    # Состояние на момент хода
    parameters_data = models.JSONField()  # Параметры управления
    indicators_data = models.JSONField()  # Экономические показатели
    budget_data = models.JSONField(default=dict)      # Бюджетные данные
    demographic_data = models.JSONField(default=dict) # Демографические данные
    production_data = models.JSONField(default=dict)  # Производственные данные
    social_data = models.JSONField(default=dict)      # Социальные данные
    events_data = models.JSONField()      # События хода
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['game_session', 'turn']
    
    def __str__(self):
        return f"История игры #{self.game_session.id}, ход {self.turn}"
