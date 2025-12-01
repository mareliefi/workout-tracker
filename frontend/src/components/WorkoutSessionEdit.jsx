import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const WorkoutSessionEdit = () => {
  const [selectedPlanId, setSelectedPlanId] = useState('');
  const [selectedExercises, setSelectedExercises] = useState([]);
  const [sessionTimes, setSessionTimes] = useState({
    scheduled_date: '',
    scheduled_time: '',
    started_date: '',
    started_time: '',
    completed_date: '',
    completed_time: ''
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { workout_plan_id, workout_session_id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    if (workout_plan_id && workout_session_id) fetchSession();
    // eslint-disable-next-line
  }, [workout_plan_id, workout_session_id]);

  // Fetch the workout session and its exercises
  const fetchSession = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(
        `http://localhost:5000/api/workout-sessions/${workout_plan_id}/${workout_session_id}`,
        {
          headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }
        }
      );
      const data = await res.json();
      if (res.ok && data.length > 0 && data[0].workout_session) {
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

        setSessionTimes({ scheduled_date, scheduled_time, started_date, started_time, completed_date, completed_time });

        if (session.session_exercises) {
          setSelectedExercises(
            session.session_exercises.map(ex => ({
              workout_plan_exercise_id: ex.workout_plan_exercise_id,
              name: ex.name || `Exercise #${ex.workout_plan_exercise_id}`,
              actual_sets: ex.actual_sets,
              actual_reps: ex.actual_reps,
              actual_weight: ex.actual_weight,
              notes: ex.notes || ''
            }))
          );
        }
      } else {
        setError('Workout session not found.');
      }
    } catch (err) {
      setError('Failed to load session');
    } finally {
      setLoading(false);
    }
  };

  const combineDateTime = (dateStr, timeStr) => {
    if (!dateStr) return null;
    return `${dateStr} ${timeStr || '00:00'}:00`;
  };

  const removeExercise = (exerciseId) => {
    setSelectedExercises(selectedExercises.filter(ex => ex.workout_plan_exercise_id !== exerciseId));
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
      const res = await fetch(
        `http://localhost:5000/api/workout-sessions/${workout_plan_id}/${workout_session_id}`,
        {
          method: 'PATCH',
          headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        }
      );
      const data = await res.json();
      if (res.ok) navigate('/workout-sessions');
      else setError(data.message || 'Failed to update session');
    } catch (err) {
      setError('An error occurred while saving');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading session...</p>
        </div>
      </div>
    );
  }

  if (error) return <div className="p-6 text-center text-red-600">{error}</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow p-4 flex justify-between items-center">
        <button onClick={() => navigate('/workout-sessions')} className="text-gray-600 hover:text-gray-900">← Back to Sessions</button>
        <h1 className="text-xl font-semibold text-gray-900">Edit Workout Session</h1>
        <span className="text-gray-700">{user?.email}</span>
      </nav>

      <main className="max-w-5xl mx-auto py-6 px-4">
        <form onSubmit={handleSubmit} className="space-y-6">

          {/* Workout Plan */}
          <div className="bg-white shadow rounded-lg p-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">Workout Plan</label>
            <select value={selectedPlanId} disabled className="w-full px-4 py-2 border rounded-md">
              <option value={selectedPlanId}>{`Plan #${selectedPlanId}`}</option>
            </select>

            {/* Session Dates */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
              {['scheduled','started','completed'].map(f => (
                <div key={f}>
                  <label className="block text-sm font-medium text-gray-700 mb-1">{f.charAt(0).toUpperCase() + f.slice(1)} At</label>
                  <input type="date" value={sessionTimes[`${f}_date`]} onChange={e => setSessionTimes({...sessionTimes, [`${f}_date`]: e.target.value})} className="w-full px-3 py-2 border rounded-md mb-1"/>
                  <input type="time" value={sessionTimes[`${f}_time`]} onChange={e => setSessionTimes({...sessionTimes, [`${f}_time`]: e.target.value})} className="w-full px-3 py-2 border rounded-md"/>
                </div>
              ))}
            </div>
          </div>

          {/* Exercises */}
          <div className="bg-white shadow rounded-lg p-6 mt-6">
            <h2 className="text-lg font-semibold mb-4">Exercises</h2>

            {/* Header for Sets / Reps / Weight */}
            <div className="grid grid-cols-3 gap-2 mb-2 font-semibold text-gray-700">
              <div className="text-center">Sets</div>
              <div className="text-center">Reps</div>
              <div className="text-center">Weight</div>
            </div>

            {selectedExercises.map((ex, idx) => (
              <div key={ex.workout_plan_exercise_id} className="border p-3 rounded mb-3">
              <div className="flex justify-between items-center mb-2">
                <span className="font-semibold">{idx+1}. {ex.name}</span>
                <button type="button" onClick={() => removeExercise(ex.workout_plan_exercise_id)} className="text-red-600">Remove</button>
              </div>
              <div className="grid grid-cols-3 gap-2">
                <input type="number" min="1" value={ex.actual_sets} onChange={e => updateExercise(ex.workout_plan_exercise_id,'actual_sets',e.target.value)} placeholder="Sets" className="border px-2 py-1 rounded"/>
                <input type="number" min="1" value={ex.actual_reps} onChange={e => updateExercise(ex.workout_plan_exercise_id,'actual_reps',e.target.value)} placeholder="Reps" className="border px-2 py-1 rounded"/>
                <input type="number" min="0" step="0.5" value={ex.actual_weight} onChange={e => updateExercise(ex.workout_plan_exercise_id,'actual_weight',e.target.value)} placeholder="Weight" className="border px-2 py-1 rounded"/>
              </div>
                <textarea value={ex.notes} onChange={e => updateExercise(ex.workout_plan_exercise_id,'notes',e.target.value)} placeholder="Notes" className="w-full border mt-2 px-2 py-1 rounded"/>
              </div>
            ))}
          </div>

          <div className="flex space-x-4">
            <button type="button" onClick={() => navigate('/workout-sessions')} className="flex-1 bg-gray-200 px-6 py-3 rounded">Cancel</button>
            <button type="submit" disabled={loading} className="flex-1 bg-indigo-600 text-white px-6 py-3 rounded">{loading ? 'Saving...' : 'Update Session'}</button>
          </div>
        </form>
      </main>
    </div>
  );
};

export default WorkoutSessionEdit;

