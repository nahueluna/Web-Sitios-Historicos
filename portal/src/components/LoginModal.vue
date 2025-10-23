<template>
  <div v-if="show" class="modal-overlay" @click.self="close">
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="login-title">
      <button class="modal-close" @click="close" aria-label="Cerrar">×</button>
      <h2 id="login-title">Iniciar Sesión</h2>
      <p>Por favor, inicia sesión con tu cuenta de Google para acceder a todas las funcionalidades.</p>
      <div class="modal-body">
        <GoogleLogin />
      </div>
      <p class="modal-footer">volver al <RouterLink to="/" @click="close">Menu Principal</RouterLink></p>
    </div>
  </div>
</template>

<script setup>
import {  watchEffect } from 'vue'
import { useLoginModalStore } from '@/stores/LoginModalStore'
import { useSessionStore } from '@/stores/sessionStore'
import GoogleLogin from '@/components/google/GoogleLoginComponent.vue'
import { RouterLink } from 'vue-router'
import { ref } from 'vue'

const LoginModal = useLoginModalStore();
const show = ref(LoginModal.showLoginModal);

function close() {
    useSessionStore().redirect_uri = null;
    LoginModal.closeLoginModal();
}

watchEffect(() => {
    show.value = LoginModal.showLoginModal;
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1200;
  padding: 1rem;
}

.modal {
  background: var(--app-bg, #ffffff);
  color: var(--text-color, #0f1724);
  max-width: 520px;
  width: 100%;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 10px 40px rgba(2, 6, 23, 0.25);
  position: relative;
  max-height: 35vh; /* ensure modal never exceeds viewport */
  overflow: auto; /* allow inner scrolling */
  display: flex;
  flex-direction: column;
}

.modal h2 {
  margin: 0 0 0.25rem 0;
  font-size: 1.25rem;
}

.modal p {
  margin: 0 0 0.75rem 0;
  color: var(--muted, #6b7280);
}

.modal-close {
  position: absolute;
  top: 8px;
  right: 8px;
  border: none;
  background: transparent;
  font-size: 1.25rem;
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
}

.modal-close:focus {
  outline: 2px solid var(--brand, #0ea5a4);
  outline-offset: 2px;
}

.modal-body {
  margin: 0.75rem 0 1rem 0;
  display: flex;
  justify-content: center;
}

.modal-footer {
  text-align: center;
  margin-top: 0.5rem;
}

/* Make sure the Google button is prominent on small screens */
@media (max-width: 560px) {
  .modal { max-width: 100%; padding: 0.85rem; }
  .modal h2 { font-size: 1.1rem; }
  .modal-body { margin: 0.6rem 0; }
}

</style>
