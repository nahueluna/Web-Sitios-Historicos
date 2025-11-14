<script setup> 
import { decodeCredential } from 'vue3-google-login'
import { useSessionStore } from "@/stores/sessionStore"
import router from '@/router'
import api from '@/service/api'
const sessionStore = useSessionStore()
// Se llama cuando el login es exitoso
const callback = async (response) => {
  try {
    const token = response.credential
    const googleResponse = await api.post('/google/auth', { credential: token })
    console.log(googleResponse.data.user)
    
    const user = googleResponse.data.user
    sessionStore.login(user)

    // Obtener tokens JWT
    const jwtResponse = await api.post("/api/auth", { email: user.email })
    console.log("JWT RESPONSE", jwtResponse)
    
    // Almacenar los tokens en tu store de sesión
    sessionStore.setTokens(jwtResponse.data.access_token, jwtResponse.data.refresh_token)
    
  } catch (error) {
    console.error("Error durante el login:", error)
    alert(error.response?.data?.message || "Error durante el login")
  }
}
</script>

<template>
  <GoogleLogin :callback="callback" />
</template>

