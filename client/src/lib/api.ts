import axios from 'axios'

export const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api/`,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) {
    config.headers = config.headers || {}
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

export async function login(username: string, password: string) {
  const { data } = await axios.post(`${API_URL}/api/auth/login`, { username, password })
  localStorage.setItem('access', data.access)
  localStorage.setItem('refresh', data.refresh)
}

export function logout() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
}


