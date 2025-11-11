<template>
  <button @click="logout" class="btn btn-outline-danger">
    <i class="bi bi-box-arrow-right me-2"></i>
    Cerrar Sesión
  </button>
</template>

<script setup>
import { googleLogout } from 'vue3-google-login';
import { useSessionStore } from "@/stores/sessionStore"
import api from '@/service/api';
const sessionStore = useSessionStore()

const logout = () => {
  googleLogout();
  api.post('/google/logout')
    .then((response) => {
      console.log(response.data.message);
    })
    .catch((error) => {
      console.error(error);
    });
  sessionStore.logout();
}
</script>