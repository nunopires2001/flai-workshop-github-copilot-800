import React, { useState, useEffect } from 'react';
import { API_ENDPOINTS } from '../config/api';

function Users() {
  const [users, setUsers] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingUser, setEditingUser] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    alias: '',
    email: '',
    team: '',
    fitness_level: ''
  });

  const apiUrl = API_ENDPOINTS.users;
  const teamsUrl = API_ENDPOINTS.teams;

  useEffect(() => {
    console.log('Users Component - API Endpoint:', apiUrl);
    
    // Fetch users
    fetch(apiUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Users Component - Fetched Data:', data);
        const usersData = data.results || data;
        console.log('Users Component - Processed Data:', usersData);
        setUsers(Array.isArray(usersData) ? usersData : []);
        setLoading(false);
      })
      .catch(error => {
        console.error('Users Component - Error:', error);
        setError(error.message);
        setLoading(false);
      });

    // Fetch teams for dropdown
    fetch(teamsUrl)
      .then(response => response.json())
      .then(data => {
        const teamsData = data.results || data;
        setTeams(Array.isArray(teamsData) ? teamsData : []);
      })
      .catch(error => {
        console.error('Teams fetch error:', error);
      });
  }, [apiUrl, teamsUrl]);

  const handleEdit = (user) => {
    setEditingUser(user);
    setFormData({
      name: user.name || '',
      alias: user.alias || '',
      email: user.email || '',
      team: user.team || '',
      fitness_level: user.fitness_level || ''
    });
    setShowModal(true);
  };

  const handleClose = () => {
    setShowModal(false);
    setEditingUser(null);
    setFormData({
      name: '',
      alias: '',
      email: '',
      team: '',
      fitness_level: ''
    });
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      // Note: This assumes your backend has a PUT/PATCH endpoint
      // You may need to adjust the URL and method based on your API
      const response = await fetch(`${apiUrl}${editingUser.id || editingUser.email}/`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        // Refresh users list
        const updatedResponse = await fetch(apiUrl);
        const data = await updatedResponse.json();
        const usersData = data.results || data;
        setUsers(Array.isArray(usersData) ? usersData : []);
        handleClose();
        alert('User updated successfully!');
      } else {
        alert('Failed to update user. This feature may not be supported by the backend yet.');
      }
    } catch (error) {
      console.error('Update error:', error);
      alert('Error updating user: ' + error.message);
    }
  };

  if (loading) return (
    <div className="container loading-container">
      <div className="spinner-border text-primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </div>
      <p className="mt-3">Loading users...</p>
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
      <h2>👥 Users</h2>
      <p className="text-muted mb-4">View all registered users and their team information</p>
      <div className="table-responsive">
        <table className="table table-hover align-middle">
          <thead>
            <tr>
              <th scope="col">Hero Name</th>
              <th scope="col">Real Name (Alias)</th>
              <th scope="col">Email</th>
              <th scope="col">Team</th>
              <th scope="col">Fitness Level</th>
              <th scope="col">Total Points</th>
              <th scope="col">Joined</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.length > 0 ? (
              users.map((user) => (
                <tr key={user.id || user.email}>
                  <td><strong>{user.name || 'N/A'}</strong></td>
                  <td><span className="text-secondary">{user.alias || 'N/A'}</span></td>
                  <td><span className="text-muted">{user.email || 'N/A'}</span></td>
                  <td><span className="badge bg-primary">{user.team_name || user.team || 'N/A'}</span></td>
                  <td><span className="badge bg-info">{user.fitness_level || 'N/A'}</span></td>
                  <td><strong className="text-success">{user.total_points || 0}</strong></td>
                  <td>{user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</td>
                  <td>
                    <button 
                      className="btn btn-sm btn-primary"
                      onClick={() => handleEdit(user)}
                    >
                      ✏️ Edit
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="8" className="empty-state">No users found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="mt-3">
        <p className="text-muted">Total Users: <strong>{users.length}</strong></p>
      </div>

      {/* Edit User Modal */}
      {showModal && (
        <div className="modal show d-block" style={{backgroundColor: 'rgba(0,0,0,0.5)'}}>
          <div className="modal-dialog modal-dialog-centered">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">Edit User Details</h5>
                <button type="button" className="btn-close" onClick={handleClose}></button>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="modal-body">
                  <div className="mb-3">
                    <label className="form-label">Hero Name</label>
                    <input
                      type="text"
                      className="form-control"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Real Name (Alias)</label>
                    <input
                      type="text"
                      className="form-control"
                      name="alias"
                      value={formData.alias}
                      onChange={handleChange}
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Email</label>
                    <input
                      type="email"
                      className="form-control"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                    />
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Team</label>
                    <select
                      className="form-select"
                      name="team"
                      value={formData.team}
                      onChange={handleChange}
                      required
                    >
                      <option value="">Select a team...</option>
                      {teams.map((team, index) => (
                        <option key={team.id || index} value={team.name}>
                          {team.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Fitness Level</label>
                    <select
                      className="form-select"
                      name="fitness_level"
                      value={formData.fitness_level}
                      onChange={handleChange}
                      required
                    >
                      <option value="">Select fitness level...</option>
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                    </select>
                  </div>
                </div>
                <div className="modal-footer">
                  <button type="button" className="btn btn-secondary" onClick={handleClose}>
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    Save Changes
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Users;
