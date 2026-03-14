import axios from "axios";
import { useSessionStore } from "../stores/sessionStore";
import { useLoginModalStore } from "@/stores/LoginModalStore";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true, // para enviar cookies si es necesario
});

// Interceptor para añadir el token a todas las requests
api.interceptors.request.use(
  (config) => {
    // Obtener token de localStorage directamente
    const token = useSessionStore().accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor de respuesta para manejar tokens expirados
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401) {
      const sessionStore = useSessionStore();
      if (sessionStore.user == null) {
        const loginModalStore = useLoginModalStore();
        loginModalStore.openLoginModal();
        return Promise.reject(error);
      } else if (!originalRequest._retry) {
        originalRequest._retry = true;

        try {
          const newToken = await sessionStore.refreshToken();

          if (newToken) {
            originalRequest.headers.Authorization = `Bearer ${newToken}`;
            return api(originalRequest);
          }
        } catch (refreshError) {
          console.error("Failed to refresh token:", refreshError);
          sessionStore.logout();
        }
      }
    }
    return Promise.reject(error);
  });


export default api;
