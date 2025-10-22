<script setup> 
import { decodeCredential } from 'vue3-google-login'
import { useSessionStore } from "@/stores/sessionStore"
import router from '@/router'
const sessionStore = useSessionStore()
// Se llama cuando el login es exitoso
const callback = (response) => {
  
  const user = decodeCredential(response.credential)
  const userData = {
    name: user.name,
    email: user.email,
    picture: user.picture,
    sub: user.sub
  }
  sessionStore.login(userData)
}
</script>

<template>
  <GoogleLogin :callback="callback" />
</template>

