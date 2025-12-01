// frontend/src/components/WorkoutSessionForm.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const WorkoutSessionForm = () => {
  const [workoutPlans, setWorkoutPlans] = useState([]);
  const [selectedPlanId, setSelectedPlanId] = useState('');
  const [planExercises, setPlanExercises] = useState([]);
  const [selectedExercises, setSelectedExercises] = useState([]);
  const [sessionTimes, setSessionTimes] = useState({
    scheduled_date: '',
    scheduled_time: '',
    started_date: '',
    started_time: '',
    completed_date: '',
    completed_time: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isEditMode, setIsEditMode] = useState(false);

  const { planId, sessionId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  // Utility: combine date + time into DB-friendly string
  const combineDateTime = (dateStr, timeStr) => {
    if (!dateStr) return null;
    const timePart = timeStr || "00:00";
    return `${dateStr} ${timePart}:00`; // YYYY-MM-DD HH:MM:SS
  };

  useEffect(() => {
    fetchWorkoutPlans();
    if (planId && sessionId) {
      setIsEditMode(true);
      fetchSession();
    }
  }, [planId, sessionId]);

  useEffect(() => {
    if (selectedPlanId) {
      fetchPlanExercises(selectedPlanId);
    }
  }, [selectedPlanId]);

  const fetchWorkoutPlans = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/workout-plans', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        setWorkoutPlans(Array.isArray(data) ? data : []);
      }
    } catch (err) {
      console.error('Error fetching workout plans:', err);
    }
  };

  const fetchPlanExercises = async (planIdToFetch) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:5000/api/workout-plans/${planIdToFetch}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        if (data && data.length > 0 && data[0].workout) {
          setPlanExercises(data[0].workout.exercises || []);
          if (!isEditMode && data[0].workout.exercises) {
            setSelectedExercises(
              data[0].workout.exercises.map(ex => ({
                workout_plan_exercise_id: ex.id,
                name: ex.name,
                actual_sets: ex.target_sets || 3,
                actual_reps: ex.target_reps || 10,
                actual_weight: ex.target_weight || 0,
                notes: ''
              }))
            );
          }
        }
      }
    } catch (err) {
      console.error('Error fetching plan exercises:', err);
    }
  };

  const fetchSession = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(
        `http://localhost:5000/api/workout-sessions/${planId}/${sessionId}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        }
      );

      if (response.ok) {
        const data = await response.json();
        if (data && data.length > 0 && data[0].workout_session) {
          const session = data[0].workout_session;
          setSelectedPlanId(session.workout_plan_id.toString());

          const parseDateTime = (dt) => {
            if (!dt) return ['', ''];
            const [datePart, timePart] = dt.split('T');
            return [datePart, timePart ? timePart.substring(0,5) : ''];
          };

          const [scheduled_date, scheduled_time] = parseDateTime(session.scheduled_at);
          const [started_date, started_time] = parseDateTime(session.started_at);
          const [completed_date, completed_time] = parseDateTime(session.completed_at);

          setSessionTimes({
            scheduled_date,
            scheduled_time,
            started_date,
            started_time,
            completed_date,
            completed_time
          });

          if (session.session_exercises) {
            setSelectedExercises(
              session.session_exercises.map(ex => ({
                workout_plan_exercise_id: ex.id,
                actual_sets: ex.actual_sets,
                actual_reps: ex.actual_reps,
                actual_weight: ex.actual_weight,
                notes: ex.notes || ''
              }))
            );
          }
        }
      }
    } catch (err) {
      setError('Failed to load session');
    }
  };

  const addExercise = (exerciseId) => {
    const exercise = planExercises.find(ex => ex.id === parseInt(exerciseId));
    if (exercise && !selectedExercises.find(ex => ex.workout_plan_exercise_id === exercise.id)) {
      setSelectedExercises([...selectedExercises, {
        workout_plan_exercise_id: exercise.id,
        name: exercise.name,
        actual_sets: exercise.target_sets || 3,
        actual_reps: exercise.target_reps || 10,
        actual_weight: exercise.target_weight || 0,
        notes: ''
      }]);
    }
  };

  const removeExercise = (exerciseId) => {
    setSelectedExercises(selectedExercises.filter(
      ex => ex.workout_plan_exercise_id !== exerciseId
    ));
  };

  const updateExercise = (exerciseId, field, value) => {
    setSelectedExercises(selectedExercises.map(ex =>
      ex.workout_plan_exercise_id === exerciseId
        ? { ...ex, [field]: field === 'notes' ? value : (parseFloat(value) || 0) }
        : ex
    ));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const payload = {
      scheduled_at: combineDateTime(sessionTimes.scheduled_date, sessionTimes.scheduled_time),
      started_at: combineDateTime(sessionTimes.started_date, sessionTimes.started_time),
      completed_at: combineDateTime(sessionTimes.completed_date, sessionTimes.completed_time),
      exercises: selectedExercises.map(ex => ({
        workout_plan_exercise_id: parseInt(ex.workout_plan_exercise_id, 10),
        actual_sets: parseInt(ex.actual_sets, 10) || 1,
        actual_reps: parseInt(ex.actual_reps, 10) || 1,
        actual_weight: parseFloat(ex.actual_weight) || 0,
        notes: ex.notes
      }))
    };

    try {
      const token = localStorage.getItem('token');
      const url = isEditMode
        ? `http://localhost:5000/api/workout-sessions/${planId}/${sessionId}`
        : `http://localhost:5000/api/workout-sessions/${parseInt(selectedPlanId, 10)}`;

      const method = isEditMode ? 'PATCH' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (response.ok) {
        navigate('/workout-sessions');
      } else {
        setError(data.message || 'Failed to save session');
      }
    } catch (err) {
      setError('An error occurred while saving');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/workout-sessions')}
                className="text-gray-600 hover:text-gray-900"
              >
                ← Back to Sessions
              </button>
              <h1 className="text-xl font-semibold text-gray-900">
                {isEditMode ? 'Edit Workout Session' : 'Create Workout Session'}
              </h1>
            </div>
            <div className="flex items-center">
              <span className="text-gray-700">{user?.email}</span>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          {/* Workout Plan */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Session Details</h2>
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Workout Plan *
              </label>
              <select
                required
                value={selectedPlanId}
                onChange={e => setSelectedPlanId(e.target.value)}
                disabled={isEditMode}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 disabled:bg-gray-100"
              >
                <option value="" disabled>Select a workout plan...</option>
                {workoutPlans.map(plan => (
                  <option key={plan.id} value={plan.id}>{plan.name}</option>
                ))}
              </select>
            </div>

            {/* Session Dates & Times */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {['scheduled','started','completed'].map(field => (
                <div key={field}>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {field.charAt(0).toUpperCase() + field.slice(1)} At
                  </label>
                  <input
                    type="date"
                    value={sessionTimes[`${field}_date`]}
                    onChange={e => setSessionTimes({...sessionTimes, [`${field}_date`]: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 mb-1"
                  />
                  <input
                    type="time"
                    value={sessionTimes[`${field}_time`]}
                    onChange={e => setSessionTimes({...sessionTimes, [`${field}_time`]: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
              ))}
            </div>
          </div>

          {/* Exercises Section */}
          {selectedPlanId && (
            <div className="bg-white shadow rounded-lg p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Exercises</h2>
                <span className="text-sm text-gray-500">
                  {selectedExercises.length} exercise{selectedExercises.length !== 1 ? 's' : ''} added
                </span>
              </div>

              {planExercises.length > 0 && (
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Add Exercise from Plan
                  </label>
                  <select
                    onChange={(e) => {
                      addExercise(e.target.value);
                      e.target.value = '';
                    }}
                    className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                    defaultValue=""
                  >
                    <option value="" disabled>Select an exercise to add...</option>
                    {planExercises
                      .filter(ex => !selectedExercises.find(sel => sel.workout_plan_exercise_id === ex.id))
                      .map(exercise => (
                        <option key={exercise.id} value={exercise.id}>{exercise.name}</option>
                      ))
                    }
                  </select>
                </div>
              )}

              {selectedExercises.length === 0 ? (
                <div className="text-center py-8 bg-gray-50 rounded-lg">
                  <p className="text-gray-500">No exercises added yet. Select exercises from the dropdown above.</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {selectedExercises.map((exercise, index) => (
                    <div key={exercise.workout_plan_exercise_id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex items-center space-x-3">
                          <span className="flex items-center justify-center w-8 h-8 rounded-full bg-green-100 text-green-600 font-semibold text-sm">{index+1}</span>
                          <h3 className="font-semibold text-gray-900">{exercise.name}</h3>
                        </div>
                        <button type="button" onClick={() => removeExercise(exercise.workout_plan_exercise_id)} className="text-red-600 hover:text-red-800">Remove</button>
                      </div>
                      <div className="grid grid-cols-3 gap-4 ml-11 mb-3">
                        <div>
                          <label className="block text-xs font-medium text-gray-600 mb-1">Actual Sets</label>
                          <input type="number" min="1" value={exercise.actual_sets} onChange={e => updateExercise(exercise.workout_plan_exercise_id,'actual_sets',e.target.value)} className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500" />
                        </div>
                        <div>
                          <label className="block text-xs font-medium text-gray-600 mb-1">Actual Reps</label>
                          <input type="number" min="1" value={exercise.actual_reps} onChange={e => updateExercise(exercise.workout_plan_exercise_id,'actual_reps',e.target.value)} className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500" />
                        </div>
                        <div>
                          <label className="block text-xs font-medium text-gray-600 mb-1">Actual Weight (kg)</label>
                          <input type="number" min="0" step="0.5" value={exercise.actual_weight} onChange={e => updateExercise(exercise.workout_plan_exercise_id,'actual_weight',e.target.value)} className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500" />
                        </div>
                      </div>
                      <div className="ml-11">
                        <label className="block text-xs font-medium text-gray-600 mb-1">Notes</label>
                        <textarea value={exercise.notes} onChange={e => updateExercise(exercise.workout_plan_exercise_id,'notes',e.target.value)} placeholder="How did it feel? Any observations?" rows="2" className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500" />
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Actions */}
          <div className="flex space-x-4">
            <button type="button" onClick={() => navigate('/workout-sessions')} className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-3 rounded-md font-medium">Cancel</button>
            <button type="submit" disabled={loading || !selectedPlanId} className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-md font-medium disabled:opacity-50">
              {loading ? 'Saving...' : isEditMode ? 'Update Session' : 'Create Session'}
            </button>
          </div>
        </form>
      </main>
    </div>
  );
};

export default WorkoutSessionForm;
