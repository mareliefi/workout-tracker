// frontend/src/components/WorkoutPlanForm.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const WorkoutPlanForm = () => {
  const [name, setName] = useState('');
  const [exercises, setExercises] = useState([]);
  const [availableExercises, setAvailableExercises] = useState([]);
  const [selectedExercises, setSelectedExercises] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isEditMode, setIsEditMode] = useState(false);
  
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    fetchAvailableExercises();
    if (id) {
      setIsEditMode(true);
      fetchWorkoutPlan();
    }
  }, [id]);

  const fetchAvailableExercises = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/api/exercises', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        setAvailableExercises(data);
      }
    } catch (err) {
      console.error('Error fetching exercises:', err);
    }
  };

  const fetchWorkoutPlan = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:5000/api/workout-plans/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        credentials: 'include'
      });

      if (response.ok) {
        const data = await response.json();
        if (data && data.length > 0 && data[0].workout) {
          const workout = data[0].workout;
          setName(workout.name);
          setSelectedExercises(workout.exercises.map(ex => ({
            exercise_id: ex.id,
            name: ex.name,
            target_sets: ex.target_sets,
            target_reps: ex.target_reps,
            target_weight: ex.target_weight
          })));
        }
      }
    } catch (err) {
      setError('Failed to load workout plan');
    }
  };

  const addExercise = (exerciseId) => {
    const exercise = availableExercises.find(ex => ex.id === parseInt(exerciseId));
    if (exercise && !selectedExercises.find(ex => ex.exercise_id === exercise.id)) {
      setSelectedExercises([...selectedExercises, {
        exercise_id: exercise.id,
        name: exercise.name,
        target_sets: 3,
        target_reps: 10,
        target_weight: 0
      }]);
    }
  };

  const removeExercise = (exerciseId) => {
    setSelectedExercises(selectedExercises.filter(ex => ex.exercise_id !== exerciseId));
  };

  const updateExercise = (exerciseId, field, value) => {
    setSelectedExercises(selectedExercises.map(ex => 
      ex.exercise_id === exerciseId 
        ? { ...ex, [field]: parseFloat(value) || 0 }
        : ex
    ));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const payload = {
      name,
      exercises: selectedExercises.map(ex => ({
        exercise_id: ex.exercise_id,
        target_sets: ex.target_sets,
        target_reps: ex.target_reps,
        target_weight: ex.target_weight
      }))
    };

    try {
      const token = localStorage.getItem('token');
      const url = isEditMode 
        ? `http://localhost:5000/api/workout-plans/${id}`
        : 'http://localhost:5000/api/workout-plans';
      
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
        navigate('/workout-plans');
      } else {
        setError(data.message || 'Failed to save workout plan');
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
                onClick={() => navigate('/workout-plans')}
                className="text-gray-600 hover:text-gray-900"
              >
                ← Back to Workout Plans
              </button>
              <h1 className="text-xl font-semibold text-gray-900">
                {isEditMode ? 'Edit Workout Plan' : 'Create Workout Plan'}
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

          {/* Plan Name */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Plan Details</h2>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Workout Plan Name *
              </label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g., Upper Body Strength"
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
          </div>

          {/* Add Exercises */}
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Exercises</h2>
              <span className="text-sm text-gray-500">
                {selectedExercises.length} exercise{selectedExercises.length !== 1 ? 's' : ''} added
              </span>
            </div>

            {/* Exercise Selector */}
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Add Exercise
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
                {availableExercises
                  .filter(ex => !selectedExercises.find(sel => sel.exercise_id === ex.id))
                  .map(exercise => (
                    <option key={exercise.id} value={exercise.id}>
                      {exercise.name} - {exercise.category}
                    </option>
                  ))
                }
              </select>
            </div>

            {/* Selected Exercises */}
            {selectedExercises.length === 0 ? (
              <div className="text-center py-8 bg-gray-50 rounded-lg">
                <p className="text-gray-500">No exercises added yet. Select exercises from the dropdown above.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {selectedExercises.map((exercise, index) => (
                  <div key={exercise.exercise_id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <span className="flex items-center justify-center w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 font-semibold text-sm">
                          {index + 1}
                        </span>
                        <h3 className="font-semibold text-gray-900">{exercise.name}</h3>
                      </div>
                      <button
                        type="button"
                        onClick={() => removeExercise(exercise.exercise_id)}
                        className="text-red-600 hover:text-red-800"
                      >
                        Remove
                      </button>
                    </div>
                    
                    <div className="grid grid-cols-3 gap-4 ml-11">
                      <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">
                          Sets
                        </label>
                        <input
                          type="number"
                          min="1"
                          value={exercise.target_sets}
                          onChange={(e) => updateExercise(exercise.exercise_id, 'target_sets', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">
                          Reps
                        </label>
                        <input
                          type="number"
                          min="1"
                          value={exercise.target_reps}
                          onChange={(e) => updateExercise(exercise.exercise_id, 'target_reps', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                        />
                      </div>
                      <div>
                        <label className="block text-xs font-medium text-gray-600 mb-1">
                          Weight (kg)
                        </label>
                        <input
                          type="number"
                          min="0"
                          step="0.5"
                          value={exercise.target_weight}
                          onChange={(e) => updateExercise(exercise.exercise_id, 'target_weight', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-4">
            <button
              type="button"
              onClick={() => navigate('/workout-plans')}
              className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 px-6 py-3 rounded-md font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading || !name}
              className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-md font-medium disabled:opacity-50"
            >
              {loading ? 'Saving...' : isEditMode ? 'Update Plan' : 'Create Plan'}
            </button>
          </div>
        </form>
      </main>
    </div>
  );
};

export default WorkoutPlanForm;