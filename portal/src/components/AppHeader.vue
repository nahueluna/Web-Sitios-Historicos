<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom sticky-top">
    <div class="container">
      <router-link to="/" class="navbar-brand fw-bold">
        <i class="bi bi-compass"></i>
        Sitios Históricos
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Inicio</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/sites" class="nav-link">Explorar Sitios</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/about" class="nav-link">Acerca de</router-link>
          </li>
        </ul>

        <div class="d-flex">
          <div v-if="!isAuthenticated" class="me-2">
            <GoogleLogin />
          </div>
          <div v-else class="d-flex align-items-center gap-2">
            <router-link to="/profile" class="nav-link">
              <img :src="user.picture" alt="Perfil" width="30" height="30" class="rounded-circle">
            </router-link>
            <GoogleLogout />
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, watchEffect } from 'vue'
import { useSessionStore } from '@/stores/sessionStore'
import GoogleLogin from './google/GoogleLoginComponent.vue'
import GoogleLogout from './google/GoogleLogoutComponent.vue'

const sessionStore = useSessionStore()
const isAuthenticated = ref(sessionStore.isAuthenticated())
const user = ref(sessionStore.user)

watchEffect(() => {
  isAuthenticated.value = sessionStore.isAuthenticated()
  user.value = sessionStore.user
})
</script>

<style scoped>
.navbar-brand {
  font-size: 1.5rem;
}

.nav-link {
  font-weight: 500;
  transition: color 0.2s ease;
}

.nav-link.router-link-active {
  color: var(--bs-primary) !important;
}
</style>