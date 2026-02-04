// API configuration utility
// Determines the correct backend API URL based on environment

const getApiBaseUrl = () => {
  // Check if we have a codespace name environment variable
  const codespaceName = process.env.REACT_APP_CODESPACE_NAME;
  
  // In development, use localhost
  if (process.env.NODE_ENV === 'development' && !codespaceName) {
    return 'http://localhost:8000/api';
  }
  
  // If codespace name is provided, use the codespace URL
  if (codespaceName) {
    return `https://${codespaceName}-8000.app.github.dev/api`;
  }
  
  // Default fallback
  return 'http://localhost:8000/api';
};

export const API_BASE_URL = getApiBaseUrl();

export const API_ENDPOINTS = {
  users: `${API_BASE_URL}/users/`,
  teams: `${API_BASE_URL}/teams/`,
  workouts: `${API_BASE_URL}/workouts/`,
  activities: `${API_BASE_URL}/activities/`,
  leaderboard: `${API_BASE_URL}/leaderboard/`,
};

console.log('API Configuration:', {
  baseUrl: API_BASE_URL,
  endpoints: API_ENDPOINTS,
  environment: process.env.NODE_ENV,
  codespaceName: process.env.REACT_APP_CODESPACE_NAME,
});
