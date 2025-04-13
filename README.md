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
* GET /v1/workout-sessions/{workout_plan_user_session_id} – Get a specific scheduled workout session 
* PATCH /v1/workout-sessions/{workout_plan_user_session_id}/{workout_plan_exercise_id} – Update status of user workout session  
* PATCH /v1/workout-session-exercise/{session_exercise_id} - Update actual_sets, actual_weight, actual_reps, notes in session exercises. 
* DELETE /v1/workout-sessions/{workout_plan_user_session_id} – cascade delete a workout session and all session exercises.

### Workout Reports
* GET /v1/reports/workout-sessions - List workout sessions with session exercises
* GET /v1/reports/workout-sessions/{session_exercise_id} – Report on user’s progress on a specific exercise

