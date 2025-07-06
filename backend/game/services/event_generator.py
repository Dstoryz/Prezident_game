import random
from typing import List, Dict, Any


class EventGenerator:
    """Генератор случайных событий для игры"""
    
    def __init__(self):
        self.events_pool = {
            'natural_disaster': [
                {
                    'title': 'Землетрясение',
                    'description': 'Сильное землетрясение нанесло ущерб инфраструктуре',
                    'gdp_impact': -2.0,
                    'inflation_impact': 1.0,
                    'unemployment_impact': 1.0,
                    'rating_impact': -5.0
                },
                {
                    'title': 'Наводнение',
                    'description': 'Масштабное наводнение затронуло сельскохозяйственные регионы',
                    'gdp_impact': -1.5,
                    'inflation_impact': 2.0,
                    'unemployment_impact': 0.5,
                    'rating_impact': -3.0
                }
            ],
            'economic_crisis': [
                {
                    'title': 'Банковский кризис',
                    'description': 'Крупные банки столкнулись с проблемами ликвидности',
                    'gdp_impact': -3.0,
                    'inflation_impact': 0.5,
                    'unemployment_impact': 2.0,
                    'rating_impact': -8.0
                },
                {
                    'title': 'Кризис на рынке недвижимости',
                    'description': 'Резкое падение цен на недвижимость',
                    'gdp_impact': -2.0,
                    'inflation_impact': -1.0,
                    'unemployment_impact': 1.5,
                    'rating_impact': -6.0
                }
            ],
            'sanctions': [
                {
                    'title': 'Международные санкции',
                    'description': 'Западные страны ввели экономические санкции',
                    'gdp_impact': -1.5,
                    'inflation_impact': 1.5,
                    'unemployment_impact': 1.0,
                    'rating_impact': -4.0
                },
                {
                    'title': 'Торговые ограничения',
                    'description': 'Ограничения на импорт ключевых товаров',
                    'gdp_impact': -1.0,
                    'inflation_impact': 2.0,
                    'unemployment_impact': 0.5,
                    'rating_impact': -3.0
                }
            ],
            'international_conflict': [
                {
                    'title': 'Международный конфликт',
                    'description': 'Напряженность в международных отношениях',
                    'gdp_impact': -1.0,
                    'inflation_impact': 1.0,
                    'unemployment_impact': 0.5,
                    'rating_impact': -2.0
                },
                {
                    'title': 'Торговая война',
                    'description': 'Эскалация торговых споров с партнерами',
                    'gdp_impact': -1.5,
                    'inflation_impact': 1.5,
                    'unemployment_impact': 1.0,
                    'rating_impact': -4.0
                }
            ],
            'commodity_price_change': [
                {
                    'title': 'Рост цен на нефть',
                    'description': 'Резкий рост мировых цен на нефть',
                    'gdp_impact': 1.0,
                    'inflation_impact': 2.0,
                    'unemployment_impact': -0.5,
                    'rating_impact': 2.0
                },
                {
                    'title': 'Падение цен на сырье',
                    'description': 'Снижение мировых цен на экспортное сырье',
                    'gdp_impact': -1.0,
                    'inflation_impact': -0.5,
                    'unemployment_impact': 0.5,
                    'rating_impact': -2.0
                }
            ],
            'social_protest': [
                {
                    'title': 'Массовые протесты',
                    'description': 'Народные выступления против экономической политики',
                    'gdp_impact': -0.5,
                    'inflation_impact': 0.5,
                    'unemployment_impact': 0.5,
                    'rating_impact': -10.0
                },
                {
                    'title': 'Забастовки',
                    'description': 'Крупные забастовки в ключевых отраслях',
                    'gdp_impact': -1.0,
                    'inflation_impact': 0.5,
                    'unemployment_impact': 1.0,
                    'rating_impact': -5.0
                }
            ]
        }
    
    def generate_events(self, turn: int, current_rating: float = 50.0) -> List[Dict[str, Any]]:
        """Генерировать события для текущего хода"""
        events = []
        
        # Базовая вероятность события (15%)
        base_probability = 0.15
        
        # Увеличиваем вероятность при низком рейтинге
        if current_rating < 30:
            base_probability = 0.25
        elif current_rating < 50:
            base_probability = 0.20
        
        # Проверяем каждую категорию событий
        for event_type, event_list in self.events_pool.items():
            if random.random() < base_probability:
                event = random.choice(event_list).copy()
                event['event_type'] = event_type
                events.append(event)
        
        # Ограничиваем количество событий за ход
        if len(events) > 2:
            events = random.sample(events, 2)
        
        return events
    
    def get_event_by_type(self, event_type: str) -> Dict[str, Any]:
        """Получить случайное событие определенного типа"""
        if event_type in self.events_pool:
            event = random.choice(self.events_pool[event_type]).copy()
            event['event_type'] = event_type
            return event
        return None 