from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start_game, name='start_game'),
    path('<int:game_id>/next-turn/', views.next_turn, name='next_turn'),
    path('<int:game_id>/state/', views.game_state, name='game_state'),
    path('<int:game_id>/history/', views.game_history, name='game_history'),
    path('<int:game_id>/budget/', views.budget_data, name='budget_data'),
    path('<int:game_id>/demographics/', views.demographic_data, name='demographic_data'),
    path('<int:game_id>/production/', views.production_data, name='production_data'),
] 