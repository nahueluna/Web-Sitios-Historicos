<script setup> 
import { decodeCredential } from 'vue3-google-login'
import { useSessionStore } from "@/stores/sessionStore"
import router from '@/router'
import api from '@/service/api'
const sessionStore = useSessionStore()
// Se llama cuando el login es exitoso
const callback = (response) => {
  const token = response.credential
  api.post('/google/auth', { credential: token })
    .then((response) => {
      console.log(response.data.user)
      const user = response.data.user
      sessionStore.login(user)

      api.post("/api/auth").then(() => {console.log("JWT creado")})
    })
    .catch((error) => {
      console.error(error)
      alert(error.message)
    })
  
}
</script>

<template>
  <GoogleLogin :callback="callback" />
</template>

