import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000', // Change if backend runs elsewhere
  withCredentials: true // for session cookies if needed
});

// after api creation
const storedToken = localStorage.getItem('token');
if (storedToken) {
  api.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
}

// Token management (for JWT auth)
export function setAuthToken(token) {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    localStorage.setItem('token', token);
  } else {
    delete api.defaults.headers.common['Authorization'];
    localStorage.removeItem('token');
  }
}

export function getAuthToken() {
  return localStorage.getItem('token');
}

// Auth APIs
export function login(email, password) {
  return api.post('/api/login', { email, password });
}

export function register(email, full_name, password) {
  return api.post('/api/register', { email, full_name, password });
}

export function logout() {
  return api.post('/api/logout');
}


export default api; 