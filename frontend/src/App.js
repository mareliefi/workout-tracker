// frontend/src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import AuthProvider from './contexts/AuthContext';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import ExerciseList from './components/ExerciseList';
import ExerciseDetail from './components/ExerciseDetail';
import WorkoutPlanList from './components/WorkoutPlanList';
import WorkoutPlanDetail from './components/WorkoutPlanDetail';
import WorkoutPlanForm from './components/WorkoutPlanForm';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          
          {/* Exercise Routes */}
          <Route
            path="/exercises"
            element={
              <ProtectedRoute>
                <ExerciseList />
              </ProtectedRoute>
            }
          />
          <Route
            path="/exercises/:id"
            element={
              <ProtectedRoute>
                <ExerciseDetail />
              </ProtectedRoute>
            }
          />
          
          {/* Workout Plan Routes */}
          <Route
            path="/workout-plans"
            element={
              <ProtectedRoute>
                <WorkoutPlanList />
              </ProtectedRoute>
            }
          />
          <Route
            path="/workout-plans/create"
            element={
              <ProtectedRoute>
                <WorkoutPlanForm />
              </ProtectedRoute>
            }
          />
          <Route
            path="/workout-plans/:id"
            element={
              <ProtectedRoute>
                <WorkoutPlanDetail />
              </ProtectedRoute>
            }
          />
          <Route
            path="/workout-plans/:id/edit"
            element={
              <ProtectedRoute>
                <WorkoutPlanForm />
              </ProtectedRoute>
            }
          />
          
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;