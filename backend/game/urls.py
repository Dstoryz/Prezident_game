from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_game, name='start_game'),
    path('<int:game_id>/next-turn/', views.next_turn, name='next_turn'),
    path('<int:game_id>/state/', views.game_state, name='game_state'),
    path('<int:game_id>/history/', views.game_history, name='game_history'),
] 