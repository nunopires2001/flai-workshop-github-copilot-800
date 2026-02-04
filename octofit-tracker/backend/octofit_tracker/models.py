from djongo import models
from bson import ObjectId as BsonObjectId


class User(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    alias = models.CharField(max_length=100, blank=True)
    superpower = models.TextField(blank=True)
    team = models.CharField(max_length=100, blank=True)
    team_id = models.CharField(max_length=24, null=True, blank=True)
    created_at = models.DateTimeField()
    fitness_level = models.CharField(max_length=50, blank=True)
    total_points = models.IntegerField(default=0)

    class Meta:
        db_table = 'users'
        ordering = ['-total_points']
        managed = False

    def __str__(self):
        return self.name


class Team(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField()
    members = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'teams'
        ordering = ['name']
        managed = False

    def __str__(self):
        return self.name


class Workout(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration_minutes = models.IntegerField()
    difficulty = models.CharField(max_length=50)
    calories_burned = models.IntegerField()
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'workouts'
        ordering = ['name']
        managed = False

    def __str__(self):
        return self.name


class Activity(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    user_id = models.CharField(max_length=24)
    workout_id = models.CharField(max_length=24)
    activity_type = models.CharField(max_length=50)
    duration_minutes = models.IntegerField()
    calories_burned = models.IntegerField()
    distance_km = models.FloatField(default=0.0)
    date = models.DateTimeField()
    notes = models.TextField(blank=True)
    points_earned = models.IntegerField(default=0)

    class Meta:
        db_table = 'activities'
        ordering = ['-date']
        managed = False

    def __str__(self):
        return f"{self.activity_type} - {self.date}"


class Leaderboard(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    user_id = models.CharField(max_length=24)
    user_name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    team_id = models.CharField(max_length=24)
    total_points = models.IntegerField(default=0)
    rank = models.IntegerField()
    last_updated = models.DateTimeField()

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']
        managed = False

    def __str__(self):
        return f"{self.rank}. {self.user_name} - {self.total_points} points"
