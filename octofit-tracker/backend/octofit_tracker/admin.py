from django.contrib import admin
from .models import User, Team, Workout, Activity, Leaderboard


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'team', 'fitness_level', 'total_points', 'created_at')
    list_filter = ('team', 'fitness_level')
    search_fields = ('name', 'email', 'alias')
    ordering = ('-total_points',)
    readonly_fields = ('created_at',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'duration_minutes', 'calories_burned', 'created_at')
    list_filter = ('difficulty',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_type', 'user_id', 'duration_minutes', 'calories_burned', 
                    'points_earned', 'date')
    list_filter = ('activity_type', 'date')
    search_fields = ('activity_type', 'notes')
    ordering = ('-date',)
    date_hierarchy = 'date'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('rank', 'user_name', 'team', 'total_points', 'last_updated')
    list_filter = ('team',)
    search_fields = ('user_name', 'team')
    ordering = ('rank',)
    readonly_fields = ('last_updated',)
