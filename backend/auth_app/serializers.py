from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile
from dj_rest_auth.registration.serializers import RegisterSerializer


class UserRegistrationSerializer(RegisterSerializer):
    """
    Кастомный сериализатор регистрации для dj-rest-auth с созданием профиля пользователя
    """
    username = serializers.CharField(required=False, allow_blank=True)
    
    def save(self, request):
        user = super().save(request)
        from .models import UserProfile
        UserProfile.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для авторизации пользователя"""
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Неверный email или пароль')
            if not user.is_active:
                raise serializers.ValidationError('Аккаунт заблокирован')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Необходимо указать email и пароль')
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя"""
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)
    games_played = serializers.IntegerField(source='user.games_played', read_only=True)
    best_score = serializers.IntegerField(source='user.best_score', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'date_joined',
            'preferred_difficulty', 'email_notifications', 'game_notifications',
            'favorite_strategy', 'achievements', 'games_played', 'best_score'
        ]
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        
        # Обновляем данные пользователя
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        
        # Обновляем профиль
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения пользователя"""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 
            'date_joined', 'games_played', 'best_score', 'profile'
        ]
        read_only_fields = ['id', 'date_joined', 'games_played', 'best_score']


class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Новые пароли не совпадают")
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Неверный текущий пароль")
        return value 