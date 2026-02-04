import React, { useState, useEffect } from 'react';
import { API_ENDPOINTS } from '../config/api';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const apiUrl = API_ENDPOINTS.leaderboard;

  useEffect(() => {
    console.log('Leaderboard Component - API Endpoint:', apiUrl);
    
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard Component - Fetched Data:', data);
        // Handle both paginated (.results) and plain array responses
        const leaderboardData = data.results || data;
        console.log('Leaderboard Component - Processed Data:', leaderboardData);
        setLeaderboard(Array.isArray(leaderboardData) ? leaderboardData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Leaderboard Component - Error:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [apiUrl]);

  if (loading) return (
    <div className="container loading-container">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p className="mt-3">Loading leaderboard...</p>
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

  const getRankBadge = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return rank;
  };

  return (
    <div className="container">
      <h2>🏆 Leaderboard</h2>
      <p className="text-muted mb-4">Top performers and competitive rankings</p>
      <div className="table-responsive">
        <table className="table table-hover align-middle">
          <thead>
            <tr>
              <th scope="col" style={{width: '80px'}}>Rank</th>
              <th scope="col">Hero Name</th>
              <th scope="col">Team</th>
              <th scope="col">Total Points</th>
              <th scope="col">Last Updated</th>
            </tr>
          </thead>
          <tbody>
            {leaderboard.length > 0 ? (
              leaderboard.map((entry, index) => {
                const rank = entry.rank || (index + 1);
                const isTopThree = rank <= 3;
                return (
                  <tr key={entry.id || entry.user_id || index} className={isTopThree ? 'table-primary' : ''}>
                    <td>
                      <h4 className="mb-0">{getRankBadge(rank)}</h4>
                    </td>
                    <td><strong>{entry.user_name || entry.user || 'N/A'}</strong></td>
                    <td><span className="badge bg-primary">{entry.team || 'N/A'}</span></td>
                    <td>
                      <h5 className="mb-0 text-success">{entry.total_points || 0}</h5>
                    </td>
                    <td>
                      <span className="text-muted">
                        {entry.last_updated ? new Date(entry.last_updated).toLocaleDateString() : 'N/A'}
                      </span>
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan="5" className="empty-state">No leaderboard data available</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="mt-3">
        <p className="text-muted">Total Competitors: <strong>{leaderboard.length}</strong></p>
      </div>
    </div>
  );
}

export default Leaderboard;
