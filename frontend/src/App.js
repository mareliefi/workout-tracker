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
import WorkoutSessionList from './components/WorkoutSessionList';
import WorkoutSessionDetail from './components/WorkoutSessionDetail';
import WorkoutSessionEdit from './components/WorkoutSessionEdit';
import WorkoutSessionForm from './components/WorkoutSessionForm';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Dashboard */}
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

          {/* Workout Session Routes */}
          <Route
            path="/workout-sessions"
            element={
              <ProtectedRoute>
                <WorkoutSessionList />
              </ProtectedRoute>
            }
          />
          <Route
            path="/workout-sessions/create"
            element={
              <ProtectedRoute>
                <WorkoutSessionForm />
              </ProtectedRoute>
            }
          />
          <Route
            path="/workout-sessions/:workout_plan_id/:workout_session_id"
            element={
              <ProtectedRoute>
                <WorkoutSessionDetail />
              </ProtectedRoute>
            }
          />
          <Route
            path="/workout-sessions/:workout_plan_id/:workout_session_id/edit"
            element={
              <ProtectedRoute>
                <WorkoutSessionEdit />
              </ProtectedRoute>
            }
          />

          {/* Default Route */}
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
