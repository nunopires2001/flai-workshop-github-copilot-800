from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Team, Workout, Activity, Leaderboard
from .serializers import (
    UserSerializer, TeamSerializer, WorkoutSerializer,
    ActivitySerializer, LeaderboardSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users (superheroes)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get users filtered by team"""
        team = request.query_params.get('team', None)
        if team:
            users = User.objects.filter(team=team)
            serializer = self.get_serializer(users, many=True)
            return Response(serializer.data)
        return Response({"error": "Team parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user_id=str(user.id))
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a specific team"""
        team = self.get_object()
        users = User.objects.filter(team_id=str(team.id))
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def leaderboard(self, request, pk=None):
        """Get leaderboard entries for a specific team"""
        team = self.get_object()
        entries = Leaderboard.objects.filter(team_id=str(team.id))
        serializer = LeaderboardSerializer(entries, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing workout types
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts filtered by difficulty"""
        difficulty = request.query_params.get('difficulty', None)
        if difficulty:
            workouts = Workout.objects.filter(difficulty=difficulty)
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        return Response({"error": "Difficulty parameter is required"}, status=status.HTTP_400_BAD_REQUEST)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing activities
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get activities filtered by activity type"""
        activity_type = request.query_params.get('type', None)
        if activity_type:
            activities = Activity.objects.filter(activity_type=activity_type)
            serializer = self.get_serializer(activities, many=True)
            return Response(serializer.data)
        return Response({"error": "Type parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get most recent activities"""
        limit = int(request.query_params.get('limit', 10))
        activities = Activity.objects.all()[:limit]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing leaderboard entries
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        """Get top N entries from leaderboard"""
        limit = int(request.query_params.get('limit', 10))
        entries = Leaderboard.objects.all()[:limit]
        serializer = self.get_serializer(entries, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get leaderboard entries for a specific team"""
        team = request.query_params.get('team', None)
        if team:
            entries = Leaderboard.objects.filter(team=team)
            serializer = self.get_serializer(entries, many=True)
            return Response(serializer.data)
        return Response({"error": "Team parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
