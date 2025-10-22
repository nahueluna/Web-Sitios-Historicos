<template>
  <button @click="logout">Cerrar Sesión</button>
</template>

<script setup>
import { googleLogout } from 'vue3-google-login';
import { useSessionStore } from "@/stores/sessionStore"
const sessionStore = useSessionStore()

const logout = () => {
  googleLogout();
  sessionStore.logout();
}
</script>