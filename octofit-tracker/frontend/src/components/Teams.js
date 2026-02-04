import React, { useState, useEffect } from 'react';
import { API_ENDPOINTS } from '../config/api';

function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiUrl = API_ENDPOINTS.teams;

  useEffect(() => {
    console.log('Teams Component - API Endpoint:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams Component - Fetched Data:', data);
        // Handle both paginated (.results) and plain array responses
        const teamsData = data.results || data;
        console.log('Teams Component - Processed Data:', teamsData);
        setTeams(Array.isArray(teamsData) ? teamsData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Teams Component - Error:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [apiUrl]);

  if (loading) return (
    <div className="container loading-container">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p className="mt-3">Loading teams...</p>
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
      <h2>🏆 Teams</h2>
      <p className="text-muted mb-4">Explore our competitive fitness teams</p>
      <div className="row">
        {teams.length > 0 ? (
          teams.map((team, index) => {
            // Parse member count from the members string
            let memberCount = 0;
            if (team.members) {
              if (Array.isArray(team.members)) {
                memberCount = team.members.length;
              } else if (typeof team.members === 'string') {
                // Count ObjectId occurrences in the string
                const matches = team.members.match(/ObjectId/g);
                memberCount = matches ? matches.length : 0;
              }
            }
            
            return (
              <div key={team.id || index} className="col-md-6 col-lg-4 mb-4">
                <div className="card h-100">
                  <div className="card-body">
                    <h5 className="card-title">{team.name}</h5>
                    <p className="card-text text-muted">{team.description}</p>
                    <div className="mt-3">
                      <span className="badge bg-success me-2">
                        👥 {memberCount} {memberCount === 1 ? 'Member' : 'Members'}
                      </span>
                    </div>
                  </div>
                  <div className="card-footer bg-transparent border-0">
                    <small className="text-muted">
                      📅 Created: {team.created_at ? new Date(team.created_at).toLocaleDateString() : 'N/A'}
                    </small>
                  </div>
                </div>
              </div>
            );
          })
        ) : (
          <div className="col-12">
            <div className="alert alert-info text-center" role="alert">
              No teams found. Be the first to create one!
            </div>
          </div>
        )}
      </div>
      <div className="mt-3">
        <p className="text-muted">Total Teams: <strong>{teams.length}</strong></p>
      </div>
    </div>
  );
}

export default Teams;
