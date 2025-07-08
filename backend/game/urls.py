from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import EnhancedGameViewSet

# Создаем роутер для ViewSet
router = DefaultRouter()
router.register(r'enhanced', EnhancedGameViewSet, basename='enhanced-game')

urlpatterns = [
    path('start/', views.start_game, name='start_game'),
    path('<int:game_id>/next-turn/', views.next_turn, name='next_turn'),
    path('<int:game_id>/state/', views.game_state, name='game_state'),
    path('<int:game_id>/history/', views.game_history, name='game_history'),
    path('<int:game_id>/budget/', views.budget_data, name='budget_data'),
    path('<int:game_id>/demographics/', views.demographic_data, name='demographic_data'),
    path('<int:game_id>/production/', views.production_data, name='production_data'),
    # Расширенная модель
    path('enhanced/<int:game_id>/enhanced_state/', views.get_enhanced_game_state, name='get_enhanced_game_state'),
    path('enhanced/<int:game_id>/next_enhanced_turn/', views.next_enhanced_turn, name='next_enhanced_turn'),
    path('enhanced/<int:game_id>/history/', views.get_enhanced_game_history, name='get_enhanced_game_history'),
    # Добавляем маршруты для расширенной модели
    path('', include(router.urls)),
] 