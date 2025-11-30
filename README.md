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
* POST /api/auth/signup – Create account
* POST /api/auth/login – Login and get JWT
* POST /api/auth/logout – Log out

### Exercises
* GET /api/exercises – List all exercises
* GET /api/exercises/{exercise_id} – Get a single exercise

### Workout Plans and Workout Plan Exercises
* POST /api/workout-plans – Create a workout plan with linked workout plan exercises
* GET /api/workout-plans – List user's workout plans with linked workout plan exercises
* GET /api/workout-plans/{workout_plan_id} – View a specific workout plan with linked workout plan exercises
* PATCH /api/workout-plans/{workout_plan_id} – Update a workout plan - update linked workout plan exercises
* DELETE /api/workout-plan/{workout_plan_id} – Delete a workout plan - cascade delete all linked workout plan exercises and workout sessions

### Workout Sessions
* POST /api/workout-session/{workout_plan_id} – Create a workout session (linking to a plan), create a session exercise entry for every workout plan exercise
* GET /api/workout-sessions – List workout sessions 
* GET /api/workout-sessions/{workout_plan_id}/{workout_session_id} – Get a specific scheduled workout session 
* PATCH /api/workout-sessions/{workout_plan_id}/{workout_session_id} – Update status of user workout session  
* DELETE /api/workout-sessions/{workout_plan_id}/{workout_session_id} – cascade delete a workout session and all session exercises.

### Workout Reports
* GET /api/reports/{workout_plan_id} - Get workout plan exericses, sessions and session exercises report for a workout plan


# Setting up Workout Tracker
## 🏋️ Workout Tracker Flask App Setup Guide

This guide will help you set up the Flask-based Workout Tracker app locally for development and testing.

---

## 📦 Prerequisites

Make sure you have the following installed:

- Docker (20.10+)
- Docker Compose (2.0+) 

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/workout-tracker.git
cd workout-tracker
```

### 4. Copy the .env file
```bash
cp .example-env .env 
```

### 5. Make scripts executable
```bash
bashchmod +x setup.sh entrypoint.sh init-db.sh
```

### 6. Run Setup Script
```bash
./setup.sh
```

### 7. To Open App
Backend API only:
```bash
http://localhost:5000
```
Frontend:
```bash
http://localhost:3000
```

### 8. To test on Postman
1. Import the collection and environment json files from the postman folder in the app's main directory, into Postman.
2. Run the app
3. Then test the different requests in the collection. 
