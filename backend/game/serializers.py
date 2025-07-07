from rest_framework import serializers
from .models import (
    GameSession, GameParameters, EconomicIndicators, GameEvent, GameHistory,
    BudgetData, DemographicData, ProductionData, SocialData
)


class GameSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSession
        fields = ['id', 'user', 'created_at', 'updated_at', 'is_active', 
                 'current_turn', 'current_year', 'current_quarter', 
                 'elections_passed', 'budget', 'accumulated_reserves']


class GameParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameParameters
        fields = ['id', 'game_session', 'interest_rate', 'tax_rate', 
                 'government_spending', 'customs_duty', 'education_priority',
                 'healthcare_priority', 'defense_priority', 'infrastructure_priority',
                 'social_priority']


class EconomicIndicatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EconomicIndicators
        fields = ['id', 'game_session', 'turn', 'gdp_growth', 'gdp_absolute',
                 'inflation', 'unemployment', 'investments', 'president_rating',
                 'public_mood', 'export_volume', 'import_volume', 'created_at',
                 'money_supply', 'gold_reserves', 'reserve_ratio', 'refinance_rate', 'printing_press_active']


class BudgetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetData
        fields = ['id', 'game_session', 'turn', 'tax_revenue', 'customs_revenue',
                 'total_revenue', 'education_spending', 'healthcare_spending',
                 'defense_spending', 'infrastructure_spending', 'social_spending',
                 'total_spending', 'budget_balance', 'accumulated_reserves', 'created_at',
                 'social_transfers']


class DemographicDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemographicData
        fields = ['id', 'game_session', 'turn', 'population', 'natural_growth',
                 'migration_growth', 'life_expectancy', 'gdp_per_capita', 'created_at',
                 'social_transfers_per_capita']


class ProductionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionData
        fields = ['id', 'game_session', 'turn', 'capital_stock', 'labor_force',
                 'technology_progress', 'capital_intensity', 'labor_productivity',
                 'savings_rate', 'depreciation_rate', 'capital_share', 'created_at']


class SocialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialData
        fields = ['id', 'game_session', 'turn', 'education_level', 'healthcare_quality',
                 'social_stability', 'income_inequality', 'created_at']


class GameEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameEvent
        fields = ['id', 'game_session', 'turn', 'event_type', 'title', 'description',
                 'gdp_impact', 'inflation_impact', 'unemployment_impact', 'rating_impact',
                 'budget_impact', 'population_impact', 'created_at']


class GameHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameHistory
        fields = ['id', 'game_session', 'turn', 'parameters_data', 'indicators_data',
                 'budget_data', 'demographic_data', 'production_data', 'social_data',
                 'events_data', 'created_at']


class GameStateSerializer(serializers.Serializer):
    """Сериализатор для полного состояния игры"""
    game_session = GameSessionSerializer()
    parameters = GameParametersSerializer()
    current_indicators = EconomicIndicatorsSerializer()
    current_budget = BudgetDataSerializer()
    current_demographics = DemographicDataSerializer()
    current_production = ProductionDataSerializer()
    current_social = SocialDataSerializer()
    recent_events = GameEventSerializer(many=True)
    
    def to_representation(self, instance):
        """Представление состояния игры"""
        data = super().to_representation(instance)
        
        # Добавляем дополнительные вычисляемые поля
        data['next_elections_in'] = 16 - (instance.current_turn % 16)
        data['is_election_year'] = (instance.current_turn % 16) == 0
        
        return data


class NextTurnRequestSerializer(serializers.Serializer):
    """Сериализатор для запроса следующего хода"""
    interest_rate = serializers.FloatField(min_value=0.0, max_value=20.0)
    tax_rate = serializers.FloatField(min_value=0.0, max_value=50.0)
    government_spending = serializers.FloatField(min_value=10.0, max_value=50.0)
    customs_duty = serializers.FloatField(min_value=0.0, max_value=30.0)
    education_priority = serializers.FloatField(min_value=0.0, max_value=40.0)
    healthcare_priority = serializers.FloatField(min_value=0.0, max_value=40.0)
    defense_priority = serializers.FloatField(min_value=0.0, max_value=40.0)
    infrastructure_priority = serializers.FloatField(min_value=0.0, max_value=40.0)
    social_priority = serializers.FloatField(min_value=0.0, max_value=40.0)
    
    def validate(self, data):
        """Валидация бюджетных приоритетов"""
        priorities = [
            data['education_priority'],
            data['healthcare_priority'],
            data['defense_priority'],
            data['infrastructure_priority'],
            data['social_priority']
        ]
        
        total_priority = sum(priorities)
        if total_priority > 100.0:
            raise serializers.ValidationError(
                f"Сумма бюджетных приоритетов не может превышать 100%. Текущая сумма: {total_priority}%"
            )
        
        return data


class GameStartSerializer(serializers.Serializer):
    """Сериализатор для начала новой игры"""
    initial_parameters = NextTurnRequestSerializer(required=False) 