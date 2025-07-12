from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        if not extra_fields.get('username'):
            # Генерируем username на основе email и количества пользователей
            base_username = email.split('@')[0]
            extra_fields['username'] = f"{base_username}{User.objects.count() + 1}"
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Расширенная модель пользователя"""
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Статистика игрока
    games_played = models.IntegerField(default=0)
    best_score = models.IntegerField(default=0)  # Лучший результат (годы у власти)
    total_playtime = models.IntegerField(default=0)  # Общее время игры в минутах
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserProfile(models.Model):
    """Дополнительный профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Игровые настройки
    preferred_difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Легкий'),
            ('medium', 'Средний'),
            ('hard', 'Сложный'),
        ],
        default='medium'
    )
    
    # Настройки уведомлений
    email_notifications = models.BooleanField(default=True)
    game_notifications = models.BooleanField(default=True)
    
    # Статистика
    favorite_strategy = models.CharField(max_length=100, blank=True)
    achievements = models.JSONField(default=list)
    
    def __str__(self):
        return f"Профиль {self.user.email}"
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class UserSession(models.Model):
    """Сессии пользователей для отслеживания активности"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Сессия {self.user.email} - {self.created_at}"
    
    class Meta:
        verbose_name = 'Сессия пользователя'
        verbose_name_plural = 'Сессии пользователей'
