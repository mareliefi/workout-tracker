// frontend/src/components/WorkoutPlanDetail.jsz
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const WorkoutPlanDetail = () => {
  const [workoutPlan, setWorkoutPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    fetchWorkoutPlanDetail();
  }, [id]);

  const fetchWorkoutPlanDetail = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:5000/api/workout-plans/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch workout plan details');
      }

      const data = await response.json();
      const plan =
        Array.isArray(data) && data.length > 0
          ? (data[0].workout ?? data[0])
          : null;
      setWorkoutPlan(plan);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading workout plan details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
          <h3 className="text-red-800 font-medium mb-2">Error Loading Workout Plan</h3>
          <p className="text-red-600">{error}</p>
          <button
            onClick={() => navigate('/workout-plans')}
            className="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm"
          >
            Back to Workout Plan List
          </button>
        </div>
      </div>
    );
  }

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
                Workout Plan Details
              </h1>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <div className="bg-white shadow rounded-lg overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-indigo-500 to-purple-600 px-6 py-8">
            <h1 className="text-3xl font-bold text-white mb-2">
              {workoutPlan.name}
            </h1>
          </div>

          {/* Details */}
          <div className="px-6 py-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-500 mb-1">
                  Workout Plan ID
                </h3>
                <p className="text-lg font-semibold text-gray-900">
                  #{workoutPlan.workout_plan_id}
                </p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-500 mb-1">
                  Created At
                </h3>
                <p className="text-lg font-semibold text-gray-900">
                  {workoutPlan.created_at}
                </p>
              </div>
              {workoutPlan.updated_at && (
                <div className="bg-gray-50 rounded-lg p-4 md:col-span-2">
                  <h3 className="text-sm font-medium text-gray-500 mb-1">
                    Updated At
                  </h3>
                  <p className="text-lg font-semibold text-gray-900">
                    {workoutPlan.updated_at}
                  </p>
                </div>
              )}
              {/* Exercises */}
              <div className="mt-10">
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">Exercises</h2>

                {workoutPlan.exercises?.length > 0 ? (
                  <ul className="space-y-3">
                    {workoutPlan.exercises.map((exercise) => (
                      <li key={exercise.id} className="bg-gray-100 p-4 rounded-md">
                        <p className="text-lg font-semibold text-gray-900">
                          #{exercise.id} — {exercise.name}
                        </p>
                        <p className="text-sm text-gray-600">
                          Sets: {exercise.target_sets} • Reps: {exercise.target_reps} • Weight: {exercise.target_weight} kg
                        </p>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-gray-600">No exercises assigned to this workout plan.</p>
                )}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <button
                onClick={() => navigate('/workout-plans')}
                className="flex-1 bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-md font-medium transition-colors"
              >
                Back to List
              </button>
              <button
                onClick={() => navigate(`/workout-plans/${id}/edit`)}
                className="flex-1 bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-md font-medium transition-colors"
              >
                Edit Workout Plan
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default WorkoutPlanDetail;
