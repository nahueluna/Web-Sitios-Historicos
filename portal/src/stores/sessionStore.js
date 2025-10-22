import { defineStore } from "pinia";
import { useLoginModalStore } from "@/stores/LoginModal";
import router from '@/router'

export const useSessionStore = defineStore('session', {
  state: () => ({
    user: null,
    redirect_uri: null,
  }),
  actions: {
    login(user) {
      this.user = user;
      localStorage.setItem('user', JSON.stringify(user));
      useLoginModalStore().closeLoginModal();
      router.push(this.redirect_uri || '/');
    },
    logout() {
      this.user = null;
      // Limpiar cookie
      localStorage.clear()
      sessionStorage.clear()

      // No limpia el historial del router
      router.replace()
    },
    isAuthenticated() {
      return this.user !== null;
    }
  },
});