from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        self.stdout.write(self.style.SUCCESS('Connected to MongoDB'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email field for users collection
        db.users.create_index([("email", 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Created unique index on email field'))

        # Marvel Superheroes Team Data
        marvel_heroes = [
            {"name": "Iron Man", "email": "tony.stark@marvel.com", "alias": "Tony Stark", "superpower": "Genius intellect and powered armor"},
            {"name": "Captain America", "email": "steve.rogers@marvel.com", "alias": "Steve Rogers", "superpower": "Super soldier serum"},
            {"name": "Thor", "email": "thor.odinson@marvel.com", "alias": "Thor Odinson", "superpower": "God of Thunder"},
            {"name": "Hulk", "email": "bruce.banner@marvel.com", "alias": "Bruce Banner", "superpower": "Superhuman strength"},
            {"name": "Black Widow", "email": "natasha.romanoff@marvel.com", "alias": "Natasha Romanoff", "superpower": "Master spy and assassin"},
            {"name": "Spider-Man", "email": "peter.parker@marvel.com", "alias": "Peter Parker", "superpower": "Spider abilities"},
            {"name": "Doctor Strange", "email": "stephen.strange@marvel.com", "alias": "Stephen Strange", "superpower": "Master of mystic arts"},
            {"name": "Black Panther", "email": "tchalla@marvel.com", "alias": "T'Challa", "superpower": "Enhanced abilities and vibranium suit"},
        ]

        # DC Superheroes Team Data
        dc_heroes = [
            {"name": "Superman", "email": "clark.kent@dc.com", "alias": "Clark Kent", "superpower": "Flight, super strength, heat vision"},
            {"name": "Batman", "email": "bruce.wayne@dc.com", "alias": "Bruce Wayne", "superpower": "Detective skills and high-tech gadgets"},
            {"name": "Wonder Woman", "email": "diana.prince@dc.com", "alias": "Diana Prince", "superpower": "Amazon warrior abilities"},
            {"name": "Flash", "email": "barry.allen@dc.com", "alias": "Barry Allen", "superpower": "Super speed"},
            {"name": "Aquaman", "email": "arthur.curry@dc.com", "alias": "Arthur Curry", "superpower": "Underwater abilities and strength"},
            {"name": "Green Lantern", "email": "hal.jordan@dc.com", "alias": "Hal Jordan", "superpower": "Power ring wielder"},
            {"name": "Cyborg", "email": "victor.stone@dc.com", "alias": "Victor Stone", "superpower": "Cybernetic enhancements"},
            {"name": "Shazam", "email": "billy.batson@dc.com", "alias": "Billy Batson", "superpower": "Magic-based powers"},
        ]

        # Insert Teams
        marvel_team = {
            "name": "Team Marvel",
            "description": "Earth's Mightiest Heroes",
            "created_at": datetime.now(),
            "members": []
        }
        dc_team = {
            "name": "Team DC",
            "description": "Justice League Unlimited",
            "created_at": datetime.now(),
            "members": []
        }

        marvel_team_result = db.teams.insert_one(marvel_team)
        dc_team_result = db.teams.insert_one(dc_team)
        marvel_team_id = marvel_team_result.inserted_id
        dc_team_id = dc_team_result.inserted_id

        self.stdout.write(self.style.SUCCESS(f'Created Team Marvel with ID: {marvel_team_id}'))
        self.stdout.write(self.style.SUCCESS(f'Created Team DC with ID: {dc_team_id}'))

        # Insert Users and track IDs
        marvel_user_ids = []
        dc_user_ids = []

        for hero in marvel_heroes:
            user_doc = {
                "name": hero["name"],
                "email": hero["email"],
                "alias": hero["alias"],
                "superpower": hero["superpower"],
                "team": "Team Marvel",
                "team_id": marvel_team_id,
                "created_at": datetime.now(),
                "fitness_level": random.choice(["beginner", "intermediate", "advanced", "expert"]),
                "total_points": random.randint(100, 1000)
            }
            result = db.users.insert_one(user_doc)
            marvel_user_ids.append(result.inserted_id)

        for hero in dc_heroes:
            user_doc = {
                "name": hero["name"],
                "email": hero["email"],
                "alias": hero["alias"],
                "superpower": hero["superpower"],
                "team": "Team DC",
                "team_id": dc_team_id,
                "created_at": datetime.now(),
                "fitness_level": random.choice(["beginner", "intermediate", "advanced", "expert"]),
                "total_points": random.randint(100, 1000)
            }
            result = db.users.insert_one(user_doc)
            dc_user_ids.append(result.inserted_id)

        # Update teams with member IDs
        db.teams.update_one(
            {"_id": marvel_team_id},
            {"$set": {"members": marvel_user_ids}}
        )
        db.teams.update_one(
            {"_id": dc_team_id},
            {"$set": {"members": dc_user_ids}}
        )

        self.stdout.write(self.style.SUCCESS(f'Created {len(marvel_heroes)} Marvel heroes'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(dc_heroes)} DC heroes'))

        # Insert Workouts
        workout_types = [
            {"name": "Cardio Blast", "description": "High-intensity cardio workout", "duration_minutes": 30, "difficulty": "intermediate", "calories_burned": 300},
            {"name": "Strength Training", "description": "Full body strength workout", "duration_minutes": 45, "difficulty": "advanced", "calories_burned": 250},
            {"name": "Yoga Flow", "description": "Relaxing yoga session", "duration_minutes": 60, "difficulty": "beginner", "calories_burned": 150},
            {"name": "HIIT Power", "description": "High-intensity interval training", "duration_minutes": 20, "difficulty": "expert", "calories_burned": 400},
            {"name": "Core Crusher", "description": "Intense core workout", "duration_minutes": 15, "difficulty": "intermediate", "calories_burned": 100},
            {"name": "Hero Sprint", "description": "Speed and agility training", "duration_minutes": 25, "difficulty": "advanced", "calories_burned": 280},
            {"name": "Power Lifting", "description": "Heavy weightlifting session", "duration_minutes": 50, "difficulty": "expert", "calories_burned": 350},
            {"name": "Flexibility Focus", "description": "Stretching and mobility work", "duration_minutes": 30, "difficulty": "beginner", "calories_burned": 80},
        ]

        workout_ids = []
        for workout in workout_types:
            workout["created_at"] = datetime.now()
            result = db.workouts.insert_one(workout)
            workout_ids.append(result.inserted_id)

        self.stdout.write(self.style.SUCCESS(f'Created {len(workout_types)} workout types'))

        # Insert Activities
        activity_types = ["running", "cycling", "swimming", "weightlifting", "yoga", "boxing", "climbing", "crossfit"]
        all_user_ids = marvel_user_ids + dc_user_ids

        activities_created = 0
        for _ in range(50):  # Create 50 random activities
            user_id = random.choice(all_user_ids)
            workout_id = random.choice(workout_ids)
            activity_type = random.choice(activity_types)
            
            days_ago = random.randint(0, 30)
            activity_date = datetime.now() - timedelta(days=days_ago)
            
            activity_doc = {
                "user_id": user_id,
                "workout_id": workout_id,
                "activity_type": activity_type,
                "duration_minutes": random.randint(15, 90),
                "calories_burned": random.randint(100, 500),
                "distance_km": round(random.uniform(1.0, 15.0), 2) if activity_type in ["running", "cycling", "swimming"] else 0,
                "date": activity_date,
                "notes": f"Great {activity_type} session!",
                "points_earned": random.randint(10, 50)
            }
            db.activities.insert_one(activity_doc)
            activities_created += 1

        self.stdout.write(self.style.SUCCESS(f'Created {activities_created} activities'))

        # Create Leaderboard entries
        leaderboard_entries = []
        
        # Marvel team leaderboard
        for user_id in marvel_user_ids:
            user = db.users.find_one({"_id": user_id})
            total_points = user.get("total_points", 0)
            
            # Add points from activities
            user_activities = db.activities.find({"user_id": user_id})
            activity_points = sum([act.get("points_earned", 0) for act in user_activities])
            total_points += activity_points
            
            leaderboard_entries.append({
                "user_id": user_id,
                "user_name": user["name"],
                "team": "Team Marvel",
                "team_id": marvel_team_id,
                "total_points": total_points,
                "rank": 0,  # Will be calculated after sorting
                "last_updated": datetime.now()
            })

        # DC team leaderboard
        for user_id in dc_user_ids:
            user = db.users.find_one({"_id": user_id})
            total_points = user.get("total_points", 0)
            
            # Add points from activities
            user_activities = db.activities.find({"user_id": user_id})
            activity_points = sum([act.get("points_earned", 0) for act in user_activities])
            total_points += activity_points
            
            leaderboard_entries.append({
                "user_id": user_id,
                "user_name": user["name"],
                "team": "Team DC",
                "team_id": dc_team_id,
                "total_points": total_points,
                "rank": 0,  # Will be calculated after sorting
                "last_updated": datetime.now()
            })

        # Sort by points and assign ranks
        leaderboard_entries.sort(key=lambda x: x["total_points"], reverse=True)
        for idx, entry in enumerate(leaderboard_entries, start=1):
            entry["rank"] = idx

        # Insert leaderboard entries
        if leaderboard_entries:
            db.leaderboard.insert_many(leaderboard_entries)
            self.stdout.write(self.style.SUCCESS(f'Created {len(leaderboard_entries)} leaderboard entries'))

        # Display summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Users: {db.users.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Teams: {db.teams.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Activities: {db.activities.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts: {db.workouts.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard Entries: {db.leaderboard.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS('\nDatabase population completed successfully!'))

        client.close()
