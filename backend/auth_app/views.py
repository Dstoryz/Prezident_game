from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from .models import User, UserProfile
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserSerializer,
    ChangePasswordSerializer
)


class UserRegistrationView(APIView):
    """Регистрация нового пользователя"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Создаем токены
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Пользователь успешно зарегистрирован',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """Авторизация пользователя"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Создаем токены
            refresh = RefreshToken.for_user(user)
            
            # Логируем пользователя
            login(request, user)
            
            return Response({
                'message': 'Успешная авторизация',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """Выход пользователя"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            logout(request)
            return Response({
                'message': 'Успешный выход'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Ошибка при выходе'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Получение и обновление профиля пользователя"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user.profile


class UserDetailView(generics.RetrieveAPIView):
    """Получение информации о пользователе"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    """Смена пароля пользователя"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': 'Пароль успешно изменен'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """Получение статистики пользователя"""
    user = request.user
    
    stats = {
        'games_played': user.games_played,
        'best_score': user.best_score,
        'total_playtime': user.total_playtime,
        'achievements': user.profile.achievements,
        'favorite_strategy': user.profile.favorite_strategy,
        'preferred_difficulty': user.profile.preferred_difficulty,
    }
    
    return Response(stats, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_game_stats(request):
    """Обновление игровой статистики пользователя"""
    user = request.user
    
    # Получаем данные из запроса
    game_years = request.data.get('years_in_power', 0)
    playtime_minutes = request.data.get('playtime_minutes', 0)
    strategy = request.data.get('strategy', '')
    
    # Обновляем статистику
    user.games_played += 1
    user.total_playtime += playtime_minutes
    
    if game_years > user.best_score:
        user.best_score = game_years
    
    if strategy:
        user.profile.favorite_strategy = strategy
    
    user.save()
    user.profile.save()
    
    return Response({
        'message': 'Статистика обновлена',
        'stats': {
            'games_played': user.games_played,
            'best_score': user.best_score,
            'total_playtime': user.total_playtime,
        }
    }, status=status.HTTP_200_OK)


class GoogleLoginView(SocialLoginView):
    """Google OAuth2 аутентификация"""
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/auth/google/callback"
    client_class = OAuth2Client


@api_view(['GET'])
def google_oauth_callback(request):
    """Обработка callback от Google OAuth"""
    try:
        # Получаем код авторизации
        code = request.GET.get('code')
        if not code:
            return render(request, 'auth/google_callback.html', {
                'success': False,
                'error': 'Код авторизации не получен'
            })
        
        # Перенаправляем на фронтенд с кодом
        return render(request, 'auth/google_callback.html', {
            'success': True,
            'code': code,
            'redirect_url': 'http://localhost:3000/auth/google/callback'
        })
        
    except Exception as e:
        return render(request, 'auth/google_callback.html', {
            'success': False,
            'error': str(e)
        })


@api_view(['POST'])
def google_oauth_complete(request):
    """Завершение Google OAuth и отправка токенов"""
    try:
        # Получаем код авторизации
        code = request.data.get('code')
        if not code:
            return Response({
                'success': False,
                'error': 'Код авторизации не получен'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Здесь должна быть логика обмена кода на токены через Google API
        # Пока что создаем тестового пользователя
        user, created = User.objects.get_or_create(
            email='google_user@example.com',
            defaults={
                'username': 'google_user',
                'first_name': 'Google',
                'last_name': 'User',
            }
        )
        
        # Создаем токены
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            'user': UserSerializer(user).data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
