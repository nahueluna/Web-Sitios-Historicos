import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000",
  withCredentials: true, // para enviar cookies si es necesario
});

// Interceptor para añadir el token a todas las requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores de token expirado
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const sessionStore = useSessionStore();
        await sessionStore.refreshToken();
        
        // Reintentar la request original con el nuevo token
        const newToken = localStorage.getItem('accessToken');
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
        
      } catch (refreshError) {
        console.error("No se pudo refrescar el token:", refreshError);
        sessionStore.logout();
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;