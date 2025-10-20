import { defineStore } from "pinia";
import router from '@/router'

export const useSessionStore = defineStore('session', {
  state: () => ({
    user: null,
  }),
  actions: {
    login(user) {
      this.user = user;
      router.push('/')
    },
    logout() {
      this.user = null;
      // Limpiar cookie
      localStorage.clear()
      sessionStorage.clear()

      // No limpia el historial del router
      router.replace('/login')
    },
    isAuthenticated() {
      return this.user !== null;
    }
  },
});