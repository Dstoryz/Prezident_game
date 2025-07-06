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
    
    def __str__(self):
        return f"Параметры игры #{self.game_session.id}"


class EconomicIndicators(models.Model):
    """Экономические показатели"""
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='indicators')
    turn = models.IntegerField()
    
    # Рассчитываемые показатели
    gdp_growth = models.FloatField()        # Темп роста ВВП (%)
    inflation = models.FloatField()         # Инфляция (%)
    unemployment = models.FloatField()      # Уровень безработицы (%)
    investments = models.FloatField()       # Объем инвестиций (% от ВВП)
    president_rating = models.FloatField()  # Рейтинг поддержки президента (%)
    
    # Дополнительные показатели
    public_mood = models.FloatField(default=50.0)  # Настроение населения
    export_volume = models.FloatField(default=30.0)  # Объем экспорта
    import_volume = models.FloatField(default=25.0)  # Объем импорта
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['game_session', 'turn']
    
    def __str__(self):
        return f"Показатели игры #{self.game_session.id}, ход {self.turn}"


class GameEvent(models.Model):
    """Игровые события"""
    EVENT_TYPES = [
        ('natural_disaster', 'Природная катастрофа'),
        ('economic_crisis', 'Экономический кризис'),
        ('sanctions', 'Санкции/торговые ограничения'),
        ('international_conflict', 'Международный конфликт'),
        ('commodity_price_change', 'Изменение цен на сырье'),
        ('social_protest', 'Социальные протесты'),
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
    events_data = models.JSONField()      # События хода
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['game_session', 'turn']
    
    def __str__(self):
        return f"История игры #{self.game_session.id}, ход {self.turn}"
