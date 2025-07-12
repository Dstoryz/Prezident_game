from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.create_new_game, name='create_new_game'),
    path('status/<int:game_id>/', views.game_status, name='game_status'),
    path('<int:game_id>/state/', views.get_game_state, name='get_game_state'),
    path('<int:game_id>/next-turn/', views.next_turn, name='next_turn'),
    path('<int:game_id>/history/', views.get_game_history, name='get_game_history'),
    # Для расширенной модели:
    path('enhanced/<int:game_id>/enhanced_state/', views.enhanced_game_state, name='enhanced_game_state'),
    path('enhanced/<int:game_id>/next_enhanced_turn/', views.next_turn, name='next_enhanced_turn'),
]
