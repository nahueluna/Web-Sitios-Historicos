import { defineStore } from 'pinia';
import router from '../router';
import api from '../service/api';
import { useLoginModalStore } from "@/stores/LoginModalStore";

export const useSessionStore = defineStore('session', {
  state: () => ({
    user: null,
    redirect_uri: null,
    accessToken: null,
    refreshToken: null,
    isLoading: false, // Para controlar estados de carga
  }),
  
  getters: {
    isAuthenticated: (state) => state.user !== null,
  },
  
  actions: {
    setTokens(accessToken, refreshToken) {
      this.accessToken = accessToken;
      this.refreshToken = refreshToken;
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
      this.refreshToken = null;
      this.isLoading = false;
      localStorage.removeItem('user');
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      router.replace("/");
    },
    
    async refreshToken() {
      // Evitar múltiples llamadas simultáneas
      if (this.isLoading) {
        return;
      }
      
      this.isLoading = true;
      
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        console.log("Refresh token...");
        
        if (!refreshToken) {
          throw new Error("No hay refresh token disponible");
        }
        
        const response = await api.post('/api/auth/refresh', {}, {
          headers: {
            'Authorization': `Bearer ${refreshToken}`
          }
        });
        
        console.log("Token refrescado exitosamente");
        
        // Actualizar el access token
        this.accessToken = response.data.access_token;
        localStorage.setItem('accessToken', this.accessToken);
        
        return this.accessToken;
        
      } catch (error) {
        console.error("Error refrescando token:", error.response?.data || error.message);
        
        // Solo hacer logout si el error es de autenticación
        if (error.response?.status === 401 || error.response?.status === 422) {
          console.log("Token inválido - cerrando sesión");
          this.logout();
        }
        
        throw error;
      } finally {
        this.isLoading = false;
      }
    },
    
    // Nuevo método para restaurar sesión completa
    async restoreSession() {
      const userData = localStorage.getItem('user');
      const refreshToken = localStorage.getItem('refreshToken');
      
      if (userData && refreshToken && !this.isAuthenticated) {
        try {
          this.user = JSON.parse(userData);
          await this.refreshToken();
          return true;
        } catch (error) {
          this.logout();
          return false;
        }
      }
      return false;
    }
  },
});