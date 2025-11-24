import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const WorkoutSessionDetail = () => {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    fetchSessionDetail();
  }, [id]);

  const fetchSessionDetail = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:5000/api/workout-sessions/${id}`, {
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        credentials: 'include'
      });

      if (!res.ok) throw new Error('Failed to fetch workout session');

      const data = await res.json();
      setSession(data);
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
          <p className="mt-4 text-gray-600">Loading workout session details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
          <h3 className="text-red-800 font-medium mb-2">Error Loading Session</h3>
          <p className="text-red-600">{error}</p>
          <button
            onClick={() => navigate('/workout-sessions')}
            className="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm"
          >
            Back to Sessions
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
                onClick={() => navigate('/workout-sessions')}
                className="text-gray-600 hover:text-gray-900"
              >
                ← Back to Sessions
              </button>
              <h1 className="text-xl font-semibold text-gray-900">
                Workout Session Details
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
              Session for: {session.workout_plan?.name || 'Workout Plan'}
            </h1>
            <p className="text-indigo-100">
              Session ID: #{session.id}
            </p>
          </div>

          {/* Details */}
          <div className="px-6 py-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-500 mb-1">Created At</h3>
                <p className="text-lg font-semibold text-gray-900">{session.created_at}</p>
              </div>
              {session.updated_at && (
                <div className="bg-gray-50 rounded-lg p-4 md:col-span-2">
                  <h3 className="text-sm font-medium text-gray-500 mb-1">Updated At</h3>
                  <p className="text-lg font-semibold text-gray-900">{session.updated_at}</p>
                </div>
              )}
            </div>

            {/* Exercises */}
            <div className="mt-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">Exercises</h2>
              {session.exercises?.length > 0 ? (
                <ul className="space-y-3">
                  {session.exercises.map(ex => (
                    <li key={ex.id} className="bg-gray-100 p-4 rounded-md">
                      <p className="text-lg font-semibold text-gray-900">
                        #{ex.id} — {ex.name}
                      </p>
                      <p className="text-sm text-gray-600">
                        Sets: {ex.sets} • Reps: {ex.reps} • Weight: {ex.weight} kg
                      </p>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-600">No exercises logged for this session.</p>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 mt-8">
              <button
                onClick={() => navigate('/workout-sessions')}
                className="flex-1 bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-md font-medium transition-colors"
              >
                Back to Sessions
              </button>
              <button
                onClick={() => navigate(`/workout-sessions/${id}/edit`)}
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
