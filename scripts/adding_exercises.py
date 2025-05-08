import os
import sys

# Add the root directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app, db
from app.models import Exercise

app = create_app()

# Add exercises inside the Flask app context
with app.app_context():
    exercises_to_add = [
        {
            "name": "Push-up",
            "category": "Bodyweight",
            "description": "A push-up exercise",
            "muscle_group": "Triceps",
        },
        {
            "name": "Squat",
            "category": "Bodyweight",
            "description": "A squat exercise",
            "muscle_group": "Glutes",
        },
        {
            "name": "Bench Press",
            "category": "Strength",
            "description": "A bench press exercise",
            "muscle_group": "Pectoralis major",
        },
        {
            "name": "Deadlift",
            "category": "Strength",
            "description": "A barbell deadlift",
            "muscle_group": "Hamstrings",
        },
        {
            "name": "Pull-up",
            "category": "Bodyweight",
            "description": "Upper body pulling movement",
            "muscle_group": "Latissimus dorsi",
        },
        {
            "name": "Overhead Press",
            "category": "Strength",
            "description": "Shoulder pressing movement",
            "muscle_group": "Deltoids",
        },
        {
            "name": "Bicep Curl",
            "category": "Strength",
            "description": "Isolated bicep exercise",
            "muscle_group": "Biceps",
        },
        {
            "name": "Lunge",
            "category": "Bodyweight",
            "description": "Lower body lunge exercise",
            "muscle_group": "Quadriceps",
        },
        {
            "name": "Plank",
            "category": "Core",
            "description": "Core stabilization exercise",
            "muscle_group": "Abdominals",
        },
        {
            "name": "Russian Twist",
            "category": "Core",
            "description": "Rotational core exercise",
            "muscle_group": "Obliques",
        },
        {
            "name": "Lat Pulldown",
            "category": "Strength",
            "description": "Lat-focused pulldown exercise",
            "muscle_group": "Latissimus dorsi",
        },
        {
            "name": "Leg Press",
            "category": "Strength",
            "description": "Leg pressing machine",
            "muscle_group": "Quadriceps",
        },
        {
            "name": "Calf Raise",
            "category": "Strength",
            "description": "Exercise for the calves",
            "muscle_group": "Gastrocnemius",
        },
        {
            "name": "Tricep Dip",
            "category": "Bodyweight",
            "description": "Triceps dip using parallel bars",
            "muscle_group": "Triceps",
        },
        {
            "name": "Mountain Climbers",
            "category": "Cardio",
            "description": "Full-body cardio move",
            "muscle_group": "Core",
        },
        {
            "name": "Burpees",
            "category": "Cardio",
            "description": "High-intensity full-body movement",
            "muscle_group": "Full body",
        },
        {
            "name": "Hip Thrust",
            "category": "Strength",
            "description": "Hip extension for glutes",
            "muscle_group": "Glutes",
        },
        {
            "name": "Cable Row",
            "category": "Strength",
            "description": "Seated cable row exercise",
            "muscle_group": "Back",
        },
        {
            "name": "Face Pull",
            "category": "Strength",
            "description": "Shoulder and upper back pull",
            "muscle_group": "Rear deltoids",
        },
        {
            "name": "Farmer's Walk",
            "category": "Functional",
            "description": "Grip and core strength carry",
            "muscle_group": "Forearms",
        },
    ]

    for exercise_data in exercises_to_add:
        exercise = Exercise(
            name=exercise_data["name"],
            category=exercise_data["category"],
            description=exercise_data["description"],
            muscle_group=exercise_data["muscle_group"],
        )
        db.session.add(exercise)

    db.session.commit()

    print(f"Added {len(exercises_to_add)} exercises to the database.")
