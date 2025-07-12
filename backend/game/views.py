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
        
        # Инициализация начальных параметров для Беларуси
        initial_params = {
            'gdp': data.get('gdp', 60_000_000_000),  # ~60 млрд USD
            'population': data.get('population', 9_400_000),  # ~9.4 млн человек
            'inflation': data.get('inflation', 6.0),  # ~6% годовых
            'unemployment': data.get('unemployment', 4.0),  # ~4%
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
            population=economic_data.get('population', initial_params['population']),  # Население в абсолютных числах
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

@api_view(['GET'])
@permission_classes([AllowAny])
def get_game_state(request, game_id):
    """Получение состояния игры для frontend"""
    try:
        game_session = GameSession.objects.get(id=game_id)
        economic_indicators = EconomicIndicators.objects.filter(game_session=game_session).order_by('-turn').first()
        budget_data = BudgetData.objects.filter(game_session=game_session).order_by('-turn').first()
        parameters = GameParameters.objects.filter(game_session=game_session).first()
        
        response_data = {
            'success': True,
            'game': {
                'id': game_session.id,
                'turn': game_session.current_turn,
                'current_turn': game_session.current_turn,
                'current_year': game_session.current_year,
                'current_quarter': game_session.current_quarter,
                'model_type': game_session.model_type,
                'is_active': game_session.is_active,
                'current_indicators': {
                    'gdp_growth': economic_indicators.gdp_growth if economic_indicators else 0.0,
                    'gdp_absolute': economic_indicators.gdp_absolute if economic_indicators else 0.0,
                    'inflation': economic_indicators.inflation if economic_indicators else 0.0,
                    'unemployment': economic_indicators.unemployment if economic_indicators else 0.0,
                    'president_rating': economic_indicators.president_rating if economic_indicators else 50.0,
                    'public_mood': economic_indicators.public_mood if economic_indicators else 50.0,
                    'investments': economic_indicators.investments if economic_indicators else 0.0,
                    'export_volume': economic_indicators.export_volume if economic_indicators else 0.0,
                    'import_volume': economic_indicators.import_volume if economic_indicators else 0.0,
                    'money_supply': economic_indicators.money_supply if economic_indicators else 0.0,
                    'gold_reserves': economic_indicators.gold_reserves if economic_indicators else 0.0,
                    'industry_output': economic_indicators.industry_output if economic_indicators else 0.0,
                    'services_output': economic_indicators.services_output if economic_indicators else 0.0,
                    'exchange_rate': economic_indicators.exchange_rate if economic_indicators else 1.0,
                    'external_debt': economic_indicators.external_debt if economic_indicators else 0.0,
                    'population': economic_indicators.population if economic_indicators else 0.0,
                    'interest_rate': economic_indicators.interest_rate if economic_indicators else 5.0,
                    'reserve_ratio': economic_indicators.reserve_ratio if economic_indicators else 0.1,
                    'refinance_rate': economic_indicators.refinance_rate if economic_indicators else 0.05,
                    'printing_press_active': False
                },
                'current_budget': {
                    'total_revenue': budget_data.total_revenue if budget_data else 0.0,
                    'total_spending': budget_data.total_spending if budget_data else 0.0,
                    'budget_balance': budget_data.budget_balance if budget_data else 0.0,
                    'social_transfers': budget_data.social_transfers if budget_data else 0.0,
                    'accumulated_reserves': budget_data.accumulated_reserves if budget_data else 0.0,
                    'external_debt': budget_data.external_debt if budget_data else 0.0,
                    'gold_reserves': budget_data.gold_reserves if budget_data else 0.0
                },
                'parameters': {
                    'interest_rate': parameters.interest_rate if parameters else 5.0,
                    'tax_rate': parameters.tax_rate if parameters else 20.0,
                    'government_spending': parameters.government_spending if parameters else 25.0,
                    'customs_duty': parameters.customs_duty if parameters else 5.0,
                    'education_priority': parameters.education_priority if parameters else 20.0,
                    'healthcare_priority': parameters.healthcare_priority if parameters else 20.0,
                    'defense_priority': parameters.defense_priority if parameters else 20.0,
                    'infrastructure_priority': parameters.infrastructure_priority if parameters else 20.0,
                    'social_priority': parameters.social_priority if parameters else 20.0,
                    'social_transfers': 0.0,
                    'reserve_ratio': 0.1,
                    'refinance_rate': 0.05,
                    'printing_press_active': False
                },
                'current_events': []
            }
        }
        
        return Response(response_data)
        
    except GameSession.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Игра не найдена'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Ошибка при получении состояния игры'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def next_turn(request, game_id):
    """Следующий ход в игре"""
    try:
        game_session = GameSession.objects.get(id=game_id)
        parameters_data = request.data
        
        # Создание экономической модели
        model = EnhancedEconomicModel()
        
        # Получение текущих показателей
        current_indicators = EconomicIndicators.objects.filter(game_session=game_session).order_by('-turn').first()
        current_budget = BudgetData.objects.filter(game_session=game_session).order_by('-turn').first()
        
        # Создание параметров для модели
        economic_params = type('EconomicParameters', (), {
            'interest_rate': parameters_data.get('interest_rate', 5.0),
            'tax_rate': parameters_data.get('tax_rate', 20.0),
            'government_spending': parameters_data.get('government_spending', 25.0),
            'customs_duty': parameters_data.get('customs_duty', 5.0),
            'education_priority': parameters_data.get('education_priority', 20.0),
            'healthcare_priority': parameters_data.get('healthcare_priority', 20.0),
            'defense_priority': parameters_data.get('defense_priority', 20.0),
            'infrastructure_priority': parameters_data.get('infrastructure_priority', 20.0),
            'social_priority': parameters_data.get('social_priority', 20.0),
            'social_transfers': parameters_data.get('social_transfers', 0.0),
            'reserve_ratio': parameters_data.get('reserve_ratio', 0.1),
            'refinance_rate': parameters_data.get('refinance_rate', 0.05),
            'printing_press_active': parameters_data.get('printing_press_active', False)
        })()
        
        # Предыдущие показатели для расчета
        previous_indicators = {
            'total_gdp': current_indicators.gdp_absolute if current_indicators else 1000000,
            'inflation': current_indicators.inflation if current_indicators else 2.0,
            'unemployment': current_indicators.unemployment if current_indicators else 5.0,
            'exchange_rate': current_indicators.exchange_rate if current_indicators else 1.0,
            'money_supply': current_indicators.money_supply if current_indicators else 800000,
            'gold_reserves': current_indicators.gold_reserves if current_indicators else 100.0,
            'external_debt': current_indicators.external_debt if current_indicators else 0.0,
            'population': current_indicators.population if current_indicators else 1.0,
            'public_mood': current_indicators.public_mood if current_indicators else 50.0,
            'industry_capital': current_indicators.industry_output if current_indicators else 600000,
            'services_capital': current_indicators.services_output if current_indicators else 400000,
            'industry_labor': 0.35,
            'services_labor': 0.65,
            'industry_technology': 1.0,
            'services_technology': 1.0
        }
        
        # Расчет новых показателей
        new_indicators = model.calculate_indicators(economic_params, previous_indicators)
        
        # Обновление игровой сессии
        game_session.current_turn += 1
        game_session.current_quarter = ((game_session.current_turn - 1) % 4) + 1
        game_session.current_year = 2024 + ((game_session.current_turn - 1) // 4)
        game_session.save()
        
        # Создание новых экономических показателей
        new_economic_indicators = EconomicIndicators.objects.create(
            game_session=game_session,
            turn=game_session.current_turn,
            gdp_growth=new_indicators['gdp_growth'],
            gdp_absolute=new_indicators['total_gdp'],
            inflation=new_indicators['inflation'],
            unemployment=new_indicators['unemployment'],
            investments=new_indicators['investments'],
            president_rating=new_indicators['president_rating'],
            public_mood=new_indicators['public_mood'],
            export_volume=new_indicators['exports'],
            import_volume=new_indicators['imports'],
            money_supply=new_indicators['money_supply'],
            gold_reserves=new_indicators['gold_reserves'],
            reserve_ratio=new_indicators.get('reserve_ratio', 0.1),
            refinance_rate=new_indicators.get('refinance_rate', 0.05),
            industry_output=new_indicators['industry_output'],
            services_output=new_indicators['services_output'],
            exchange_rate=new_indicators['exchange_rate'],
            external_debt=new_indicators['external_debt'],
            population=new_indicators['population'],
            interest_rate=new_indicators['interest_rate']
        )
        
        # Создание новых бюджетных данных
        new_budget_data = BudgetData.objects.create(
            game_session=game_session,
            turn=game_session.current_turn,
            tax_revenue=new_indicators['tax_revenue'],
            customs_revenue=new_indicators.get('customs_revenue', 0.0),
            total_revenue=new_indicators['total_revenue'],
            education_spending=new_indicators['education_spending'],
            healthcare_spending=new_indicators['healthcare_spending'],
            defense_spending=new_indicators['defense_spending'],
            infrastructure_spending=new_indicators['infrastructure_spending'],
            social_spending=new_indicators['social_spending'],
            total_spending=new_indicators['total_spending'],
            social_transfers=new_indicators['social_transfers'],
            budget_balance=new_indicators['budget_balance'],
            accumulated_reserves=new_indicators['budget']['accumulated_reserves'],
            gold_reserves=new_indicators['gold_reserves'],
            external_debt=new_indicators['external_debt']
        )
        
        # Обновление параметров игры
        if parameters_data:
            GameParameters.objects.filter(game_session=game_session).update(
                interest_rate=parameters_data.get('interest_rate', 5.0),
                tax_rate=parameters_data.get('tax_rate', 20.0),
                government_spending=parameters_data.get('government_spending', 25.0),
                customs_duty=parameters_data.get('customs_duty', 5.0),
                education_priority=parameters_data.get('education_priority', 20.0),
                healthcare_priority=parameters_data.get('healthcare_priority', 20.0),
                defense_priority=parameters_data.get('defense_priority', 20.0),
                infrastructure_priority=parameters_data.get('infrastructure_priority', 20.0),
                social_priority=parameters_data.get('social_priority', 20.0)
            )
        
        # Подготовка ответа
        response_data = {
            'success': True,
            'game': {
                'id': game_session.id,
                'turn': game_session.current_turn,
                'current_turn': game_session.current_turn,
                'current_year': game_session.current_year,
                'current_quarter': game_session.current_quarter,
                'model_type': game_session.model_type,
                'is_active': game_session.is_active,
                'current_indicators': {
                    'gdp_growth': new_indicators['gdp_growth'],
                    'gdp_absolute': new_indicators['total_gdp'],
                    'inflation': new_indicators['inflation'],
                    'unemployment': new_indicators['unemployment'],
                    'president_rating': new_indicators['president_rating'],
                    'public_mood': new_indicators['public_mood'],
                    'investments': new_indicators['investments'],
                    'export_volume': new_indicators['exports'],
                    'import_volume': new_indicators['imports'],
                    'money_supply': new_indicators['money_supply'],
                    'gold_reserves': new_indicators['gold_reserves'],
                    'industry_output': new_indicators['industry_output'],
                    'services_output': new_indicators['services_output'],
                    'exchange_rate': new_indicators['exchange_rate'],
                    'external_debt': new_indicators['external_debt'],
                    'population': new_indicators['population'],
                    'interest_rate': new_indicators['interest_rate'],
                    'reserve_ratio': new_indicators.get('reserve_ratio', 0.1),
                    'refinance_rate': new_indicators.get('refinance_rate', 0.05),
                    'printing_press_active': parameters_data.get('printing_press_active', False)
                },
                'current_budget': {
                    'total_revenue': new_indicators['total_revenue'],
                    'total_spending': new_indicators['total_spending'],
                    'budget_balance': new_indicators['budget_balance'],
                    'social_transfers': new_indicators['social_transfers'],
                    'accumulated_reserves': new_indicators['budget']['accumulated_reserves'],
                    'external_debt': new_indicators['external_debt'],
                    'gold_reserves': new_indicators['gold_reserves']
                },
                'parameters': parameters_data,
                'current_events': []
            },
            'game_over': False,
            'game_over_reason': None
        }
        
        return Response(response_data)
        
    except GameSession.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Игра не найдена'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Ошибка при выполнении хода'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_game_history(request, game_id):
    """Получение истории игры для графиков"""
    try:
        game_session = GameSession.objects.get(id=game_id)
        indicators_history = EconomicIndicators.objects.filter(game_session=game_session).order_by('turn')
        
        history_data = []
        for indicator in indicators_history:
            history_data.append({
                'turn': indicator.turn,
                'indicators_data': {
                    'gdp_growth': indicator.gdp_growth,
                    'gdp_absolute': indicator.gdp_absolute,
                    'inflation': indicator.inflation,
                    'unemployment': indicator.unemployment,
                    'president_rating': indicator.president_rating,
                    'public_mood': indicator.public_mood,
                    'investments': indicator.investments,
                    'export_volume': indicator.export_volume,
                    'import_volume': indicator.import_volume,
                    'money_supply': indicator.money_supply,
                    'gold_reserves': indicator.gold_reserves,
                    'industry_output': indicator.industry_output,
                    'services_output': indicator.services_output,
                    'exchange_rate': indicator.exchange_rate,
                    'external_debt': indicator.external_debt,
                    'population': indicator.population,
                    'interest_rate': indicator.interest_rate
                }
            })
        
        return Response({
            'success': True,
            'history': history_data
        })
        
    except GameSession.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Игра не найдена'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e),
            'message': 'Ошибка при получении истории игры'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def enhanced_game_state(request, game_id):
    """Расширенное состояние игры для расширенного фронтенда"""
    try:
        game_session = GameSession.objects.get(id=game_id)
        economic_indicators = EconomicIndicators.objects.filter(game_session=game_session).order_by('-turn').first()
        budget_data = BudgetData.objects.filter(game_session=game_session).order_by('-turn').first()
        # Можно добавить обработку кризисов, если есть
        crisis = None
        indicators = {
            'gdp_absolute': economic_indicators.gdp_absolute if economic_indicators else 0.0,
            'gdp_growth': economic_indicators.gdp_growth if economic_indicators else 0.0,
            'industry_output': economic_indicators.industry_output if economic_indicators else 0.0,
            'services_output': economic_indicators.services_output if economic_indicators else 0.0,
            'inflation': economic_indicators.inflation if economic_indicators else 0.0,
            'unemployment': economic_indicators.unemployment if economic_indicators else 0.0,
            'president_rating': economic_indicators.president_rating if economic_indicators else 50.0,
            'public_mood': economic_indicators.public_mood if economic_indicators else 50.0,
            'investments': economic_indicators.investments if economic_indicators else 0.0,
            'export_volume': economic_indicators.export_volume if economic_indicators else 0.0,
            'import_volume': economic_indicators.import_volume if economic_indicators else 0.0,
            'money_supply': economic_indicators.money_supply if economic_indicators else 0.0,
            'gold_reserves': economic_indicators.gold_reserves if economic_indicators else 0.0,
            'exchange_rate': economic_indicators.exchange_rate if economic_indicators else 1.0,
            'external_debt': economic_indicators.external_debt if economic_indicators else 0.0,
            'population': economic_indicators.population if economic_indicators else 0.0,
            'interest_rate': economic_indicators.interest_rate if economic_indicators else 5.0,
            'reserve_ratio': economic_indicators.reserve_ratio if economic_indicators else 0.1,
            'refinance_rate': economic_indicators.refinance_rate if economic_indicators else 0.05,
            'printing_press_active': False
        }
        budget = {
            'total_revenue': budget_data.total_revenue if budget_data else 0.0,
            'total_spending': budget_data.total_spending if budget_data else 0.0,
            'budget_balance': budget_data.budget_balance if budget_data else 0.0,
            'social_transfers': budget_data.social_transfers if budget_data else 0.0,
            'accumulated_reserves': budget_data.accumulated_reserves if budget_data else 0.0,
            'external_debt': budget_data.external_debt if budget_data else 0.0,
            'gold_reserves': budget_data.gold_reserves if budget_data else 0.0
        }
        response_data = {
            'game': {
                'id': game_session.id,
                'turn': game_session.current_turn,
                'model_type': game_session.model_type,
                'indicators': indicators,
                'budget': budget,
                'crisis': crisis
            }
        }
        return Response(response_data)
    except GameSession.DoesNotExist:
        return Response({'error': 'Игра не найдена'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
