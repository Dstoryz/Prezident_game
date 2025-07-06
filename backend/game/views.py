from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import GameSession, GameParameters, EconomicIndicators, GameEvent, GameHistory
from .serializers import (
    GameSessionSerializer, GameParametersSerializer, EconomicIndicatorsSerializer,
    GameEventSerializer, NextTurnRequestSerializer
)
from .services.game_engine import GameEngine


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_game(request):
    """Начать новую игру"""
    try:
        # Создаем новую игровую сессию
        game_session = GameSession.objects.create(user=request.user)
        
        # Создаем параметры по умолчанию
        parameters = GameParameters.objects.create(game_session=game_session)
        
        # Запускаем игровой движок
        game_engine = GameEngine()
        initial_state = game_engine.start_new_game()
        
        # Создаем начальные показатели
        indicators = EconomicIndicators.objects.create(
            game_session=game_session,
            turn=1,
            **initial_state['indicators']
        )
        
        # Обновляем сессию
        game_session.current_turn = initial_state['turn']
        game_session.current_year = initial_state['year']
        game_session.current_quarter = initial_state['quarter']
        game_session.save()
        
        # Возвращаем данные игры
        serializer = GameSessionSerializer(game_session)
        return Response({
            'success': True,
            'message': 'Игра успешно начата',
            'game': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Ошибка при создании игры: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def next_turn(request, game_id):
    """Обработать следующий ход"""
    try:
        # Получаем игровую сессию
        game_session = get_object_or_404(GameSession, id=game_id, user=request.user, is_active=True)
        
        # Валидируем входные данные
        serializer = NextTurnRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Неверные параметры',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Получаем текущее состояние игры
        current_parameters = GameParametersSerializer(game_session.parameters).data
        current_indicators = EconomicIndicatorsSerializer(
            game_session.indicators.filter(turn=game_session.current_turn).first()
        ).data
        
        current_state = {
            'parameters': current_parameters,
            'indicators': current_indicators,
            'turn': game_session.current_turn,
            'year': game_session.current_year,
            'quarter': game_session.current_quarter,
            'elections_passed': game_session.elections_passed
        }
        
        # Обрабатываем следующий ход
        game_engine = GameEngine()
        new_state = game_engine.process_next_turn(current_state, serializer.validated_data)
        
        # Обновляем параметры
        for key, value in new_state['parameters'].items():
            setattr(game_session.parameters, key, value)
        game_session.parameters.save()
        
        # Создаем новые показатели
        new_indicators = EconomicIndicators.objects.create(
            game_session=game_session,
            turn=new_state['turn'],
            **new_state['indicators']
        )
        
        # Создаем события
        events = []
        for event_data in new_state['events']:
            event = GameEvent.objects.create(
                game_session=game_session,
                turn=new_state['turn'],
                **event_data
            )
            events.append(GameEventSerializer(event).data)
        
        # Обновляем сессию
        game_session.current_turn = new_state['turn']
        game_session.current_year = new_state['year']
        game_session.current_quarter = new_state['quarter']
        game_session.elections_passed = new_state['elections_passed']
        
        # Проверяем окончание игры
        if new_state.get('game_over', False):
            game_session.is_active = False
        
        game_session.save()
        
        # Сохраняем историю
        GameHistory.objects.create(
            game_session=game_session,
            turn=new_state['turn'],
            parameters_data=new_state['parameters'],
            indicators_data=new_state['indicators'],
            events_data=events
        )
        
        # Возвращаем результат
        return Response({
            'success': True,
            'message': 'Ход обработан успешно',
            'game': GameSessionSerializer(game_session).data,
            'new_indicators': EconomicIndicatorsSerializer(new_indicators).data,
            'events': events,
            'game_over': new_state.get('game_over', False),
            'game_over_reason': new_state.get('game_over_reason')
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Ошибка при обработке хода: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def game_state(request, game_id):
    """Получить текущее состояние игры"""
    try:
        game_session = get_object_or_404(GameSession, id=game_id, user=request.user)
        
        serializer = GameSessionSerializer(game_session)
        return Response({
            'success': True,
            'game': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Ошибка при получении состояния игры: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def game_history(request, game_id):
    """Получить историю игры"""
    try:
        game_session = get_object_or_404(GameSession, id=game_id, user=request.user)
        
        # Получаем историю показателей
        indicators_history = EconomicIndicators.objects.filter(
            game_session=game_session
        ).order_by('turn')
        
        # Получаем историю событий
        events_history = GameEvent.objects.filter(
            game_session=game_session
        ).order_by('turn')
        
        return Response({
            'success': True,
            'indicators_history': EconomicIndicatorsSerializer(indicators_history, many=True).data,
            'events_history': GameEventSerializer(events_history, many=True).data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Ошибка при получении истории: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
