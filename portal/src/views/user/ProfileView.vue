<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card shadow-sm">
          <div class="card-body text-center">
            <img :src="user.picture" alt="Foto de perfil" class="rounded-circle mb-3" width="100" height="100">
            <h1 class="h3 mb-1">Bienvenido, {{ user.name }}</h1>
            <p class="text-muted">{{ user.email }}</p>
          </div>
        </div>

        <div class="card shadow-sm mt-4">
          <div class="card-body">
            <h2 class="h4 mb-3">Información de la Sesión</h2>
            <ul class="list-unstyled">
              <li><strong>Correo Electrónico:</strong> {{ user.email }}</li>
              <li><strong>Nombre Completo:</strong> {{ user.name }} {{ user.lastname }}</li>
            </ul>
          </div>
        </div>

        <div class="mt-4">
          <div v-if="reviews.length === 0" class="alert alert-info">
            <i class="bi bi-info-circle me-2"></i>
            No has escrito ninguna reseña aún.
          </div>
          <div v-else>
            <h3 class="h4 mb-3">
              <router-link to="/mis-reseñas" class="text-decoration-none">Mis Reseñas Recientes</router-link>
            </h3>
            <div class="row g-3">
              <div v-for="review in reviews" :key="review.id" class="col-md-6">
                <ReviewComponent :review="review" />
              </div>
            </div>
          </div>

          <div v-if="favorites.length === 0" class="alert alert-info mt-3">
            <i class="bi bi-star me-2"></i>
            No has agregado ningún favorito aún.
          </div>
          <div v-else>
            <h3 class="h4 mb-3 mt-4">
              <router-link to="/mis-favoritos" class="text-decoration-none">Mis Favoritos Recientes</router-link>
            </h3>
            <div class="row g-3">
              <div v-for="favorite in favorites" :key="favorite.id" class="col-md-6">
                <SiteCard :site="favorite" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useSessionStore } from "@/stores/sessionStore"
import { useReviewsStore } from '@/stores/reviewsStore'
import { fetchSites } from '@/api/sites'
import ReviewComponent from '@/components/ReviewComponent.vue'
import SiteCard from '@/components/SiteCard.vue'

const sessionStore = useSessionStore()
const reviewsStore = useReviewsStore()

const user = sessionStore.user
const reviews = reviewsStore.reviews.slice(0, 3)
const favorites = ref([])

// Cargar favoritos desde la API
onMounted(async () => {
  try {
    const response = await fetchSites({
      sort: 'favorites',
      limit: 3,
    })
    favorites.value = response.sites
  } catch (error) {
    console.error('Error al cargar favoritos:', error)
  }
})


</script>