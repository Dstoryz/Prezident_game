from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.http import JsonResponse
from .models import GameSession, EconomicIndicators, BudgetData, GameParameters
from .services.enhanced_economic_model import EnhancedEconomicModel
from .serializers import GameSessionSerializer, EconomicIndicatorsSerializer
import json

@api_view(['POST'])
@permission_classes([AllowAny])
def create_new_game(request):
    """Создание новой игровой сессии"""
    try:
        # Получение параметров из запроса
        data = request.data if hasattr(request, 'data') else json.loads(request.body)
        
        # Создание экономической модели
        model = EnhancedEconomicModel()
        
        # Инициализация начальных параметров
        initial_params = {
            'gdp': data.get('gdp', 1000000),  # Начальный ВВП
            'population': data.get('population', 100000),  # Население
            'inflation': data.get('inflation', 2.0),  # Инфляция
            'unemployment': data.get('unemployment', 5.0),  # Безработица
            'budget_deficit': data.get('budget_deficit', 0.0),  # Дефицит бюджета
        }
        
        # Создание игровой сессии (используем правильные поля модели)
        game_session = GameSession.objects.create(
            user_id=1,  # Временный пользователь
            current_turn=1,
            current_year=2024,
            current_quarter=1,
            model_type='enhanced',
            budget=initial_params['gdp'] * 0.1,  # 10% от ВВП как начальный бюджет
            accumulated_reserves=initial_params['gdp'] * 0.05  # 5% от ВВП как резервы
        )
        
        # Создание параметров игры
        game_parameters = GameParameters.objects.create(
            game_session=game_session,
            interest_rate=5.0,
            tax_rate=20.0,
            government_spending=25.0,
            customs_duty=5.0,
            education_priority=20.0,
            healthcare_priority=20.0,
            defense_priority=20.0,
            infrastructure_priority=20.0,
            social_priority=20.0
        )
        
        # Создание начальных экономических показателей
        economic_data = model.initialize_economy(initial_params)
        
        economic_indicators = EconomicIndicators.objects.create(
            game_session=game_session,
            turn=1,
            gdp_growth=economic_data.get('gdp_growth', 0.0),
            gdp_absolute=economic_data.get('gdp_absolute', initial_params['gdp']),
            inflation=economic_data.get('inflation', initial_params['inflation']),
            unemployment=economic_data.get('unemployment', initial_params['unemployment']),
            investments=economic_data.get('investments', 20.0),
            president_rating=economic_data.get('president_rating', 50.0),
            public_mood=economic_data.get('public_mood', 50.0),
            export_volume=economic_data.get('export_volume', 30.0),
            import_volume=economic_data.get('import_volume', 25.0),
            money_supply=economic_data.get('money_supply', initial_params['gdp'] * 0.8),
            gold_reserves=economic_data.get('gold_reserves', 100.0),
            reserve_ratio=economic_data.get('reserve_ratio', 0.1),
            refinance_rate=economic_data.get('refinance_rate', 0.05),
            industry_output=economic_data.get('industry_output', initial_params['gdp'] * 0.6),
            services_output=economic_data.get('services_output', initial_params['gdp'] * 0.4),
            exchange_rate=economic_data.get('exchange_rate', 1.0),
            external_debt=economic_data.get('external_debt', 0.0),
            population=economic_data.get('population', initial_params['population'] / 1000000),  # Конвертируем в миллионы
            interest_rate=economic_data.get('interest_rate', 5.0)
        )
        
        # Создание бюджетных данных
        budget_data = BudgetData.objects.create(
            game_session=game_session,
            turn=1,
            tax_revenue=economic_data.get('tax_revenue', initial_params['gdp'] * 0.2),
            customs_revenue=economic_data.get('customs_revenue', initial_params['gdp'] * 0.05),
            total_revenue=economic_data.get('total_revenue', initial_params['gdp'] * 0.25),
            education_spending=economic_data.get('education_spending', initial_params['gdp'] * 0.05),
            healthcare_spending=economic_data.get('healthcare_spending', initial_params['gdp'] * 0.05),
            defense_spending=economic_data.get('defense_spending', initial_params['gdp'] * 0.05),
            infrastructure_spending=economic_data.get('infrastructure_spending', initial_params['gdp'] * 0.05),
            social_spending=economic_data.get('social_spending', initial_params['gdp'] * 0.05),
            total_spending=economic_data.get('total_spending', initial_params['gdp'] * 0.25),
            social_transfers=economic_data.get('social_transfers', initial_params['gdp'] * 0.1),
            budget_balance=economic_data.get('budget_balance', 0.0),
            accumulated_reserves=economic_data.get('accumulated_reserves', initial_params['gdp'] * 0.05),
            gold_reserves=economic_data.get('gold_reserves', 100.0),
            external_debt=economic_data.get('external_debt', 0.0)
        )
        
        # Подготовка ответа
        response_data = {
            'game_id': game_session.id,
            'player_name': data.get('player_name', 'Игрок'),
            'difficulty': data.get('difficulty', 'medium'),
            'status': 'created',
            'economic_indicators': {
                'gdp': economic_indicators.gdp_absolute,
                'gdp_growth': economic_indicators.gdp_growth,
                'inflation': economic_indicators.inflation,
                'unemployment': economic_indicators.unemployment,
                'interest_rate': economic_indicators.interest_rate,
                'exchange_rate': economic_indicators.exchange_rate,
                'president_rating': economic_indicators.president_rating,
                'public_mood': economic_indicators.public_mood
            },
            'budget_data': {
                'revenue': budget_data.total_revenue,
                'expenses': budget_data.total_spending,
                'deficit': budget_data.budget_balance,
                'debt': budget_data.external_debt,
                'reserves': budget_data.accumulated_reserves
            },
            'parameters': {
                'interest_rate': game_parameters.interest_rate,
                'tax_rate': game_parameters.tax_rate,
                'government_spending': game_parameters.government_spending
            },
            'message': 'Новая игра успешно создана!'
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'Ошибка при создании игры'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def game_status(request, game_id):
    """Получение статуса игры"""
    try:
        game_session = GameSession.objects.get(id=game_id)
        economic_indicators = EconomicIndicators.objects.filter(game_session=game_session).first()
        budget_data = BudgetData.objects.filter(game_session=game_session).first()
        parameters = GameParameters.objects.filter(game_session=game_session).first()
        
        response_data = {
            'game_id': game_session.id,
            'current_turn': game_session.current_turn,
            'current_year': game_session.current_year,
            'current_quarter': game_session.current_quarter,
            'model_type': game_session.model_type,
            'status': 'active' if game_session.is_active else 'inactive',
            'economic_indicators': {
                'gdp': economic_indicators.gdp_absolute if economic_indicators else 0,
                'gdp_growth': economic_indicators.gdp_growth if economic_indicators else 0,
                'inflation': economic_indicators.inflation if economic_indicators else 0,
                'unemployment': economic_indicators.unemployment if economic_indicators else 0,
                'interest_rate': economic_indicators.interest_rate if economic_indicators else 0,
                'exchange_rate': economic_indicators.exchange_rate if economic_indicators else 1.0,
                'president_rating': economic_indicators.president_rating if economic_indicators else 0,
                'public_mood': economic_indicators.public_mood if economic_indicators else 50.0
            } if economic_indicators else None,
            'budget_data': {
                'revenue': budget_data.total_revenue if budget_data else 0,
                'expenses': budget_data.total_spending if budget_data else 0,
                'deficit': budget_data.budget_balance if budget_data else 0,
                'debt': budget_data.external_debt if budget_data else 0,
                'reserves': budget_data.accumulated_reserves if budget_data else 0
            } if budget_data else None,
            'parameters': {
                'interest_rate': parameters.interest_rate if parameters else 5.0,
                'tax_rate': parameters.tax_rate if parameters else 20.0,
                'government_spending': parameters.government_spending if parameters else 25.0
            } if parameters else None
        }
        
        return Response(response_data)
        
    except GameSession.DoesNotExist:
        return Response({
            'error': 'Игра не найдена'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': str(e),
            'message': 'Ошибка при получении статуса игры'
        }, status=status.HTTP_400_BAD_REQUEST)
