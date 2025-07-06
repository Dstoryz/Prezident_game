from django.contrib import admin
from .models import User, UserProfile, UserSession

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff', 'date_joined', 'games_played', 'best_score')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    ordering = ('-date_joined',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_difficulty', 'email_notifications', 'game_notifications')
    search_fields = ('user__email', 'user__username')

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'session_key', 'ip_address', 'created_at', 'last_activity', 'is_active')
    search_fields = ('user__email', 'session_key')
