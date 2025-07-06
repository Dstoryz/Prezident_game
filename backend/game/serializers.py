from rest_framework import serializers
from .models import GameSession, GameParameters, EconomicIndicators, GameEvent, GameHistory


class GameParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameParameters
        fields = ['interest_rate', 'tax_rate', 'government_spending', 'customs_duty']


class EconomicIndicatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EconomicIndicators
        fields = [
            'gdp_growth', 'inflation', 'unemployment', 'investments', 
            'president_rating', 'public_mood', 'export_volume', 'import_volume'
        ]


class GameEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameEvent
        fields = [
            'event_type', 'title', 'description', 'gdp_impact', 
            'inflation_impact', 'unemployment_impact', 'rating_impact'
        ]


class GameSessionSerializer(serializers.ModelSerializer):
    parameters = GameParametersSerializer(read_only=True)
    current_indicators = serializers.SerializerMethodField()
    current_events = serializers.SerializerMethodField()
    
    class Meta:
        model = GameSession
        fields = [
            'id', 'current_turn', 'current_year', 'current_quarter', 
            'elections_passed', 'is_active', 'parameters', 
            'current_indicators', 'current_events'
        ]
    
    def get_current_indicators(self, obj):
        """Получить текущие показатели"""
        try:
            indicators = obj.indicators.filter(turn=obj.current_turn).first()
            return EconomicIndicatorsSerializer(indicators).data if indicators else None
        except:
            return None
    
    def get_current_events(self, obj):
        """Получить события текущего хода"""
        try:
            events = obj.events.filter(turn=obj.current_turn)
            return GameEventSerializer(events, many=True).data
        except:
            return []


class GameHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameHistory
        fields = ['turn', 'parameters_data', 'indicators_data', 'events_data']


class NextTurnRequestSerializer(serializers.Serializer):
    """Сериализатор для запроса следующего хода"""
    interest_rate = serializers.FloatField(min_value=0, max_value=50, required=False)
    tax_rate = serializers.FloatField(min_value=0, max_value=100, required=False)
    government_spending = serializers.FloatField(min_value=0, max_value=100, required=False)
    customs_duty = serializers.FloatField(min_value=0, max_value=100, required=False) 