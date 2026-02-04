from rest_framework import serializers
from .models import User, Team, Workout, Activity, Leaderboard
from bson import ObjectId


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'alias', 'superpower', 'team', 'team_id', 
                  'created_at', 'fitness_level', 'total_points']
        read_only_fields = ['created_at']


class TeamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_at', 'members']
        read_only_fields = ['created_at']


class WorkoutSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'duration_minutes', 'difficulty', 
                  'calories_burned', 'created_at']
        read_only_fields = ['created_at']


class ActivitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activity
        fields = ['id', 'user_id', 'workout_id', 'activity_type', 'duration_minutes', 
                  'calories_burned', 'distance_km', 'date', 'notes', 'points_earned']


class LeaderboardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'user_id', 'user_name', 'team', 'team_id', 
                  'total_points', 'rank', 'last_updated']
        read_only_fields = ['last_updated']
