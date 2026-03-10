<template>
  <!-- sticky-top: mantiene la navbar fija en la parte superior al hacer scroll -->
  <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom sticky-top">
    <!-- container: centra el contenido con ancho máximo responsivo -->
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
        <!-- ms-auto: empuja la lista de navegación hacia la derecha usando margen automático al inicio -->
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link to="/" class="nav-link">Inicio</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/sites" class="nav-link">Explorar Sitios</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/about" class="nav-link">Acerca de</router-link>
          </li>
          <li>
            <template v-if="!isAuthenticated">
              <GoogleLogin />
            </template>
            <template v-else>
              <router-link to="/profile" class="nav-link">
                <!-- rounded-circle: hace que la imagen del perfil sea perfectamente circular -->
                <img :src="user.picture" alt="Perfil" width="30" height="30" class="rounded-circle">
              </router-link>
            </template>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useSessionStore } from '@/stores/sessionStore'
import { storeToRefs } from 'pinia'
import GoogleLogin from './google/GoogleLoginComponent.vue'

const sessionStore = useSessionStore()
const { isAuthenticated, user } = storeToRefs(sessionStore)
</script>

<style scoped>
.navbar-brand {
  font-size: 1.5rem;
}

.nav-link {
  font-weight: 500;
  /* transition: anima el cambio de color en 0.2 segundos con easing ease */
  transition: color 0.2s ease;
}

.nav-link.router-link-active {
  /* !important: fuerza el color primario de Bootstrap, ignorando otras reglas de especificidad */
  color: var(--bs-primary) !important;
}



</style>