<template>
    <h1>Iniciar Sesión</h1>
    <p>Por favor, inicia sesión con tu cuenta de Google para acceder a todas las funcionalidades.</p>
    <br><br>
    <GoogleLogin />
    <br><br>
    <p>volver al <RouterLink to="/">Menu Principal</RouterLink></p>
</template>

<script setup>
import GoogleLogin from '@/components/google/GoogleLoginComponent.vue'
import { RouterLink } from 'vue-router'
</script>