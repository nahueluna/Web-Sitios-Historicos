<template>
    <div>
        <h1>Perfil de Usuario</h1>
        <br><br>
        <img :src="user.picture" alt="Foto de perfil">
        <p>Bienvenido {{ user.name }} a tu perfil.</p>
        <br>
        <div>
            <h2>Información de la Sesión</h2>
            <ul>
                <li><strong>Correo Electrónico:</strong> {{ user.email }}</li>
                <li><strong>Nombre Completo:</strong> {{ user.name }} {{ user.lastname }}</li>
            </ul>
        </div>
        <br>
        <div>
            <div v-if="reviews.length === 0">
                <h3>No has escrito ninguna reseña aún.</h3>
            </div>
            <div v-else>
                <h3>
                    <RouterLink to="/mis-reseñas">Ver todas mis reseñas</RouterLink>
                </h3>
                <br>
                <div v-for="review in reviews">
                    <ReviewComponent :review="review" />
                    <br>
                </div>
            </div>
            <div v-if="favorites.length === 0">
                <h3>No has agregado ningún favorito aún.</h3>
            </div>
            <div v-else>
                <h3>
                    <RouterLink to="/mis-favoritos">Ver todos mis favoritos</RouterLink>
                </h3>
                <br>
                <div v-for="favorite in favorites">
                    <FavoriteComponent :favorite="favorite" />
                    <br>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useSessionStore } from "@/stores/sessionStore"
import { useReviewsStore } from '@/stores/reviewsStore'
import { useFavoritesStore } from '@/stores/favoriteStore'
import ReviewComponent from '@/components/ReviewComponent.vue'
import FavoriteComponent from '@/components/FavoriteComponent.vue'
const sessionStore = useSessionStore()
const reviewsStore = useReviewsStore()
const favoritesStore = useFavoritesStore()

const user = sessionStore.user
const reviews = reviewsStore.reviews.slice(0, 3)
const favorites = favoritesStore.favorites.slice(0, 3)

</script>