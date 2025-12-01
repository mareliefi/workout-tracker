// frontend/src/components/WorkoutReport.jsx
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const WorkoutReport = () => {
  const { workout_plan_id } = useParams();
  const navigate = useNavigate();
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const quotes = [
    "Small progress is still progress 💪",
    "You’re stronger than your excuses.",
    "The only bad workout is the one you didn’t do.",
    "One session at a time — you’re getting better!",
  ];

  useEffect(() => {
    fetchReport();
  }, []);

  const fetchReport = async () => {
    try {
      const token = localStorage.getItem("token");
      const res = await fetch(
        `http://localhost:5000/api/reports/workout-plan/${workout_plan_id}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      if (!res.ok) throw new Error("Failed to load report");
      const data = await res.json();
      setReport(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (d) => (d ? new Date(d).toLocaleDateString() : "—");

  if (loading)
    return <div className="p-6 text-center text-gray-600">Loading progress report...</div>;
  if (error)
    return <div className="p-6 text-red-600 text-center">Error: {error}</div>;

  // ---- Derived stats ----
  const sessions = report.workout_plan_sessions;
  const completed = sessions.filter((s) => s.completed_at).length;
  const completionRate = sessions.length ? Math.round((completed / sessions.length) * 100) : 0;

  const lastWorkout = sessions
    .filter((s) => s.completed_at)
    .sort((a, b) => new Date(b.completed_at) - new Date(a.completed_at))[0];

  // PB tracking
  const personalBests = {};

  sessions.forEach((session) =>
    session.session_exercises.forEach((e) => {
      if (!personalBests[e.exercise_name]) {
        personalBests[e.exercise_name] = { weight: null, reps: null, sets: null };
      }

      // Weight PB
      if (
        !personalBests[e.exercise_name].weight ||
        e.actual_weight > personalBests[e.exercise_name].weight.actual_weight
      ) {
        personalBests[e.exercise_name].weight = e;
      }

      // Reps PB
      if (
        !personalBests[e.exercise_name].reps ||
        e.actual_reps > personalBests[e.exercise_name].reps.actual_reps
      ) {
        personalBests[e.exercise_name].reps = e;
      }

      // Sets PB
      if (
        !personalBests[e.exercise_name].sets ||
        e.actual_sets > personalBests[e.exercise_name].sets.actual_sets
      ) {
        personalBests[e.exercise_name].sets = e;
      }
    })
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="p-6 max-w-5xl mx-auto">
        <button
          className="text-indigo-600 hover:text-indigo-800 mb-6"
          onClick={() => navigate(-1)}
        >
          ← Back
        </button>

        <h1 className="text-2xl font-bold mb-3">
          {report.workout_plan_name} — Progress Report
        </h1>

        {/* 🔥 Motivation */}
        <p className="text-lg italic text-gray-700 mb-6">
          {quotes[Math.floor(Math.random() * quotes.length)]}
        </p>

        {/* 🔥 Summary */}
        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white shadow rounded p-4 text-center">
            <p className="text-4xl font-bold">{sessions.length}</p>
            <p className="text-gray-600">Total Sessions</p>
          </div>
          <div className="bg-white shadow rounded p-4 text-center">
            <p className="text-4xl font-bold">{completionRate}%</p>
            <p className="text-gray-600">Completion Rate</p>
          </div>
          <div className="bg-white shadow rounded p-4 text-center">
            <p className="text-2xl font-bold">
              {lastWorkout ? formatDate(lastWorkout.completed_at) : "—"}
            </p>
            <p className="text-gray-600">Last Completed Session</p>
          </div>
        </div>

        {/* 🔥 Personal Bests */}
        <h2 className="text-lg font-semibold mt-6 mb-2">Personal Bests</h2>
        <div className="bg-white shadow rounded p-4 mb-6 space-y-4">

          {Object.entries(personalBests).map(([name, pb]) => (
            <div key={name} className="border-b pb-3">
              <p className="text-xl font-bold mb-1">{name}</p>

              {/* Weight PB */}
              {pb.weight && (
                <div className="text-sm">
                  🏋️ <strong>Heaviest Weight:</strong> {pb.weight.actual_weight}kg
                  {pb.weight.notes && (
                    <p className="mt-1 text-xs italic bg-yellow-50 rounded px-2 py-1 text-yellow-700">
                      💬 "{pb.weight.notes}"
                    </p>
                  )}
                </div>
              )}

              {/* Reps PB */}
              {pb.reps && (
                <div className="text-sm mt-1">
                  🔁 <strong>Most Reps:</strong> {pb.reps.actual_reps}
                  {pb.reps.notes && pb.reps !== pb.weight && (
                    <p className="mt-1 text-xs italic bg-blue-50 rounded px-2 py-1 text-blue-700">
                      💬 "{pb.reps.notes}"
                    </p>
                  )}
                </div>
              )}

              {/* Sets PB */}
              {pb.sets && (
                <div className="text-sm mt-1">
                  📦 <strong>Most Sets:</strong> {pb.sets.actual_sets}
                  {pb.sets.notes && pb.sets !== pb.weight && pb.sets !== pb.reps && (
                    <p className="mt-1 text-xs italic bg-green-50 rounded px-2 py-1 text-green-700">
                      💬 "{pb.sets.notes}"
                    </p>
                  )}
                </div>
              )}
            </div>
          ))}

          {Object.keys(personalBests).length === 0 && (
            <p className="text-gray-500">No completed exercise records yet.</p>
          )}
        </div>

        {/* 🔥 Session details */}
        <h2 className="text-lg font-semibold mb-2">Sessions</h2>
        <div className="space-y-4">
          {sessions.map((session) => (
            <div key={session.session_id} className="bg-white shadow rounded p-4">
              <h3 className="font-semibold mb-2">Session #{session.session_id}</h3>
              <p><strong>Scheduled:</strong> {formatDate(session.scheduled_at)}</p>
              <p><strong>Started:</strong> {formatDate(session.started_at)}</p>
              <p><strong>Completed:</strong> {formatDate(session.completed_at)}</p>

              <h4 className="font-semibold mt-3 mb-1">Exercise Results</h4>
              {session.session_exercises.length === 0 && (
                <p className="text-gray-500">No exercises logged</p>
              )}
              {session.session_exercises.map((s) => (
                <div key={s.id} className="border-t py-2 text-sm">
                  <strong>{s.exercise_name}</strong> — {s.actual_sets} × {s.actual_reps} @ {s.actual_weight}kg
                  {s.notes && <p className="text-gray-500 text-xs">{s.notes}</p>}
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default WorkoutReport;

