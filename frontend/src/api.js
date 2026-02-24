import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Projects
export const createProject = (projectData) => api.post('/api/projects', projectData)
export const listProjects = () => api.get('/api/projects')
export const getProject = (id) => api.get(`/api/projects/${id}`)
export const updateProject = (id, projectData) => api.put(`/api/projects/${id}`, projectData)
export const deleteProject = (id) => api.delete(`/api/projects/${id}`)

// Takeoffs
export const createTakeoff = (projectId, takeoffData) => api.post(`/api/projects/${projectId}/takeoffs`, takeoffData)
export const listTakeoffs = (projectId) => api.get(`/api/projects/${projectId}/takeoffs`)
export const deleteTakeoff = (projectId, takeoffId) => api.delete(`/api/projects/${projectId}/takeoffs/${takeoffId}`)

// Settings
export const updateSetting = (key, value) => api.post('/api/settings', { key, value })
export const getSetting = (key) => api.get(`/api/settings/${key}`)

// Stats
export const getStats = () => api.get('/api/stats')
export const healthCheck = () => api.get('/health')

export default api
