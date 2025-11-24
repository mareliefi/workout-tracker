// frontend/src/components/ExerciseDetail.js
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const ExerciseDetail = () => {
  const [exercise, setExercise] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    fetchExerciseDetail();
  }, [id]);

  const fetchExerciseDetail = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:5000/api/exercises/${id}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch exercise details');
      }

      const data = await response.json();
      setExercise(data);
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
          <p className="mt-4 text-gray-600">Loading exercise details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
          <h3 className="text-red-800 font-medium mb-2">Error Loading Exercise</h3>
          <p className="text-red-600">{error}</p>
          <button
            onClick={() => navigate('/exercises')}
            className="mt-4 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md text-sm"
          >
            Back to Exercise List
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
                onClick={() => navigate('/exercises')}
                className="text-gray-600 hover:text-gray-900"
              >
                ← Back to Exercises
              </button>
              <h1 className="text-xl font-semibold text-gray-900">
                Exercise Details
              </h1>
            </div>
            <div className="flex items-center">
              <span className="text-gray-700">{user?.email}</span>
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
              {exercise.name}
            </h1>
            <div className="flex items-center space-x-3">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-white bg-opacity-20 text-white">
                {exercise.category}
              </span>
              {exercise.muscle_group && (
                <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-white bg-opacity-20 text-white">
                  {exercise.muscle_group}
                </span>
              )}
            </div>
          </div>

          {/* Details */}
          <div className="px-6 py-8">
            <div className="mb-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-3">
                Description
              </h2>
              <p className="text-gray-700 leading-relaxed">
                {exercise.description || 'No description available for this exercise.'}
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-500 mb-1">
                  Exercise ID
                </h3>
                <p className="text-lg font-semibold text-gray-900">
                  #{exercise.id}
                </p>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-500 mb-1">
                  Category
                </h3>
                <p className="text-lg font-semibold text-gray-900">
                  {exercise.category}
                </p>
              </div>
              {exercise.muscle_group && (
                <div className="bg-gray-50 rounded-lg p-4 md:col-span-2">
                  <h3 className="text-sm font-medium text-gray-500 mb-1">
                    Primary Muscle Group
                  </h3>
                  <p className="text-lg font-semibold text-gray-900">
                    {exercise.muscle_group}
                  </p>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4">
              <button
                onClick={() => navigate('/exercises')}
                className="flex-1 bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 rounded-md font-medium transition-colors"
              >
                Back to List
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default ExerciseDetail;