import { defineStore } from 'pinia';
import { ref } from 'vue';
import { api } from "@/utils/api.ts";

export const useAuthStore = defineStore('auth', () => {
  let _logoutTimer: ReturnType<typeof setTimeout> | null = null

  const accessToken = ref('')
  const tokenType = ref('')
  const username = ref('')
  const expiresIn = ref(0)
  const expiresAt = ref(0)
  const balance = ref(0)

  function setToken(data: {
    access_token: string
    token_type: string
    username: string
    expires_in: number
  }) {
    accessToken.value = data.access_token
    tokenType.value = data.token_type
    username.value = data.username
    expiresIn.value = data.expires_in
    expiresAt.value = Date.now() + data.expires_in * 1000
    scheduleAutoLogout()
  }

  function logout() {
    accessToken.value = ''
    tokenType.value = ''
    username.value = ''
    expiresIn.value = 0
    expiresAt.value = 0
    clearTimeout(_logoutTimer!)
  }

  function scheduleAutoLogout() {
    clearTimeout(_logoutTimer!)
    const delay = expiresAt.value - Date.now()
    _logoutTimer = setTimeout(() => logout(), delay > 0 ? delay : 0)
  }

  function tryAutoLogin() {
    if (!accessToken.value || !expiresAt.value) return
    if (Date.now() > expiresAt.value) logout()
    else scheduleAutoLogout()
  }

  async function getUserBalance() {
  try {
    const { data } = await api.get('/points/balance')
    balance.value = data.balance
  } catch (error) {
    console.error('Error loading balance', error)
    logout()
  }
}

  return {
    accessToken,
    tokenType,
    username,
    expiresIn,
    expiresAt,
    balance,
    setToken,
    logout,
    tryAutoLogin,
    getUserBalance
  }
}, {
  persist: true
})
