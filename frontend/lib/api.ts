import axios, { AxiosInstance, AxiosError } from 'axios'
import { getAuth } from '@clerk/nextjs/server'
import { logger } from './logger'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use((config) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('clerk_token') : null
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  if (typeof window !== 'undefined') {
    logger.api(config.method?.toUpperCase() || 'GET', config.url || '')
  }
  return config
})

// Response interceptor
api.interceptors.response.use(
  (response) => {
    if (typeof window !== 'undefined') {
      logger.api(response.config.method?.toUpperCase() || 'GET', response.config.url || '', response.status)
    }
    return response
  },
  (error: AxiosError) => {
    if (typeof window !== 'undefined') {
      logger.error(`API Error: ${error.message}`, {
        status: error.response?.status,
        endpoint: error.config?.url,
      })
    }
    return Promise.reject(error)
  }
)

export const tenantApi = {
  create: (data: any) => api.post('/api/v1/tenants', data),
  get: (id: string) => api.get(`/api/v1/tenants/${id}`),
  update: (id: string, data: any) => api.put(`/api/v1/tenants/${id}`, data),
  delete: (id: string) => api.delete(`/api/v1/tenants/${id}`),
  list: () => api.get('/api/v1/tenants'),
  getMetrics: (id: string) => api.get(`/api/v1/tenants/${id}/metrics`),
}

export const authApi = {
  signup: (data: any) => api.post('/api/v1/auth/signup', data),
  login: (email: string, password: string) => api.post('/api/v1/auth/login', { email, password }),
  getCurrentUser: () => api.get('/api/v1/auth/me'),
  addTenantUser: (tenantId: string, data: any) => api.post(`/api/v1/auth/tenant-users/${tenantId}`, data),
  listTenantUsers: (tenantId: string) => api.get(`/api/v1/auth/tenant-users/${tenantId}`),
}

export const apiKeyApi = {
  generate: (tenantId: string) => api.post(`/api/v1/api-keys/${tenantId}`),
  get: (tenantId: string) => api.get(`/api/v1/api-keys/${tenantId}`),
}

export const integrationApi = {
  create: (tenantId: string, data: any) => api.post(`/api/v1/integrations/${tenantId}`, data),
  list: (tenantId: string) => api.get(`/api/v1/integrations/${tenantId}`),
  get: (tenantId: string, integrationId: string) => api.get(`/api/v1/integrations/${tenantId}/${integrationId}`),
  delete: (tenantId: string, integrationId: string) => api.delete(`/api/v1/integrations/${tenantId}/${integrationId}`),
  sync: (tenantId: string, integrationId: string) => api.post(`/api/v1/integrations/${tenantId}/${integrationId}/sync`),
}

export default api
