import React, { useState, useEffect } from 'react';
import { API_ENDPOINTS } from '../config/api';

function Workouts() {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiUrl = API_ENDPOINTS.workouts;

  useEffect(() => {
    console.log('Workouts Component - API Endpoint:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Workouts Component - Fetched Data:', data);
        // Handle both paginated (.results) and plain array responses
        const workoutsData = data.results || data;
        console.log('Workouts Component - Processed Data:', workoutsData);
        setWorkouts(Array.isArray(workoutsData) ? workoutsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Workouts Component - Error:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [apiUrl]);

  if (loading) return (
    <div className="container loading-container">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p className="mt-3">Loading workouts...</p>
    </div>
  );
  
  if (error) return (
    <div className="container error-container">
      <div className="alert alert-danger" role="alert">
        <h4 className="alert-heading">Error!</h4>
        <p>{error}</p>
      </div>
    </div>
  );

  return (
    <div className="container">
      <h2>💪 Workouts</h2>
      <p className="text-muted mb-4">Browse available workout programs and training plans</p>
      <div className="row">
        {workouts.length > 0 ? (
          workouts.map((workout, index) => (
            <div key={workout.id || index} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">{workout.name || 'Unnamed Workout'}</h5>
                  <p className="card-text text-muted">{workout.description || 'No description available'}</p>
                  <hr />
                  <div className="mb-2">
                    <span className="badge bg-info">{workout.difficulty_level || workout.difficulty || 'N/A'}</span>
                  </div>
                  <ul className="list-unstyled mt-3">
                    <li className="mb-2">⏱️ <strong>Duration:</strong> {workout.duration_minutes || 0} min</li>
                    <li className="mb-2">🔥 <strong>Calories:</strong> {workout.calories_burned || 0} kcal</li>
                  </ul>
                </div>
                <div className="card-footer bg-transparent border-0">
                  <button className="btn btn-primary btn-sm w-100">Start Workout</button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-12">
            <div className="alert alert-info text-center" role="alert">
              No workouts available at the moment.
            </div>
          </div>
        )}
      </div>
      <div className="mt-3">
        <p className="text-muted">Total Workouts: <strong>{workouts.length}</strong></p>
      </div>
    </div>
  );
}

export default Workouts;
