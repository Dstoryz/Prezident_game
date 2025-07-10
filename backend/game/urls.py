from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.create_new_game, name='create_new_game'),
    path('status/<int:game_id>/', views.game_status, name='game_status'),
]
