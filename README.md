# Workout Tracker

## Workout Management
1. Users will be able to create their workout plans. Workout plans should consist of multiple exercises, each with a set number of repetitions, sets, and weights. Users should be able to update and delete their workout plans. Additionally, users should be able to schedule workouts for specific dates and times.
2. Create Workout: Allow users to create workouts composed of multiple exercises.
3. Update Workout: Allow users to update workouts.
4. Delete Workout: Allow users to delete workouts.
5. Schedule Workouts: Allow users to schedule workouts for specific dates and times.
6. Update scheduled workout with actual reps, actual sets, actual weight and status.
7. List Workouts: List active or pending workouts sorted by date and time.
8. Generate Reports: Generate reports on past workouts and progress.

## API Endpoints
### Authorisation 
* POST /v1/auth/signup – Create account
* POST /v1/auth/login – Login and get JWT
* POST /v1/auth/logout – Log out

### Exercises
* GET /v1/exercises – List all exercises
* GET /v1/exercises/{exercise_id} – Get a single exercise

### Workout Plans and Workout Plan Exercises
* POST /v1/workout-plans – Create a workout plan with linked workout plan exercises
* GET /v1/workout-plans – List user's workout plans with linked workout plan exercises
* GET /v1/workout-plans/{workout_plan_id} – View a specific workout plan with linked workout plan exercises
* PATCH /v1/workout-plans/{workout_plan_id} – Update a workout plan - update linked workout plan exercises
* DELETE /v1/workout-plan/{workout_plan_id} – Delete a workout plan - cascade delete all linked workout plan exercises and workout sessions

### Workout Sessions
* POST /v1/workout-session/{workout_plan_id} – Create a workout session (linking to a plan), create a session exercise entry for every workout plan exercise
* GET /v1/workout-sessions – List workout sessions 
* GET /v1/workout-sessions/{workout_plan_id}/{workout_session_id} – Get a specific scheduled workout session 
* PATCH /v1/workout-sessions/{workout_plan_id}/{workout_session_id} – Update status of user workout session  
* DELETE /v1/workout-sessions/{workout_plan_id}/{workout_session_id} – cascade delete a workout session and all session exercises.

### Workout Reports
* GET /v1/reports/{workout_plan_id} - Get workout plan exericses, sessions and session exercises report for a workout plan

# Setting up Workout Tracker
## 🏋️ Workout Tracker Flask App Setup Guide

This guide will help you set up the Flask-based Workout Tracker app locally for development and testing.

---

## 📦 Prerequisites

Make sure you have the following installed:

- Python 3.8+ 
- PostgreSQL
- pip
- virtualenv

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/workout-tracker.git
cd workout-tracker
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create the .env file
```bash
# Flask
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1

# Database (PostgreSQL)
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=workout_tracker

# SQLAlchemy
SQLALCHEMY_DATABASE_URI=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}
SECRET_KEY=change_this_secret
SQLALCHEMY_TEST_URI=postgresql://postgres:postgres@localhost:${DB_PORT}/workout_tracker_test
SECRET_KEY_TEST=another_test_secret
SQLALCHEMY_TRACK_MODIFICATIONS=False
```
⚠️ Replace your_postgres_user and your_postgres_password with your actual PostgreSQL credentials.

### 5. Create the databases
Make sure PostgreSQL is running, then create the required databases:
```bash
createdb workout_tracker
createdb workout_tracker_test
```

Open `psql` as the `postgres` superuser:
```bash
psql -U postgres
CREATE USER your_username WITH PASSWORD 'your_password';
CREATE DATABASE workout_tracker OWNER your_username;
CREATE DATABASE workout_tracker_test OWNER your_username;
GRANT ALL PRIVILEGES ON DATABASE workout_tracker TO your_username;
GRANT ALL PRIVILEGES ON DATABASE workout_tracker_test TO your_username;
```

### 6. Run database migrations
```bash
flask db upgrade
```

### 7. Run the Flask app
```bash
flask run
```

### 8. To Run tests
```bash
pytest
```







