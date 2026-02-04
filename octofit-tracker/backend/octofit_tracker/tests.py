from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Workout, Activity, Leaderboard
from bson import ObjectId
from datetime import datetime


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user_data = {
            'name': 'Test Hero',
            'email': 'test@marvel.com',
            'alias': 'Tester',
            'superpower': 'Testing abilities',
            'team': 'Team Marvel',
            'fitness_level': 'advanced',
            'total_points': 100
        }
    
    def test_user_creation(self):
        """Test creating a user"""
        user = User.objects.create(**self.user_data)
        self.assertEqual(user.name, 'Test Hero')
        self.assertEqual(user.email, 'test@marvel.com')
        self.assertEqual(user.total_points, 100)
    
    def test_user_str_method(self):
        """Test user string representation"""
        user = User.objects.create(**self.user_data)
        self.assertEqual(str(user), 'Test Hero')


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team_data = {
            'name': 'Test Team',
            'description': 'A team for testing',
            'members': []
        }
    
    def test_team_creation(self):
        """Test creating a team"""
        team = Team.objects.create(**self.team_data)
        self.assertEqual(team.name, 'Test Team')
        self.assertEqual(team.description, 'A team for testing')
    
    def test_team_str_method(self):
        """Test team string representation"""
        team = Team.objects.create(**self.team_data)
        self.assertEqual(str(team), 'Test Team')


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        self.workout_data = {
            'name': 'Test Workout',
            'description': 'A test workout',
            'duration_minutes': 30,
            'difficulty': 'intermediate',
            'calories_burned': 250
        }
    
    def test_workout_creation(self):
        """Test creating a workout"""
        workout = Workout.objects.create(**self.workout_data)
        self.assertEqual(workout.name, 'Test Workout')
        self.assertEqual(workout.duration_minutes, 30)
        self.assertEqual(workout.difficulty, 'intermediate')
    
    def test_workout_str_method(self):
        """Test workout string representation"""
        workout = Workout.objects.create(**self.workout_data)
        self.assertEqual(str(workout), 'Test Workout')


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            name='API Test Hero',
            email='apitest@marvel.com',
            team='Team Marvel',
            total_points=200
        )
        self.workout = Workout.objects.create(
            name='API Test Workout',
            description='Test',
            duration_minutes=20,
            difficulty='beginner',
            calories_burned=150
        )
    
    def test_get_activities_list(self):
        """Test getting list of activities"""
        url = reverse('activity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_activity(self):
        """Test creating an activity"""
        url = reverse('activity-list')
        activity_data = {
            'user_id': str(self.user._id),
            'workout_id': str(self.workout._id),
            'activity_type': 'running',
            'duration_minutes': 30,
            'calories_burned': 200,
            'distance_km': 5.0,
            'date': datetime.now().isoformat(),
            'points_earned': 25
        }
        response = self.client.post(url, activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LeaderboardAPITest(APITestCase):
    """Test cases for Leaderboard API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        # Create test users
        self.user1 = User.objects.create(
            name='Hero One',
            email='hero1@marvel.com',
            team='Team Marvel',
            total_points=500
        )
        self.user2 = User.objects.create(
            name='Hero Two',
            email='hero2@dc.com',
            team='Team DC',
            total_points=300
        )
    
    def test_get_leaderboard(self):
        """Test getting leaderboard"""
        url = reverse('leaderboard-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_top_leaderboard(self):
        """Test getting top N entries from leaderboard"""
        url = reverse('leaderboard-top')
        response = self.client.get(url, {'limit': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.team = Team.objects.create(
            name='Test API Team',
            description='Testing team'
        )
    
    def test_get_users_list(self):
        """Test getting list of users"""
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        """Test creating a user"""
        url = reverse('user-list')
        user_data = {
            'name': 'New Hero',
            'email': 'newhero@marvel.com',
            'alias': 'New',
            'superpower': 'New powers',
            'team': 'Test API Team',
            'team_id': str(self.team._id),
            'fitness_level': 'beginner',
            'total_points': 0
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Hero')


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_get_teams_list(self):
        """Test getting list of teams"""
        url = reverse('team-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_team(self):
        """Test creating a team"""
        url = reverse('team-list')
        team_data = {
            'name': 'API Test Team',
            'description': 'Created via API test',
            'members': []
        }
        response = self.client.post(url, team_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'API Test Team')
