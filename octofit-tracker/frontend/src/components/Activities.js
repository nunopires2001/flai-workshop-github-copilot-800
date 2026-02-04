import React, { useState, useEffect } from 'react';
import { API_ENDPOINTS } from '../config/api';

function Activities() {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiUrl = API_ENDPOINTS.activities;

  useEffect(() => {
    console.log('Activities Component - API Endpoint:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Activities Component - Fetched Data:', data);
        // Handle both paginated (.results) and plain array responses
        const activitiesData = data.results || data;
        console.log('Activities Component - Processed Data:', activitiesData);
        setActivities(Array.isArray(activitiesData) ? activitiesData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Activities Component - Error:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [apiUrl]);

  if (loading) return (
    <div className="container loading-container">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p className="mt-3">Loading activities...</p>
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
      <h2>🏃 Activities</h2>
      <p className="text-muted mb-4">Track all fitness activities and achievements</p>
      <div className="table-responsive">
        <table className="table table-hover align-middle">
          <thead>
            <tr>
              <th scope="col">User</th>
              <th scope="col">Activity Type</th>
              <th scope="col">⏱️ Duration</th>
              <th scope="col">📍 Distance</th>
              <th scope="col">🔥 Calories</th>
              <th scope="col">Date</th>
            </tr>
          </thead>
          <tbody>
            {activities.length > 0 ? (
              activities.map((activity, index) => (
                <tr key={activity.id || index}>
                  <td><strong>{activity.user_name || activity.user || 'User'}</strong></td>
                  <td><span className="badge bg-secondary">{activity.activity_type || 'N/A'}</span></td>
                  <td>{activity.duration_minutes || 0} min</td>
                  <td>{activity.distance_km || 0} km</td>
                  <td><strong className="text-danger">{activity.calories_burned || 0}</strong> kcal</td>
                  <td><span className="text-muted">{activity.date ? new Date(activity.date).toLocaleDateString() : 'N/A'}</span></td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="6" className="empty-state">No activities recorded yet</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="mt-3">
        <p className="text-muted">Total Activities: <strong>{activities.length}</strong></p>
      </div>
    </div>
  );
}

export default Activities;
