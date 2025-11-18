import axios from "axios";
import { useSessionStore } from "../stores/sessionStore";

const api = axios.create({
  baseURL: "http://localhost:5000",
  withCredentials: true, // para enviar cookies si es necesario
});

// Interceptor para añadir el token a todas las requests
api.interceptors.request.use(
  (config) => {
    // Obtener token de localStorage directamente
    const token = useSessionStore().accessToken;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else {
      console.log("No token available for request");
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

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const sessionStore = useSessionStore();
        const newToken = await sessionStore.refreshToken();

        if (newToken) {
          console.log("New token obtained, retrying request");
          originalRequest.headers.Authorization = `Bearer ${newToken}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        console.error("Failed to refresh token:", refreshError);
        const sessionStore = useSessionStore();
        sessionStore.logout();
      }
    }

    return Promise.reject(error);
  }
);


export default api;
