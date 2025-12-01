// frontend/src/components/WorkoutSessionDetail.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const WorkoutSessionDetail = () => {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { workout_plan_id, workout_session_id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    fetchWorkoutSession();
  }, [workout_plan_id, workout_session_id]);

  const fetchWorkoutSession = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(
        `http://localhost:5000/api/workout-sessions/${workout_plan_id}/${workout_session_id}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          credentials: 'include'
        }
      );

      if (!response.ok) {
        throw new Error('Failed to fetch workout session details');
      }

      const data = await response.json();

      // API returns [{ workout_session: {...} }], so we extract it
      const ws = Array.isArray(data) && data.length > 0 ? data[0].workout_session : null;

      setSession(ws);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading workout session details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
          <h3 className="text-red-800 font-medium mb-2">Error Loading Workout Session</h3>
          <p className="text-red-600">{error}</p>
          <button
            onClick={() => navigate('/workout-sessions')}
            className="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm"
          >
            Back to Workout Sessions
          </button>
        </div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600">Workout session not found.</p>
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
                onClick={() => navigate('/workout-sessions')}
                className="text-gray-600 hover:text-gray-900"
              >
                ← Back to Workout Sessions
              </button>
              <h1 className="text-xl font-semibold text-gray-900">
                Workout Session Details
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">{user?.name}</span>
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
              Session #{session.workout_session_id}
            </h1>
            <p className="text-white">
              Scheduled: {formatDate(session.scheduled_at)} • Completed: {formatDate(session.completed_at)}
            </p>
          </div>

          {/* Details */}
          <div className="px-6 py-8">
            <div className="grid grid-cols-1 gap-6 mb-8">
              {/* Session Info */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-500 mb-1">Workout Plan ID</h3>
                <p className="text-lg font-semibold text-gray-900">
                  #{session.workout_plan_id}
                </p>
              </div>

              {/* Exercises */}
              <div>
                <h2 className="text-2xl font-semibold text-gray-800 mb-4">Exercises</h2>
                {session.session_exercises?.length > 0 ? (
                  <ul className="space-y-3">
                    {session.session_exercises.map((ex, idx) => (
                      <li key={idx} className="bg-gray-100 p-4 rounded-md">
                        <p className="text-lg font-semibold text-gray-900">
                          #{ex.workout_plan_exercise_id} {ex.name}
                        </p>
                        <p className="text-sm text-gray-600">
                          Sets: {ex.actual_sets} • Reps: {ex.actual_reps} • Weight: {ex.actual_weight} kg
                        </p>
                        {ex.notes && <p className="text-sm text-gray-500 mt-1">Notes: {ex.notes}</p>}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-gray-600">No exercises recorded for this session.</p>
                )}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <button
                onClick={() => navigate('/workout-sessions')}
                className="flex-1 bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-md font-medium transition-colors"
              >
                Back to List
              </button>
              <button
                onClick={() =>
                  navigate(
                    `/workout-sessions/${session.workout_plan_id}/${session.workout_session_id}/edit`
                  )
                }
                className="flex-1 bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-md font-medium transition-colors"
              >
                Edit Session
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default WorkoutSessionDetail;


