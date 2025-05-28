import axios from 'axios'
import { stringify } from 'qs'
import { useAuthStore } from '@/stores/auth'

export const api = axios.create({
  baseURL: '/api',
  paramsSerializer: params => stringify(params, { arrayFormat: 'repeat' }),
})

api.interceptors.request.use(config => {
  const auth = useAuthStore()
  if (auth.accessToken) {
    config.headers.Authorization = `${auth.tokenType} ${auth.accessToken}`
  }
  return config
})
