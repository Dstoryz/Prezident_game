from django.urls import path
from . import views

app_name = 'auth_app'

urlpatterns = [
    # Аутентификация
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    
    # Google OAuth
    path('google/', views.GoogleLoginView.as_view(), name='google_login'),
    path('google/callback/', views.google_oauth_callback, name='google_callback'),
    path('google/complete/', views.google_oauth_complete, name='google_complete'),
    
    # Профиль пользователя
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('user/', views.UserDetailView.as_view(), name='user-detail'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
    # Статистика
    path('stats/', views.user_stats, name='user-stats'),
    path('update-stats/', views.update_game_stats, name='update-game-stats'),
] 