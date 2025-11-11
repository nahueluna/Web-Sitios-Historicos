<template>
    <nav class="header d-flex align-items-center justify-content-between">
        <div class="d-flex align-items-center gap-3">
            <RouterLink to="/" class="navbar-brand text-white">Home</RouterLink>
            <RouterLink to="/privado" class="nav-link text-white">Privado</RouterLink>
        </div>

        <div>
            <div v-if="!isAuthenticated">
                <GoogleLogin />
            </div>
            <div v-else class="d-flex align-items-center gap-2">
                <RouterLink to="/mis-reseñas" class="nav-link text-white">Mis Reseñas</RouterLink>
                <RouterLink to="/mis-favoritos" class="nav-link text-white">Mis Favoritos</RouterLink>
                <img :src="user.picture" alt="Foto de perfil" width="30" height="30" class="rounded-circle"/>
                <RouterLink to="/perfil" class="nav-link text-white">{{ user.name }}</RouterLink>
                <GoogleLogout />
            </div>
        </div>
    </nav>
</template>

<script setup>
import GoogleLogin from './google/GoogleLoginComponent.vue'
import GoogleLogout from './google/GoogleLogoutComponent.vue'
import { useSessionStore } from "@/stores/sessionStore"
import { ref, watchEffect } from 'vue'

const sessionStore = useSessionStore()
const isAuthenticated = ref(sessionStore.isAuthenticated())
const user = ref(sessionStore.user)

watchEffect(() => {
    isAuthenticated.value = sessionStore.isAuthenticated()
    user.value = sessionStore.user
})

</script>