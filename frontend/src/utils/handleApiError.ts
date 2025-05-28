import { isAxiosError } from 'axios'

export function handleApiError(error: unknown, fallback = 'Something went wrong.') {
  if (isAxiosError(error)) {
    return error.response?.data?.message || fallback
  }
  return String(error)
}
