<template>
    <div class="wrapper">
        <nav>
            <RouterLink to="/">Home</RouterLink>
            <div v-if="!isAuthenticated">
                <RouterLink to="/login">Iniciar Sesión</RouterLink>
            </div>
            <br>
            <div v-if="isAuthenticated">
                <RouterLink to="/profile">{{ user.name }}</RouterLink>
            </div>
            <div v-if="isAuthenticated">
                <GoogleLogout />
            </div>
        </nav>
    </div>
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