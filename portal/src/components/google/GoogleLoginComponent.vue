<script setup>
import { useSessionStore } from "@/stores/sessionStore"
import api from '@/service/api'

const sessionStore = useSessionStore()
// Se llama cuando el login es exitoso
const callback = async (response) => {
  try {
    const token = response.credential
    const googleResponse = await api.post('/google/auth', { credential: token })

    const user = googleResponse.data.user
    sessionStore.login(user)

    // Obtener tokens JWT
    const jwtResponse = await api.post("/api/auth", { email: user.email })
    // Almacenar los tokens en tu store de sesión
    sessionStore.setTokens(jwtResponse.data.access_token, jwtResponse.data.refresh_token)

  } catch (error) {
    console.error("Error durante el login:", error)
  }
}
</script>

<template>
  <GoogleLogin :callback="callback" />
</template>

