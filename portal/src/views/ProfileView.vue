<template>
    <div>
        <h1>Perfil de Usuario</h1>
        <img :src="user.picture" alt="Foto de perfil">
        <p>Bienvenido {{ user.name }} a tu perfil.</p>
        <div>
            <h2>Información de la Sesión</h2>
            <ul>
                <li><strong>Correo Electrónico:</strong> {{ user.email }}</li>
                <li><strong>Nombre Completo:</strong> {{ user.name }}</li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { useSessionStore } from "@/stores/sessionStore"
const sessionStore = useSessionStore()
const user = sessionStore.user
</script>