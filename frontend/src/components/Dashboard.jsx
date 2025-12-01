// frontend/src/components/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [recentSessions, setRecentSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const fetchRecentSessions = async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:5000/api/workout-sessions', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        credentials: 'include'
      });

      if (!res.ok) throw new Error('Failed to fetch recent sessions');
      const data = await res.json();

      // Guarantee array to avoid "data.sort is not a function"
      const sessionsArray = Array.isArray(data) ? data : Array.isArray(data?.sessions) ? data.sessions : [];

      const sortedSessions = sessionsArray
        .sort((a, b) => {
          const aTime = a.completed_at || a.scheduled_at || 0;
          const bTime = b.completed_at || b.scheduled_at || 0;
          return new Date(bTime) - new Date(aTime);
        })
        .slice(0, 5);

      setRecentSessions(sortedSessions);
    } catch (err) {
      setError(err.message || 'Error loading recent activity');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecentSessions();
  }, []);

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const chartData =
    Array.isArray(recentSessions) && recentSessions.length > 0
      ? [
          { name: 'Sessions Completed', count: recentSessions.filter(s => s.completed_at).length },
          { name: 'Sessions Pending', count: recentSessions.filter(s => !s.completed_at).length }
        ]
      : [];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold text-gray-900">
                Workout Tracker
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome, {user?.name}</span>
              <button
                onClick={handleLogout}
                className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        
        {/* Quick Actions */}
        <div className="mt-8">
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Quick Actions
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <button 
                onClick={() => navigate('/workout-plans/create')}
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Create Workout
              </button>
              <button 
                onClick={() => navigate('/workout-plans')}
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                View Workout Plans
              </button>
              <button 
                onClick={() => navigate('/workout-sessions/create')}
                className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Create/Start Workout Session
              </button>
              <button 
                onClick={() => navigate('/workout-sessions')}
                className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                View Workout Sessions
              </button>
              <button
                onClick={() => navigate('/workout-plans')}
                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                View Progress Report
              </button>
              <button 
                onClick={() => navigate('/exercises')}
                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium"
              >
                Browse Exercises
              </button>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="mt-8">
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium text-gray-900 mb-4">
              Recent Activity
            </h2>

            {/* === First-time user welcome + CTA === */}
            {!loading && !error && recentSessions.length === 0 && (
              <div className="text-center py-6">
                <h3 className="text-xl font-semibold text-gray-800 mb-2">
                  Welcome to your fitness journey! 💪
                </h3>
                <p className="text-gray-600 mb-4">
                  You haven't logged any workout sessions yet — let's get started!
                </p>
                <button
                  onClick={() => navigate('/workout-sessions/create')}
                  className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-md text-md font-medium"
                >
                  Start Your First Workout 🚀
                </button>
              </div>
            )}

            {/* Chart */}
            {recentSessions.length > 0 && (
              <div className="w-full h-64 mb-6">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData}>
                    <XAxis dataKey="name" />
                    <YAxis allowDecimals={false} />
                    <Tooltip />
                    <Bar dataKey="count" fill="#4F46E5" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}

            {loading && <p className="text-gray-500">Loading recent sessions...</p>}
            {error && <p className="text-red-600">{error}</p>}

            {!loading && !error && recentSessions.length > 0 && (
              <ul className="space-y-4 max-h-96 overflow-y-auto">
                {recentSessions.map(session => (
                  <li
                    key={session.id}
                    className="border rounded-md p-4 flex justify-between items-center hover:bg-gray-50"
                  >
                    <div>
                      <p className="font-medium text-gray-900">
                        {session.workout_name + ' Session #' + session.id}
                      </p>
                      <p className="text-sm text-gray-500">
                        {session.completed_at
                          ? `Completed on ${formatDate(session.completed_at)}`
                          : `Scheduled for ${formatDate(session.scheduled_at)}`}
                      </p>
                    </div>
                    <button
                      onClick={() =>
                        navigate(`/workout-sessions/${session.workout_plan_id}/${session.id}`)
                      }
                      className="bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-1 rounded-md text-sm font-medium"
                    >
                      View Session
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;

