<template>
    <div class="header">
        <div >
            <RouterLink to="/">Home</RouterLink>
            <br>
            <RouterLink to="/privado">Privado</RouterLink>
        </div>
        <br>
        <div v-if="!isAuthenticated" >
            <GoogleLogin />
        </div>
        <div v-else>
            <img :src="user.picture" alt="Foto de perfil" width="30" height="30"/>
            <RouterLink  to="/perfil">{{ user.name }}</RouterLink>
            <br><br>
            <GoogleLogout />
        </div>  
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