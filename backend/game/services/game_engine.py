from typing import Dict, Any, Optional
from .economic_logic import EconomicEngine
from .event_generator import EventGenerator


class GameEngine:
    """Основной игровой движок"""
    
    def __init__(self):
        self.economic_engine = EconomicEngine()
        self.event_generator = EventGenerator()
    
    def start_new_game(self) -> Dict[str, Any]:
        """Начать новую игру"""
        # Создаем начальные показатели
        initial_parameters = {
            'interest_rate': 5.0,
            'tax_rate': 20.0,
            'government_spending': 25.0,
            'customs_duty': 5.0
        }
        
        initial_indicators = self.economic_engine.calculate_indicators(initial_parameters)
        
        return {
            'parameters': initial_parameters,
            'indicators': initial_indicators,
            'events': [],
            'turn': 1,
            'year': 2024,
            'quarter': 1,
            'elections_passed': 0
        }
    
    def process_next_turn(self, current_state: Dict[str, Any], 
                         new_parameters: Dict[str, float]) -> Dict[str, Any]:
        """Обработать следующий ход"""
        
        # Обновляем параметры
        parameters = current_state.get('parameters', {}).copy()
        parameters.update(new_parameters)
        
        # Получаем предыдущие показатели
        previous_indicators = current_state.get('indicators', {})
        
        # Рассчитываем новые показатели
        new_indicators = self.economic_engine.calculate_indicators(
            parameters, previous_indicators
        )
        
        # Генерируем события
        current_rating = new_indicators.get('president_rating', 50.0)
        events = self.event_generator.generate_events(
            current_state.get('turn', 1), current_rating
        )
        
        # Применяем влияние событий
        if events:
            new_indicators = self.economic_engine.apply_event_impacts(new_indicators, events)
        
        # Обновляем время
        current_turn = current_state.get('turn', 1)
        current_year = current_state.get('year', 2024)
        current_quarter = current_state.get('quarter', 1)
        elections_passed = current_state.get('elections_passed', 0)
        
        # Переходим к следующему кварталу
        current_turn += 1
        current_quarter += 1
        
        if current_quarter > 4:
            current_quarter = 1
            current_year += 1
            
            # Проверяем выборы каждые 4 года
            if (current_year - 2024) % 4 == 0:
                elections_passed += 1
        
        # Проверяем условия окончания игры
        game_over = False
        game_over_reason = None
        
        if new_indicators.get('president_rating', 50.0) < 50.0 and elections_passed > 0:
            game_over = True
            game_over_reason = "Потеря поддержки населения"
        
        return {
            'parameters': parameters,
            'indicators': new_indicators,
            'events': events,
            'turn': current_turn,
            'year': current_year,
            'quarter': current_quarter,
            'elections_passed': elections_passed,
            'game_over': game_over,
            'game_over_reason': game_over_reason
        }
    
    def check_elections(self, current_state: Dict[str, Any]) -> Dict[str, Any]:
        """Проверить результаты выборов"""
        current_rating = current_state.get('indicators', {}).get('president_rating', 50.0)
        elections_passed = current_state.get('elections_passed', 0)
        
        if elections_passed == 0:
            return {
                'elections_this_turn': False,
                'election_result': None,
                'game_over': False
            }
        
        # Проверяем каждые 4 года (16 ходов)
        if current_state.get('turn', 1) % 16 == 0:
            if current_rating < 50.0:
                return {
                    'elections_this_turn': True,
                    'election_result': 'defeat',
                    'game_over': True,
                    'reason': f'Потеря выборов. Рейтинг: {current_rating:.1f}%'
                }
            else:
                return {
                    'elections_this_turn': True,
                    'election_result': 'victory',
                    'game_over': False,
                    'reason': f'Победа на выборах. Рейтинг: {current_rating:.1f}%'
                }
        
        return {
            'elections_this_turn': False,
            'election_result': None,
            'game_over': False
        } 