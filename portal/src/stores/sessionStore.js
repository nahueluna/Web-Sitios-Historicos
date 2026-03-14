import { defineStore } from 'pinia';
import router from '../router';
import api from '../service/api';
import { useLoginModalStore } from "@/stores/LoginModalStore";
import axios from 'axios';

export const useSessionStore = defineStore('session', {
  state: () => ({
    user: null,
    redirect_uri: null,
    accessToken: null,
    _refreshToken: null,
  }),

  getters: {
    isAuthenticated: (state) => state.user !== null,
  },

  actions: {
    setTokens(accessToken, refreshToken) {
      this.accessToken = accessToken;
      this._refreshToken = refreshToken;
      localStorage.setItem('accessToken', accessToken);
      localStorage.setItem('refreshToken', refreshToken);
    },

    login(user) {
      this.user = user;
      localStorage.setItem('user', JSON.stringify(user));
      useLoginModalStore().closeLoginModal();
      if (this.redirect_uri) {
        router.push(this.redirect_uri);
        this.redirect_uri = null;
      } else {
        router.push('/');
      }
    },

    logout() {
      this.user = null;
      this.accessToken = null;
      this._refreshToken = null;
      localStorage.removeItem('user');
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      router.replace("/");
    },

    async refreshToken() {
      const refreshToken = localStorage.getItem('refreshToken');
      this._refreshToken = refreshToken;
      // Usar axios directamente para evitar problemas de interceptor
      const response = await axios.post(
        `${api.defaults.baseURL}/api/auth/refresh`,
        {}, // Body vacío
        {
          headers: {
            'Authorization': `Bearer ${refreshToken}`
          }
        }
      );
      const newAccessToken = response.data.access_token;
      this.accessToken = newAccessToken;
      localStorage.setItem('accessToken', newAccessToken);
      return newAccessToken;
    },

    // Método para restaurar sesión completa
    async restoreSession() {
      const userData = localStorage.getItem('user');
      const storedAccessToken = localStorage.getItem('accessToken');
      const storedRefreshToken = localStorage.getItem('refreshToken');

      if (userData && storedAccessToken && storedRefreshToken) {
        try {
          this.user = JSON.parse(userData);
          this.accessToken = storedAccessToken;
          this._refreshToken = storedRefreshToken;

          // Verificar si el token actual sigue siendo válido
          await this.refreshToken();
          return true;
        } catch (error) {
          console.error("Error restaurando sesión:", error);
          this.logout();
          return false;
        }
      }
      return false;
    }
  },
});
