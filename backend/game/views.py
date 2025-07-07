from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import logging

from .models import (
    GameSession, GameParameters, EconomicIndicators, GameEvent, GameHistory,
    BudgetData, DemographicData, ProductionData, SocialData
)
from .serializers import (
    GameSessionSerializer, GameParametersSerializer, EconomicIndicatorsSerializer,
    GameEventSerializer, GameHistorySerializer, NextTurnRequestSerializer,
    BudgetDataSerializer, DemographicDataSerializer, ProductionDataSerializer,
    SocialDataSerializer, GameStateSerializer
)
from .services.economic_logic import EconomicEngine
from .services.event_generator import EventGenerator


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_game(request):
    """Начать новую игру"""
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"[start_game] Входные данные: {request.data}")
    try:
        with transaction.atomic():
            # Создаем новую игровую сессию
            game_session = GameSession.objects.create(
                user=request.user,
                current_turn=1,
                current_year=2024,
                current_quarter=1,
                elections_passed=0,
                budget=1000.0,
                accumulated_reserves=500.0
            )
            
            # Получаем начальные параметры из запроса или используем значения по умолчанию
            initial_params = request.data.get('initial_parameters', {})
            logger.warning(f"[start_game] initial_parameters: {initial_params}")
            
            # Создаем параметры игры
            parameters = GameParameters.objects.create(
                game_session=game_session,
                interest_rate=initial_params.get('interest_rate', 5.0),
                tax_rate=initial_params.get('tax_rate', 20.0),
                government_spending=initial_params.get('government_spending', 25.0),
                customs_duty=initial_params.get('customs_duty', 5.0),
                education_priority=initial_params.get('education_priority', 20.0),
                healthcare_priority=initial_params.get('healthcare_priority', 20.0),
                defense_priority=initial_params.get('defense_priority', 20.0),
                infrastructure_priority=initial_params.get('infrastructure_priority', 20.0),
                social_priority=initial_params.get('social_priority', 20.0)
            )
            
            # Рассчитываем начальные показатели
            economic_engine = EconomicEngine()
            indicators_data = economic_engine.calculate_indicators({
                'interest_rate': parameters.interest_rate,
                'tax_rate': parameters.tax_rate,
                'government_spending': parameters.government_spending,
                'customs_duty': parameters.customs_duty,
                'education_priority': parameters.education_priority,
                'healthcare_priority': parameters.healthcare_priority,
                'defense_priority': parameters.defense_priority,
                'infrastructure_priority': parameters.infrastructure_priority,
                'social_priority': parameters.social_priority
            })
            
            # Создаем экономические показатели
            indicators = EconomicIndicators.objects.create(
                game_session=game_session,
                turn=1,
                gdp_growth=indicators_data['gdp_growth'],
                gdp_absolute=indicators_data['gdp_absolute'],
                inflation=indicators_data['inflation'],
                unemployment=indicators_data['unemployment'],
                investments=indicators_data['investments'],
                president_rating=indicators_data['president_rating'],
                public_mood=indicators_data['public_mood'],
                export_volume=indicators_data['export_volume'],
                import_volume=indicators_data['import_volume']
            )
            
            # Создаем бюджетные данные
            budget_fields = {f.name for f in BudgetData._meta.get_fields()}
            clean_budget_data = {k: v for k, v in indicators_data['budget_data'].items() if k in budget_fields}
            budget_data = BudgetData.objects.create(
                game_session=game_session,
                turn=1,
                **clean_budget_data
            )
            
            # Создаем демографические данные
            demographic_data = DemographicData.objects.create(
                game_session=game_session,
                turn=1,
                **indicators_data['demographic_data']
            )
            
            # Создаем производственные данные
            production_data = ProductionData.objects.create(
                game_session=game_session,
                turn=1,
                **indicators_data['production_data']
            )
            
            # Создаем социальные данные
            social_data = SocialData.objects.create(
                game_session=game_session,
                turn=1,
                **indicators_data['social_data']
            )
            
            # Создаем запись в истории
            GameHistory.objects.create(
                game_session=game_session,
                turn=1,
                parameters_data=GameParametersSerializer(parameters).data,
                indicators_data=EconomicIndicatorsSerializer(indicators).data,
                budget_data=BudgetDataSerializer(budget_data).data,
                demographic_data=DemographicDataSerializer(demographic_data).data,
                production_data=ProductionDataSerializer(production_data).data,
                social_data=SocialDataSerializer(social_data).data,
                events_data=[]
            )
            # Формируем полное состояние игры для фронта
            game_state = {
                'id': game_session.id,
                'current_turn': game_session.current_turn,
                'current_year': game_session.current_year,
                'current_quarter': game_session.current_quarter,
                'elections_passed': game_session.elections_passed,
                'is_active': game_session.is_active,
                'parameters': GameParametersSerializer(parameters).data,
                'current_indicators': EconomicIndicatorsSerializer(indicators).data,
                'current_budget': BudgetDataSerializer(budget_data).data,
                'current_demographics': DemographicDataSerializer(demographic_data).data,
                'current_production': ProductionDataSerializer(production_data).data,
                'current_social': SocialDataSerializer(social_data).data,
                'recent_events': [],
            }
            return Response({
                'success': True,
                'message': 'Игра успешно начата',
                'game': game_state
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        logger.error(f"[start_game] Ошибка: {str(e)}", exc_info=True)
        return Response({
            'error': f'Ошибка при создании игры: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def next_turn(request, game_id):
    """Обработать следующий ход"""
    try:
        game_session = get_object_or_404(GameSession, id=game_id, user=request.user)
        
        # Валидируем параметры
        serializer = NextTurnRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        parameters_data = serializer.validated_data
        
        with transaction.atomic():
            # Обновляем параметры
            parameters = game_session.parameters
            for field, value in parameters_data.items():
                setattr(parameters, field, value)
            parameters.save()
            
            # Получаем предыдущие данные
            previous_indicators = game_session.indicators.filter(turn=game_session.current_turn).first()
            previous_budget = game_session.budget_data.filter(turn=game_session.current_turn).first()
            previous_demographics = game_session.demographic_data.filter(turn=game_session.current_turn).first()
            previous_production = game_session.production_data.filter(turn=game_session.current_turn).first()
            
            # Рассчитываем новые показатели
            economic_engine = EconomicEngine()
            indicators_data = economic_engine.calculate_indicators(
                parameters_data,
                EconomicIndicatorsSerializer(previous_indicators).data if previous_indicators else None,
                BudgetDataSerializer(previous_budget).data if previous_budget else None,
                DemographicDataSerializer(previous_demographics).data if previous_demographics else None,
                ProductionDataSerializer(previous_production).data if previous_production else None
            )
            
            # Генерируем события
            event_generator = EventGenerator()
            events = event_generator.generate_events(game_session.current_turn)
            
            # Применяем влияние событий
            if events:
                indicators_data = economic_engine.apply_event_impacts(indicators_data, events)
            
            # Обновляем игровую сессию
            game_session.current_turn += 1
            game_session.current_quarter = ((game_session.current_turn - 1) % 4) + 1
            game_session.current_year = 2024 + (game_session.current_turn - 1) // 4
            
            # Проверяем выборы
            if game_session.current_turn % 16 == 0:
                game_session.elections_passed += 1
                if indicators_data['president_rating'] < 50:
                    game_session.is_active = False
            
            # Обновляем бюджет и накопления
            game_session.budget = indicators_data['budget_data']['total_revenue']
            game_session.accumulated_reserves += indicators_data['budget_data']['budget_balance']
            
            game_session.save()
            
            # Создаем новые записи данных
            new_turn = game_session.current_turn
            
            indicators = EconomicIndicators.objects.create(
                game_session=game_session,
                turn=new_turn,
                gdp_growth=indicators_data['gdp_growth'],
                gdp_absolute=indicators_data['gdp_absolute'],
                inflation=indicators_data['inflation'],
                unemployment=indicators_data['unemployment'],
                investments=indicators_data['investments'],
                president_rating=indicators_data['president_rating'],
                public_mood=indicators_data['public_mood'],
                export_volume=indicators_data['export_volume'],
                import_volume=indicators_data['import_volume']
            )
            
            # --- Фильтрация полей для BudgetData ---
            budget_fields = {f.name for f in BudgetData._meta.get_fields()}
            clean_budget_data = {k: v for k, v in indicators_data['budget_data'].items() if k in budget_fields}
            budget_data = BudgetData.objects.create(
                game_session=game_session,
                turn=new_turn,
                **clean_budget_data
            )
            # --- Фильтрация полей для DemographicData ---
            demographic_fields = {f.name for f in DemographicData._meta.get_fields()}
            clean_demographic_data = {k: v for k, v in indicators_data['demographic_data'].items() if k in demographic_fields}
            demographic_data = DemographicData.objects.create(
                game_session=game_session,
                turn=new_turn,
                **clean_demographic_data
            )
            # --- Фильтрация полей для ProductionData ---
            production_fields = {f.name for f in ProductionData._meta.get_fields()}
            clean_production_data = {k: v for k, v in indicators_data['production_data'].items() if k in production_fields}
            production_data = ProductionData.objects.create(
                game_session=game_session,
                turn=new_turn,
                **clean_production_data
            )
            # --- Фильтрация полей для SocialData ---
            social_fields = {f.name for f in SocialData._meta.get_fields()}
            clean_social_data = {k: v for k, v in indicators_data['social_data'].items() if k in social_fields}
            social_data = SocialData.objects.create(
                game_session=game_session,
                turn=new_turn,
                **clean_social_data
            )
            
            # Создаем события
            created_events = []
            for event_data in events:
                event = GameEvent.objects.create(
                    game_session=game_session,
                    turn=new_turn,
                    **event_data
                )
                created_events.append(GameEventSerializer(event).data)
            
            # Создаем запись в истории
            GameHistory.objects.create(
                game_session=game_session,
                turn=new_turn,
                parameters_data=GameParametersSerializer(parameters).data,
                indicators_data=EconomicIndicatorsSerializer(indicators).data,
                budget_data=BudgetDataSerializer(budget_data).data,
                demographic_data=DemographicDataSerializer(demographic_data).data,
                production_data=ProductionDataSerializer(production_data).data,
                social_data=SocialDataSerializer(social_data).data,
                events_data=created_events
            )
            
            # Получаем текущий бюджет
            current_budget = BudgetDataSerializer(budget_data).data if budget_data else None
            # Формируем полное состояние игры для фронта
            game_state = {
                'id': game_session.id,
                'current_turn': game_session.current_turn,
                'current_year': game_session.current_year,
                'current_quarter': game_session.current_quarter,
                'elections_passed': game_session.elections_passed,
                'is_active': game_session.is_active,
                'parameters': GameParametersSerializer(parameters).data,
                'current_indicators': EconomicIndicatorsSerializer(indicators).data,
                'current_events': created_events,
                'current_budget': current_budget,
            }
            return Response({
                'success': True,
                'message': 'Ход успешно выполнен',
                'game': game_state,
                'game_over': not game_session.is_active,
                'game_over_reason': 'Рейтинг президента ниже 50 после выборов' if not game_session.is_active else '',
                'events': created_events,
                'indicators': EconomicIndicatorsSerializer(indicators).data,
                'current_budget': current_budget,
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        return Response({
            'error': f'Ошибка при обработке хода: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def game_state(request, game_id):
    """Получить текущее состояние игры"""
    try:
        game_session = get_object_or_404(GameSession, id=game_id, user=request.user)
        
        # Получаем текущие данные
        current_indicators = game_session.indicators.filter(turn=game_session.current_turn).first()
        current_budget = game_session.budget_data.filter(turn=game_session.current_turn).first()
        current_demographics = game_session.demographic_data.filter(turn=game_session.current_turn).first()
        current_production = game_session.production_data.filter(turn=game_session.current_turn).first()
        current_social = game_session.social_data.filter(turn=game_session.current_turn).first()
        recent_events = game_session.events.filter(turn=game_session.current_turn)
        
        return Response({
            'game_session': GameSessionSerializer(game_session).data,
            'parameters': GameParametersSerializer(game_session.parameters).data,
            'current_indicators': EconomicIndicatorsSerializer(current_indicators).data if current_indicators else None,
            'current_budget': BudgetDataSerializer(current_budget).data if current_budget else None,
            'current_demographics': DemographicDataSerializer(current_demographics).data if current_demographics else None,
            'current_production': ProductionDataSerializer(current_production).data if current_production else None,
            'current_social': SocialDataSerializer(current_social).data if current_social else None,
            'recent_events': GameEventSerializer(recent_events, many=True).data,
            'next_elections_in': 16 - (game_session.current_turn % 16),
            'is_election_year': (game_session.current_turn % 16) == 0
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Ошибка при получении состояния игры: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def game_history(request, game_id):
    """Получить историю игры"""
    try:
        game_session = get_object_or_404(GameSession, id=game_id, user=request.user)
        
        # Получаем историю последних 20 ходов
        history = game_session.history.order_by('-turn')[:20]
        
        return Response({
            'game_id': game_id,
            'history': GameHistorySerializer(history, many=True).data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Ошибка при получении истории: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def budget_data(request, game_id):
    """Получить бюджетные данные"""
    try:
        game_session = get_object_or_404(GameSession, id=game_id, user=request.user)
        
        budget_history = game_session.budget_data.order_by('turn')
        
        return Response({
            'game_id': game_id,
            'budget_history': BudgetDataSerializer(budget_history, many=True).data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Ошибка при получении бюджетных данных: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def demographic_data(request, game_id):
    """Получить демографические данные"""
    try:
        game_session = get_object_or_404(GameSession, id=game_id, user=request.user)
        
        demographic_history = game_session.demographic_data.order_by('turn')
        
        return Response({
            'game_id': game_id,
            'demographic_history': DemographicDataSerializer(demographic_history, many=True).data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Ошибка при получении демографических данных: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def production_data(request, game_id):
    """Получить производственные данные (модель Солоу)"""
    try:
        game_session = get_object_or_404(GameSession, id=game_id, user=request.user)
        
        production_history = game_session.production_data.order_by('turn')
        
        return Response({
            'game_id': game_id,
            'production_history': ProductionDataSerializer(production_history, many=True).data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Ошибка при получении производственных данных: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)
