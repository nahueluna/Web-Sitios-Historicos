<template>
  <div class="modal fade" :class="{ show: show, 'd-block': show }" tabindex="-1" role="dialog" aria-labelledby="loginModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="loginModalLabel">Iniciar Sesión</h5>
          <button type="button" class="btn-close" @click="close" aria-label="Cerrar"></button>
        </div>
        <div class="modal-body text-center">
          <p class="mb-4">Por favor, inicia sesión con tu cuenta de Google para acceder a todas las funcionalidades.</p>
          <GoogleLogin />
        </div>
        <div class="modal-footer justify-content-center">
          <router-link to="/" class="btn btn-outline-secondary" @click="close">
            <i class="bi bi-house me-2"></i>
            Volver al Inicio
          </router-link>
        </div>
      </div>
    </div>
  </div>
  <div v-if="show" class="modal-backdrop fade show" @click="close"></div>
</template>

<script setup>
import { useLoginModalStore } from '@/stores/LoginModalStore'
import { useSessionStore } from '@/stores/sessionStore'
import { storeToRefs } from 'pinia'
import GoogleLogin from '@/components/google/GoogleLoginComponent.vue'

const loginModalStore = useLoginModalStore()
const sessionStore = useSessionStore()
const { showLoginModal: show } = storeToRefs(loginModalStore)

function close() {
  sessionStore.redirect_uri = null
  loginModalStore.closeLoginModal()
}
</script>

<style scoped>
/* Bootstrap modal styles are used, no additional styles needed */
</style>
