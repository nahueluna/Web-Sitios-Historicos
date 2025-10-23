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
        
            <h3><RouterLink to="/mis-reseñas">Ver todas mis reseñas</RouterLink></h3>
            <br>
            <div>
                <div v-for="review in reviews">
                    <ReviewComponent :review="review" />
                    <br>
                </div>
            </div>
            
            <!--<RouterLink to="/favoritos">Favoritos</RouterLink>-->
        </div>
    </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useSessionStore } from "@/stores/sessionStore"
import { useReviewsStore } from '@/stores/reviewsStore'
import ReviewComponent from '@/components/ReviewComponent.vue'
import { onMounted } from 'vue'
const sessionStore = useSessionStore()
const reviewsStore = useReviewsStore()

const user = sessionStore.user
const reviews = reviewsStore.reviews.slice(0,5)

//onMounted(() => {
//    review.value = reviewsStore.getReviews(5)
//})

</script>