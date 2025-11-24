import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const WorkoutSessionForm = () => {
  const [workoutPlans, setWorkoutPlans] = useState([]);
  const [selectedPlanId, setSelectedPlanId] = useState('');
  const [selectedExercises, setSelectedExercises] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isEditMode, setIsEditMode] = useState(false);

  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    fetchWorkoutPlans();
    if (id) {
      setIsEditMode(true);
      fetchWorkoutSession();
    }
  }, [id]);

  // Fetch all workout plans to select for this session
  const fetchWorkoutPlans = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:5000/api/workout-plans', {
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        credentials: 'include'
      });

      if (!res.ok) throw new Error('Failed to fetch workout plans');

      const data = await res.json();
      setWorkoutPlans(data);
    } catch (err) {
      console.error(err);
    }
  };

  // Fetch session data if editing
  const fetchWorkoutSession = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:5000/api/workout-sessions/${id}`, {
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        credentials: 'include'
      });

      if (!res.ok) throw new Error('Failed to fetch session');

      const data = await res.json();
      if (data) {
        setSelectedPlanId(data.workout_plan_id);
        setSelectedExercises(data.exercises.map(ex => ({
          exercise_id: ex.id,
          name: ex.name,
          sets: ex.sets,
          reps: ex.reps,
          weight: ex.weight
        })));
      }
    } catch (err) {
      setError('Failed to load session');
    }
  };

  const handleExerciseChange = (exerciseId, field, value) => {
    setSelectedExercises(prev =>
      prev.map(ex =>
        ex.exercise_id === exerciseId
          ? { ...ex, [field]: parseFloat(value) || 0 }
          : ex
      )
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const payload = {
      workout_plan_id: selectedPlanId,
      exercises: selectedExercises.map(ex => ({
        exercise_id: ex.exercise_id,
        sets: ex.sets,
        reps: ex.reps,
        weight: ex.weight
      }))
    };

    try {
      const token = localStorage.getItem('token');
      const url = isEditMode
        ? `http://localhost:5000/api/workout-sessions/${id}`
        : 'http://localhost:5000/api/workout-sessions';
      const method = isEditMode ? 'PATCH' : 'POST';

      const res = await fetch(url, {
        method,
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(payload)
      });

      const data = await res.json();

      if (res.ok) {
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

      {/* Main Form */}
      <main className="max-w-5xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-600">{error}</p>
            </div>
          )}

          {/* Select Workout Plan */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Session Details</h2>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Workout Plan *
            </label>
            <select
              required
              value={selectedPlanId}
              onChange={(e) => setSelectedPlanId(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="" disabled>Select a workout plan...</option>
              {workoutPlans.map(plan => (
                <option key={plan.id} value={plan.id}>
                  {plan.name}
                </option>
              ))}
            </select>
          </div>

          {/* Exercises */}
          {selectedExercises.length > 0 && (
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Exercises</h2>
              <div className="space-y-4">
                {selectedExercises.map((ex, idx) => (
                  <div key={ex.exercise_id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-3">
                      <h3 className="font-semibold text-gray-900">{ex.name}</h3>
                    </div>
                    <div className="grid grid-cols-3 gap-4">
                      <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">Sets</label>
                        <input
                          type="number"
                          min="1"
                          value={ex.sets}
                          onChange={(e) => handleExerciseChange(ex.exercise_id, 'sets', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">Reps</label>
                        <input
                          type="number"
                          min="1"
                          value={ex.reps}
                          onChange={(e) => handleExerciseChange(ex.exercise_id, 'reps', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">Weight (kg)</label>
                        <input
                          type="number"
                          min="0"
                          step="0.5"
                          value={ex.weight}
                          onChange={(e) => handleExerciseChange(ex.exercise_id, 'weight', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex space-x-4">
            <button
              type="button"
              onClick={() => navigate('/workout-sessions')}
              className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-3 rounded-md font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || !selectedPlanId}
              className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-md font-medium disabled:opacity-50"
            >
              {loading ? 'Saving...' : isEditMode ? 'Update Session' : 'Create Session'}
            </button>
          </div>
        </form>
      </main>
    </div>
  );
};

export default WorkoutSessionForm;
