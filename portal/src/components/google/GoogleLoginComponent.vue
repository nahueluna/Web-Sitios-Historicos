<script setup> 
import { decodeCredential } from 'vue3-google-login'
import { useSessionStore } from "@/stores/sessionStore"
import router from '@/router'
const sessionStore = useSessionStore()
// Se llama cuando el login es exitoso
const callback = (response) => {
  
  const userData = decodeCredential(response.credential)
  sessionStore.login(userData)
}
</script>

<template>
  <GoogleLogin :callback="callback" />
</template>

