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
from rest_framework import viewsets
from rest_framework.decorators import action

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
from .services.event_generator import EventGenerator
from .services.enhanced_economic_model import EnhancedEconomicModel, EconomicParameters


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
            
            # Рассчитываем начальные показатели с расширенной моделью
            enhanced_model = EnhancedEconomicModel()
            economic_params = EconomicParameters(
                interest_rate=parameters.interest_rate,
                tax_rate=parameters.tax_rate,
                government_spending=parameters.government_spending,
                customs_duty=parameters.customs_duty,
                education_priority=parameters.education_priority,
                healthcare_priority=parameters.healthcare_priority,
                defense_priority=parameters.defense_priority,
                infrastructure_priority=parameters.infrastructure_priority,
                social_priority=parameters.social_priority
            )
            indicators_data = enhanced_model.calculate_indicators(economic_params)
            
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
            if 'budget_data' in indicators_data:
                clean_budget_data = {k: v for k, v in indicators_data['budget_data'].items() if k in budget_fields}
            else:
                # Если budget_data нет, создаем данные по умолчанию
                clean_budget_data = {
                    'tax_revenue': 0.0,
                    'customs_revenue': 0.0,
                    'total_revenue': 0.0,
                    'education_spending': 0.0,
                    'healthcare_spending': 0.0,
                    'defense_spending': 0.0,
                    'infrastructure_spending': 0.0,
                    'social_spending': 0.0,
                    'total_spending': 0.0,
                    'budget_balance': 0.0,
                    'accumulated_reserves': 500.0,
                    'social_transfers': 0.0,
                    'gold_reserves': 100.0,
                    'external_debt': 0.0
                }
            budget_data = BudgetData.objects.create(
                game_session=game_session,
                turn=1,
                **clean_budget_data
            )
            
            # Создаем демографические данные
            if 'demographic_data' in indicators_data:
                demographic_data = DemographicData.objects.create(
                    game_session=game_session,
                    turn=1,
                    **indicators_data['demographic_data']
                )
            else:
                # Если demographic_data нет, создаем данные по умолчанию
                demographic_data = DemographicData.objects.create(
                    game_session=game_session,
                    turn=1,
                    population=150.0,
                    natural_growth=0.5,
                    migration_growth=0.0,
                    life_expectancy=75.0,
                    gdp_per_capita=10000.0,
                    social_transfers_per_capita=0.0
                )
            
            # Создаем производственные данные
            if 'production_data' in indicators_data:
                production_data = ProductionData.objects.create(
                    game_session=game_session,
                    turn=1,
                    **indicators_data['production_data']
                )
            else:
                # Если production_data нет, создаем данные по умолчанию
                production_data = ProductionData.objects.create(
                    game_session=game_session,
                    turn=1,
                    capital_stock=1000.0,
                    labor_force=75.0,
                    technology_progress=1.0,
                    capital_intensity=13.33,
                    labor_productivity=13.33,
                    savings_rate=20.0,
                    depreciation_rate=5.0,
                    capital_share=30.0
                )
            
            # Создаем социальные данные
            if 'social_data' in indicators_data:
                social_data = SocialData.objects.create(
                    game_session=game_session,
                    turn=1,
                    **indicators_data['social_data']
                )
            else:
                # Если social_data нет, создаем данные по умолчанию
                social_data = SocialData.objects.create(
                    game_session=game_session,
                    turn=1,
                    education_level=12.0,
                    healthcare_quality=70.0,
                    social_stability=75.0,
                    income_inequality=0.35
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
        print(f"[next_turn] Получен запрос для игры {game_id}")
        print(f"[next_turn] Данные запроса: {request.data}")
        
        game_session = get_object_or_404(GameSession, id=game_id, user=request.user)
        
        # Валидируем параметры
        serializer = NextTurnRequestSerializer(data=request.data)
        if not serializer.is_valid():
            print(f"[next_turn] Ошибки валидации: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        parameters_data = serializer.validated_data
        print(f"[next_turn] Валидированные данные: {parameters_data}")
        
        with transaction.atomic():
            # Обновляем параметры
            parameters = game_session.parameters
            for field, value in parameters_data.items():
                if hasattr(parameters, field):
                    setattr(parameters, field, value)
            parameters.save()
            
            # Получаем предыдущие данные
            previous_indicators = game_session.indicators.filter(turn=game_session.current_turn).first()
            previous_budget = game_session.budget_data.filter(turn=game_session.current_turn).first()
            previous_demographics = game_session.demographic_data.filter(turn=game_session.current_turn).first()
            previous_production = game_session.production_data.filter(turn=game_session.current_turn).first()
            
            # Рассчитываем новые показатели с расширенной моделью
            enhanced_model = EnhancedEconomicModel()
            economic_params = EconomicParameters(**parameters_data)
            indicators_data = enhanced_model.calculate_indicators(
                economic_params,
                EconomicIndicatorsSerializer(previous_indicators).data if previous_indicators else None
            )
            
            # Генерируем события
            event_generator = EventGenerator()
            events = event_generator.generate_events(game_session.current_turn)
            
            # Примечание: EnhancedEconomicModel уже включает обработку событий в calculate_indicators
            
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
        print(f"[next_turn] Исключение: {str(e)}")
        import traceback
        print(f"[next_turn] Traceback: {traceback.format_exc()}")
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


class EnhancedGameViewSet(viewsets.ViewSet):
    """API для расширенной экономической модели"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enhanced_model = EnhancedEconomicModel()
    
    @action(detail=False, methods=['post'])
    def start_enhanced_game(self, request):
        """Начать новую игру с расширенной моделью"""
        try:
            # Создаем новую игровую сессию
            game_session = GameSession.objects.create(
                user=request.user,
                current_turn=1,
                is_active=True
            )
            
            # Инициализируем экономические показатели
            initial_indicators = self.enhanced_model.calculate_indicators(
                EconomicParameters()
            )
            
            # Сохраняем начальные показатели
            economic_indicators = EconomicIndicators.objects.create(
                game_session=game_session,
                turn=1,
                gdp_growth=initial_indicators['gdp_growth'],
                gdp_absolute=initial_indicators['total_gdp'],
                inflation=initial_indicators['inflation'],
                unemployment=initial_indicators['unemployment'],
                investments=20.0,  # Базовые инвестиции
                president_rating=initial_indicators['president_rating'],
                public_mood=initial_indicators['public_mood'],
                export_volume=initial_indicators['exports'],
                import_volume=initial_indicators['imports'],
                # Новые поля для расширенной модели
                industry_output=initial_indicators['industry_output'],
                services_output=initial_indicators['services_output'],
                exchange_rate=initial_indicators['exchange_rate'],
                money_supply=initial_indicators['money_supply'],
                gold_reserves=initial_indicators['gold_reserves'],
                external_debt=initial_indicators['external_debt'],
                population=initial_indicators['population'],
                interest_rate=initial_indicators['interest_rate']
            )
            
            # Сохраняем бюджетные данные
            budget_data = BudgetData.objects.create(
                game_session=game_session,
                turn=1,
                tax_revenue=initial_indicators['tax_revenue'],
                customs_revenue=initial_indicators.get('customs_revenue', 0),
                total_revenue=initial_indicators['total_revenue'],
                education_spending=initial_indicators['education_spending'],
                healthcare_spending=initial_indicators['healthcare_spending'],
                defense_spending=initial_indicators['defense_spending'],
                infrastructure_spending=initial_indicators['infrastructure_spending'],
                social_spending=initial_indicators['social_spending'],
                total_spending=initial_indicators['total_spending'],
                budget_balance=initial_indicators['budget_balance'],
                social_transfers=initial_indicators['social_transfers'],
                accumulated_reserves=500.0,
                gold_reserves=initial_indicators['gold_reserves'],
                external_debt=initial_indicators['external_debt']
            )
            
            return Response({
                'success': True,
                'message': 'Игра с расширенной моделью начата',
                'game': {
                    'id': game_session.id,
                    'turn': game_session.current_turn,
                    'indicators': EconomicIndicatorsSerializer(economic_indicators).data,
                    'budget': BudgetDataSerializer(budget_data).data,
                    'model_type': 'enhanced'
                }
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Ошибка при запуске игры: {str(e)}'
            }, status=400)
    
    @action(detail=True, methods=['post'])
    def next_enhanced_turn(self, request, pk=None):
        """Следующий ход с расширенной моделью"""
        try:
            game_session = GameSession.objects.get(id=pk, user=request.user)
            
            # Получаем параметры управления
            parameters_data = request.data.get('parameters', {})
            parameters = EconomicParameters(
                interest_rate=parameters_data.get('interest_rate', 5.0),
                tax_rate=parameters_data.get('tax_rate', 20.0),
                government_spending=parameters_data.get('government_spending', 25.0),
                customs_duty=parameters_data.get('customs_duty', 5.0),
                education_priority=parameters_data.get('education_priority', 20.0),
                healthcare_priority=parameters_data.get('healthcare_priority', 20.0),
                defense_priority=parameters_data.get('defense_priority', 20.0),
                infrastructure_priority=parameters_data.get('infrastructure_priority', 20.0),
                social_priority=parameters_data.get('social_priority', 20.0),
                social_transfers=parameters_data.get('social_transfers', 0.0),
                reserve_ratio=parameters_data.get('reserve_ratio', 0.1),
                refinance_rate=parameters_data.get('refinance_rate', 0.05),
                printing_press_active=parameters_data.get('printing_press_active', False)
            )
            
            # Получаем предыдущие показатели
            previous_indicators = EconomicIndicators.objects.filter(
                game_session=game_session
            ).order_by('-turn').first()
            
            previous_data = None
            if previous_indicators:
                previous_data = {
                    'total_gdp': previous_indicators.gdp_absolute,
                    'inflation': previous_indicators.inflation,
                    'unemployment': previous_indicators.unemployment,
                    'exchange_rate': previous_indicators.exchange_rate,
                    'money_supply': previous_indicators.money_supply,
                    'gold_reserves': previous_indicators.gold_reserves,
                    'external_debt': previous_indicators.external_debt,
                    'population': previous_indicators.population,
                    'public_mood': previous_indicators.public_mood,
                    'industry_capital': previous_indicators.industry_output * 0.3,  # Упрощенная оценка
                    'services_capital': previous_indicators.services_output * 0.4,
                    'industry_labor': 0.4,
                    'services_labor': 0.6,
                    'industry_technology': 1.0,
                    'services_technology': 1.0
                }
            
            # Рассчитываем новые показатели
            new_indicators = self.enhanced_model.calculate_indicators(parameters, previous_data)
            
            # Обновляем игровую сессию
            game_session.current_turn += 1
            game_session.save()
            
            # Сохраняем новые экономические показатели
            economic_indicators = EconomicIndicators.objects.create(
                game_session=game_session,
                turn=game_session.current_turn,
                gdp_growth=new_indicators['gdp_growth'],
                gdp_absolute=new_indicators['total_gdp'],
                inflation=new_indicators['inflation'],
                unemployment=new_indicators['unemployment'],
                investments=20.0,  # Базовые инвестиции
                president_rating=new_indicators['president_rating'],
                public_mood=new_indicators['public_mood'],
                export_volume=new_indicators['exports'],
                import_volume=new_indicators['imports'],
                # Новые поля
                industry_output=new_indicators['industry_output'],
                services_output=new_indicators['services_output'],
                exchange_rate=new_indicators['exchange_rate'],
                money_supply=new_indicators['money_supply'],
                gold_reserves=new_indicators['gold_reserves'],
                external_debt=new_indicators['external_debt'],
                population=new_indicators['population'],
                interest_rate=new_indicators['interest_rate']
            )
            
            # Сохраняем бюджетные данные
            budget_data = BudgetData.objects.create(
                game_session=game_session,
                turn=game_session.current_turn,
                tax_revenue=new_indicators['tax_revenue'],
                customs_revenue=new_indicators.get('customs_revenue', 0),
                total_revenue=new_indicators['total_revenue'],
                education_spending=new_indicators['education_spending'],
                healthcare_spending=new_indicators['healthcare_spending'],
                defense_spending=new_indicators['defense_spending'],
                infrastructure_spending=new_indicators['infrastructure_spending'],
                social_spending=new_indicators['social_spending'],
                total_spending=new_indicators['total_spending'],
                budget_balance=new_indicators['budget_balance'],
                social_transfers=new_indicators['social_transfers'],
                accumulated_reserves=500.0,  # Упрощенная логика
                gold_reserves=new_indicators['gold_reserves'],
                external_debt=new_indicators['external_debt']
            )
            
            # Проверяем, произошел ли кризис
            crisis_info = None
            if new_indicators.get('crisis'):
                crisis_info = {
                    'type': new_indicators['crisis']['name'],
                    'description': self.get_crisis_description(new_indicators['crisis']['name']),
                    'effects': new_indicators['crisis']
                }
            
            return Response({
                'success': True,
                'message': 'Ход выполнен успешно',
                'game': {
                    'id': game_session.id,
                    'turn': game_session.current_turn,
                    'indicators': EconomicIndicatorsSerializer(economic_indicators).data,
                    'budget': BudgetDataSerializer(budget_data).data,
                    'crisis': crisis_info,
                    'model_type': 'enhanced'
                }
            })
            
        except GameSession.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Игровая сессия не найдена'
            }, status=404)
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Ошибка при выполнении хода: {str(e)}'
            }, status=400)
    
    @action(detail=True, methods=['get'])
    def enhanced_state(self, request, pk=None):
        """Получить состояние игры с расширенной моделью"""
        try:
            game_session = GameSession.objects.get(id=pk, user=request.user)
            
            # Получаем последние показатели
            indicators = EconomicIndicators.objects.filter(
                game_session=game_session
            ).order_by('-turn').first()
            
            budget = BudgetData.objects.filter(
                game_session=game_session
            ).order_by('-turn').first()
            
            if not indicators or not budget:
                return Response({
                    'success': False,
                    'message': 'Данные игры не найдены'
                }, status=404)
            
            return Response({
                'success': True,
                'game': {
                    'id': game_session.id,
                    'turn': game_session.current_turn,
                    'indicators': EconomicIndicatorsSerializer(indicators).data,
                    'budget': BudgetDataSerializer(budget).data,
                    'model_type': 'enhanced'
                }
            })
            
        except GameSession.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Игровая сессия не найдена'
            }, status=404)
    
    def get_crisis_description(self, crisis_type: str) -> str:
        """Получить описание кризиса"""
        descriptions = {
            'supply_shock': 'Шок предложения: рост цен, снижение производства',
            'financial_crisis': 'Финансовый кризис: рост безработицы, увеличение долга',
            'sanctions': 'Санкции: снижение экспорта, девальвация валюты',
            'natural_disaster': 'Природная катастрофа: ущерб экономике и населению',
            'social_protests': 'Социальные протесты: падение настроения населения'
        }
        return descriptions.get(crisis_type, 'Неизвестный кризис')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_enhanced_game(request):
    """Начать новую расширенную игру"""
    try:
        with transaction.atomic():
            # Создаем новую игровую сессию с расширенной моделью
            game_session = GameSession.objects.create(
                user=request.user,
                current_turn=1,
                model_type='enhanced',
                is_active=True
            )
            
            # Создаем расширенную экономическую модель
            enhanced_model = EnhancedEconomicModel()
            
            # Получаем начальные параметры
            initial_params = request.data.get('parameters', {})
            economic_params = EconomicParameters(
                interest_rate=initial_params.get('interest_rate', 5.0),
                tax_rate=initial_params.get('tax_rate', 20.0),
                government_spending=initial_params.get('government_spending', 25.0),
                customs_duty=initial_params.get('customs_duty', 5.0),
                education_priority=initial_params.get('education_priority', 20.0),
                healthcare_priority=initial_params.get('healthcare_priority', 20.0),
                defense_priority=initial_params.get('defense_priority', 20.0),
                infrastructure_priority=initial_params.get('infrastructure_priority', 20.0),
                social_priority=initial_params.get('social_priority', 20.0),
                social_transfers=initial_params.get('social_transfers', 0.0),
                reserve_ratio=initial_params.get('reserve_ratio', 0.1),
                refinance_rate=initial_params.get('refinance_rate', 0.05),
                printing_press_active=initial_params.get('printing_press_active', False)
            )
            
            # Рассчитываем начальные показатели
            indicators_data = enhanced_model.calculate_indicators(economic_params)
            
            # Создаем экономические показатели
            indicators = EconomicIndicators.objects.create(
                game_session=game_session,
                turn=1,
                gdp_absolute=indicators_data['gdp_absolute'],
                gdp_growth=indicators_data['gdp_growth'],
                inflation=indicators_data['inflation'],
                unemployment=indicators_data['unemployment'],
                president_rating=indicators_data['president_rating'],
                money_supply=indicators_data['money_supply'],
                gold_reserves=indicators_data['gold_reserves'],
                industry_output=indicators_data['industry_output'],
                services_output=indicators_data['services_output'],
                exchange_rate=indicators_data['exchange_rate'],
                external_debt=indicators_data['external_debt'],
                population=indicators_data['population'],
                interest_rate=indicators_data['interest_rate']
            )
            
            # Создаем бюджетные данные
            budget_data = BudgetData.objects.create(
                game_session=game_session,
                turn=1,
                total_revenue=indicators_data['budget']['total_revenue'],
                total_spending=indicators_data['budget']['total_spending'],
                budget_balance=indicators_data['budget']['budget_balance'],
                accumulated_reserves=indicators_data['budget']['accumulated_reserves'],
                social_transfers=indicators_data['budget']['social_transfers'],
                external_debt=indicators_data['budget']['external_debt']
            )
            
            # Обновляем игровую сессию
            game_session.indicators = indicators
            game_session.budget = budget_data
            game_session.save()
            
            # Формируем ответ
            game_data = {
                'id': game_session.id,
                'turn': game_session.current_turn,
                'model_type': game_session.model_type,
                'is_active': game_session.is_active,
                'indicators': {
                    'gdp_absolute': indicators.gdp_absolute,
                    'gdp_growth': indicators.gdp_growth,
                    'inflation': indicators.inflation,
                    'unemployment': indicators.unemployment,
                    'president_rating': indicators.president_rating,
                    'money_supply': indicators.money_supply,
                    'gold_reserves': indicators.gold_reserves,
                    'industry_output': indicators.industry_output,
                    'services_output': indicators.services_output,
                    'exchange_rate': indicators.exchange_rate,
                    'external_debt': indicators.external_debt,
                    'population': indicators.population,
                    'interest_rate': indicators.interest_rate
                },
                'budget': {
                    'total_revenue': budget_data.total_revenue,
                    'total_spending': budget_data.total_spending,
                    'budget_balance': budget_data.budget_balance,
                    'accumulated_reserves': budget_data.accumulated_reserves,
                    'social_transfers': budget_data.social_transfers,
                    'external_debt': budget_data.external_debt
                }
            }
            
            return Response({
                'success': True,
                'message': 'Расширенная игра успешно начата',
                'game': game_data
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({
            'error': f'Ошибка при создании расширенной игры: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def next_enhanced_turn(request, game_id):
    """Обработать следующий ход расширенной игры"""
    try:
        game_session = get_object_or_404(GameSession, id=game_id, user=request.user)
        
        # Получаем параметры из запроса
        parameters_data = request.data.get('parameters', {})
        
        with transaction.atomic():
            # Создаем расширенную экономическую модель
            enhanced_model = EnhancedEconomicModel()
            
            # Создаем параметры экономики
            economic_params = EconomicParameters(
                interest_rate=parameters_data.get('interest_rate', 5.0),
                tax_rate=parameters_data.get('tax_rate', 20.0),
                government_spending=parameters_data.get('government_spending', 25.0),
                customs_duty=parameters_data.get('customs_duty', 5.0),
                education_priority=parameters_data.get('education_priority', 20.0),
                healthcare_priority=parameters_data.get('healthcare_priority', 20.0),
                defense_priority=parameters_data.get('defense_priority', 20.0),
                infrastructure_priority=parameters_data.get('infrastructure_priority', 20.0),
                social_priority=parameters_data.get('social_priority', 20.0),
                social_transfers=parameters_data.get('social_transfers', 0.0),
                reserve_ratio=parameters_data.get('reserve_ratio', 0.1),
                refinance_rate=parameters_data.get('refinance_rate', 0.05),
                printing_press_active=parameters_data.get('printing_press_active', False)
            )
            
            # Рассчитываем новые показатели
            indicators_data = enhanced_model.calculate_indicators(economic_params)
            
            # Создаем новые экономические показатели
            indicators = EconomicIndicators.objects.create(
                game_session=game_session,
                turn=game_session.current_turn + 1,
                gdp_absolute=indicators_data['gdp_absolute'],
                gdp_growth=indicators_data['gdp_growth'],
                inflation=indicators_data['inflation'],
                unemployment=indicators_data['unemployment'],
                president_rating=indicators_data['president_rating'],
                money_supply=indicators_data['money_supply'],
                gold_reserves=indicators_data['gold_reserves'],
                investments=indicators_data.get('investments', 0),
                industry_output=indicators_data['industry_output'],
                services_output=indicators_data['services_output'],
                exchange_rate=indicators_data['exchange_rate'],
                external_debt=indicators_data['external_debt'],
                population=indicators_data['population'],
                interest_rate=indicators_data['interest_rate']
            )
            
            # Создаем новые бюджетные данные
            budget = BudgetData.objects.create(
                game_session=game_session,
                turn=game_session.current_turn + 1,
                tax_revenue=indicators_data['budget'].get('tax_revenue', 0),
                customs_revenue=indicators_data['budget'].get('customs_revenue', 0),
                total_revenue=indicators_data['budget']['total_revenue'],
                education_spending=indicators_data['budget'].get('education_spending', 0),
                healthcare_spending=indicators_data['budget'].get('healthcare_spending', 0),
                defense_spending=indicators_data['budget'].get('defense_spending', 0),
                infrastructure_spending=indicators_data['budget'].get('infrastructure_spending', 0),
                social_spending=indicators_data['budget'].get('social_spending', 0),
                total_spending=indicators_data['budget']['total_spending'],
                budget_balance=indicators_data['budget']['budget_balance'],
                accumulated_reserves=indicators_data['budget']['accumulated_reserves'],
                social_transfers=indicators_data['budget']['social_transfers'],
                external_debt=indicators_data['budget']['external_debt']
            )
            
            # Обновляем игровую сессию
            game_session.current_turn += 1
            game_session.save()
            
            # Проверяем кризис
            crisis = None
            crisis_data = indicators_data.get('crisis')
            if crisis_data and isinstance(crisis_data, dict) and 'type' in crisis_data:
                crisis = {
                    'type': crisis_data.get('type', ''),
                    'description': crisis_data.get('description', ''),
                    'effects': crisis_data.get('effects', {})
                }
            
            # Формируем ответ
            game_data = {
                'id': game_session.id,
                'turn': game_session.current_turn,
                'model_type': game_session.model_type,
                'is_active': game_session.is_active,
                'indicators': {
                    'gdp_absolute': indicators.gdp_absolute,
                    'gdp_growth': indicators.gdp_growth,
                    'inflation': indicators.inflation,
                    'unemployment': indicators.unemployment,
                    'president_rating': indicators.president_rating,
                    'money_supply': indicators.money_supply,
                    'gold_reserves': indicators.gold_reserves,
                    'industry_output': indicators.industry_output,
                    'services_output': indicators.services_output,
                    'exchange_rate': indicators.exchange_rate,
                    'external_debt': indicators.external_debt,
                    'population': indicators.population,
                    'interest_rate': indicators.interest_rate
                },
                'budget': {
                    'total_revenue': budget.total_revenue,
                    'total_spending': budget.total_spending,
                    'budget_balance': budget.budget_balance,
                    'accumulated_reserves': budget.accumulated_reserves,
                    'social_transfers': budget.social_transfers,
                    'external_debt': budget.external_debt
                }
            }
            
            if crisis:
                game_data['crisis'] = crisis
            
            return Response({
                'success': True,
                'message': 'Ход выполнен успешно',
                'game': game_data
            })
            
    except Exception as e:
        return Response({
            'error': f'Ошибка при выполнении хода: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_enhanced_game_state(request, game_id):
    """Получить состояние расширенной игры"""
    try:
        game_session = get_object_or_404(GameSession, id=game_id, user=request.user)
        
        indicators = game_session.indicators.order_by('-turn').first()
        budget = game_session.budget_data.order_by('-turn').first()
        
        if not indicators or not budget:
            return Response({
                'error': 'Данные игры не найдены'
            }, status=status.HTTP_404_NOT_FOUND)
        
        game_data = {
            'id': game_session.id,
            'turn': game_session.current_turn,
            'model_type': game_session.model_type,
            'is_active': game_session.is_active,
            'indicators': {
                'gdp_absolute': indicators.gdp_absolute,
                'gdp_growth': indicators.gdp_growth,
                'inflation': indicators.inflation,
                'unemployment': indicators.unemployment,
                'president_rating': indicators.president_rating,
                'money_supply': indicators.money_supply,
                'gold_reserves': indicators.gold_reserves,
                'industry_output': indicators.industry_output,
                'services_output': indicators.services_output,
                'exchange_rate': indicators.exchange_rate,
                'external_debt': indicators.external_debt,
                'population': indicators.population,
                'interest_rate': indicators.interest_rate
            },
            'budget': {
                'total_revenue': budget.total_revenue,
                'total_spending': budget.total_spending,
                'budget_balance': budget.budget_balance,
                'accumulated_reserves': budget.accumulated_reserves,
                'social_transfers': budget.social_transfers,
                'external_debt': budget.external_debt
            }
        }
        
        return Response({
            'success': True,
            'game': game_data
        })
        
    except Exception as e:
        return Response({
            'error': f'Ошибка получения состояния игры: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_enhanced_game_history(request, game_id):
    """Получить историю расширенной игры для построения графиков"""
    try:
        game = get_object_or_404(GameSession, id=game_id, user=request.user)
        
        # Получаем историю из базы данных
        history_entries = []
        
        # Получаем текущие данные
        current_indicators = game.indicators.order_by('-turn').first()
        current_budget = game.budget_data.order_by('-turn').first()
        
        if not current_indicators or not current_budget:
            return Response({
                'error': 'Данные игры не найдены'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Получаем текущее состояние
        current_state = {
            'turn': game.current_turn,
            'indicators': {
                'gdp_absolute': current_indicators.gdp_absolute,
                'gdp_growth': current_indicators.gdp_growth,
                'inflation': current_indicators.inflation,
                'unemployment': current_indicators.unemployment,
                'president_rating': current_indicators.president_rating,
                'money_supply': current_indicators.money_supply,
                'gold_reserves': current_indicators.gold_reserves,
                'industry_output': getattr(current_indicators, 'industry_output', 0),
                'services_output': getattr(current_indicators, 'services_output', 0),
                'exchange_rate': getattr(current_indicators, 'exchange_rate', 1.0),
                'external_debt': getattr(current_indicators, 'external_debt', 0),
                'population': getattr(current_indicators, 'population', 100),
                'interest_rate': getattr(current_indicators, 'interest_rate', 5.0),
            },
            'budget': {
                'total_revenue': current_budget.total_revenue,
                'total_spending': current_budget.total_spending,
                'budget_balance': current_budget.budget_balance,
                'accumulated_reserves': current_budget.accumulated_reserves,
                'social_transfers': getattr(current_budget, 'social_transfers', 0),
                'external_debt': getattr(current_budget, 'external_debt', 0),
            },
            'timestamp': game.updated_at.isoformat()
        }
        
        # Добавляем текущее состояние в историю
        history_entries.append(current_state)
        
        # В реальном приложении здесь бы была логика получения исторических данных
        # Пока возвращаем только текущее состояние
        return Response({
            'history': history_entries,
            'total_turns': game.current_turn
        })
        
    except Exception as e:
        return Response(
            {'error': f'Ошибка получения истории: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
