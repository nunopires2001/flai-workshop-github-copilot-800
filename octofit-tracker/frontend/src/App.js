import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Users from './components/Users';
import Teams from './components/Teams';
import Workouts from './components/Workouts';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">🏋️ OctoFit Tracker</Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav" 
              aria-controls="navbarNav" 
              aria-expanded="false" 
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                <li className="nav-item">
                  <Link className="nav-link" to="/users">Users</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">Teams</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">Workouts</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">Activities</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={
            <div className="container">
              <div className="welcome-section">
                <h1 className="display-3">🏋️ Welcome to OctoFit Tracker! 🎯</h1>
                <p className="lead">Track your fitness journey, compete with your team, and achieve your goals!</p>
                <hr className="my-4" />
                <p className="text-muted mb-4">Quick access to the main sections:</p>
                <div className="row mt-4">
                  <div className="col-md-4 mb-3">
                    <Link to="/users" className="text-decoration-none">
                      <div className="card text-center h-100 hover-card">
                        <div className="card-body">
                          <h2 className="mb-3">👥</h2>
                          <h5 className="card-title">Users</h5>
                          <p className="card-text text-muted">View all registered heroes and their stats</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-4 mb-3">
                    <Link to="/activities" className="text-decoration-none">
                      <div className="card text-center h-100 hover-card">
                        <div className="card-body">
                          <h2 className="mb-3">🏃</h2>
                          <h5 className="card-title">Activities</h5>
                          <p className="card-text text-muted">Track all fitness activities and achievements</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-4 mb-3">
                    <Link to="/leaderboard" className="text-decoration-none">
                      <div className="card text-center h-100 hover-card">
                        <div className="card-body">
                          <h2 className="mb-3">🏆</h2>
                          <h5 className="card-title">Leaderboard</h5>
                          <p className="card-text text-muted">See who's leading the competition</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                </div>
                <div className="row mt-3">
                  <div className="col-md-6 mb-3">
                    <Link to="/teams" className="text-decoration-none">
                      <div className="card text-center h-100 hover-card">
                        <div className="card-body">
                          <h2 className="mb-3">🏅</h2>
                          <h5 className="card-title">Teams</h5>
                          <p className="card-text text-muted">Explore competitive fitness teams</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                  <div className="col-md-6 mb-3">
                    <Link to="/workouts" className="text-decoration-none">
                      <div className="card text-center h-100 hover-card">
                        <div className="card-body">
                          <h2 className="mb-3">💪</h2>
                          <h5 className="card-title">Workouts</h5>
                          <p className="card-text text-muted">Browse workout programs and training plans</p>
                        </div>
                      </div>
                    </Link>
                  </div>
                </div>
              </div>
            </div>
          } />
          <Route path="/users" element={<Users />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/workouts" element={<Workouts />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
