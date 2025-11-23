import axios from 'axios'
import io from 'socket.io-client'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// Create axios instance with interceptor for auth
const axiosInstance = axios.create({
  baseURL: API_BASE
})

// Add auth header to all requests
axiosInstance.interceptors.request.use((config) => {
  const apiKey = localStorage.getItem('api_key')
  if (apiKey) {
    config.headers['Authorization'] = `Bearer ${apiKey}`
  }
  return config
})

// Auth endpoints
export async function login(apiKey) {
  try {
    const resp = await axios.post(`${API_BASE}/auth/login`, { api_key: apiKey })
    return resp.data
  } catch (err) {
    throw err
  }
}

// Agent endpoints
export async function initializeAgent() {
  const resp = await axiosInstance.post('/agent/initialize')
  return resp.data
}

export async function getStatus() {
  const resp = await axiosInstance.get('/agent/status')
  return resp.data
}

export async function getConfig() {
  const resp = await axiosInstance.get('/agent/config')
  return resp.data
}

export async function queryAgent(query, include_sources = false) {
  const resp = await axiosInstance.post('/agent/query', { query, include_sources })
  return resp.data
}

// WebSocket streaming for real-time responses
export async function queryAgentStreaming(query, include_sources = false, onChunk) {
  return new Promise((resolve, reject) => {
    const apiKey = localStorage.getItem('api_key')
    
    const socket = io(API_BASE, {
      auth: { token: apiKey },
      transports: ['websocket', 'polling']
    })

    socket.on('connect', () => {
      console.log('WebSocket connected')
      socket.emit('query', { query, include_sources })
    })

    socket.on('chunk', (data) => {
      if (onChunk) {
        onChunk(data.chunk)
      }
    })

    socket.on('complete', (data) => {
      socket.disconnect()
      resolve(data)
    })

    socket.on('error', (error) => {
      socket.disconnect()
      reject(new Error(error.message || 'Streaming error'))
    })

    socket.on('connect_error', (error) => {
      socket.disconnect()
      reject(new Error('WebSocket connection failed: ' + error.message))
    })
  })
}

