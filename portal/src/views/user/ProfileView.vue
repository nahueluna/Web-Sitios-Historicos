<template>
  <!-- container: centra el contenido, py-5: padding vertical 5 -->
  <div class="container py-5">
    <!-- row: fila flexbox, justify-content-center: centra horizontalmente -->
    <div class="row justify-content-center">
      <!-- col-lg-8: ocupa 8/12 columnas en pantallas grandes -->
      <div class="col-lg-8">
        <!-- card: componente de tarjeta, shadow-sm: sombra pequeña -->
        <div class="card shadow-sm">
          <!-- card-body: cuerpo de la tarjeta, text-center: texto centrado -->
          <div class="card-body text-center">
            <!-- rounded-circle: imagen circular, mb-3: margen inferior 3 -->
            <img :src="user.picture" alt="Foto de perfil" class="rounded-circle mb-3" width="100" height="100">
            <h1 class="h3 mb-1">Bienvenido, {{ user.name }}</h1>
            <p class="text-muted">{{ user.email }}</p>

            <!-- LOGOUT COMPONENT -->
            <GoogleLogout />

          </div>
        </div>

        <!-- card: tarjeta, mt-4: margen superior 4 -->
        <div class="card shadow-sm mt-4">
          <div class="card-body">
            <h2 class="h4 mb-3">Información de la Sesión</h2>
            <ul class="list-unstyled">
              <li><strong>Correo Electrónico:</strong> {{ user.email }}</li>
              <li><strong>Nombre Completo:</strong> {{ user.name }} {{ user.lastname }}</li>
            </ul>
          </div>
        </div>

        <!-- mt-4: margen superior 4 -->
        <div class="mt-4">
          <div v-if="reviews.length === 0" class="alert alert-info">
            <!-- me-2: margen derecho 2 -->
            <i class="bi bi-info-circle me-2"></i>
            No has escrito ninguna reseña aún.
          </div>
          <div v-else>
            <!-- d-flex: display flexbox, justify-content-between: distribuye espacio entre elementos, align-items-start: alinea al inicio verticalmente, mb-4: margen inferior 4 -->
            <div class="d-flex justify-content-between align-items-start mb-4">
              <div>
                <h2 class="h4 mb-1">Mis Reseñas Recientes</h2>
                <p class="text-muted mb-0">Reseñas que has escrito recientemente</p>
              </div>
              <!-- d-none d-md-flex: oculto en móvil, flex en tablet/desktop, align-items-center: centra verticalmente -->
              <router-link to="/mis-reseñas" class="btn btn-outline-secondary d-none d-md-flex align-items-center">
                Ver todos
                <!-- ms-2: margen izquierdo 2 -->
                <i class="bi bi-arrow-right ms-2"></i>
              </router-link>
            </div>
            <!-- Listado de reseñas recientes -->
            <div class="row g-3">
              <div v-for="review in reviews.slice(0, 4)" :key="review.id" class="col-md-6 col-lg-4">
                <ReviewComponent :review="review" />
              </div>
            </div>
            <!-- d-md-none: visible solo en móvil, text-center: texto centrado, mt-4: margen superior 4 -->
            <div class="d-md-none text-center mt-4">
              <router-link to="/mis-reseñas" class="btn btn-outline-secondary">
                Ver todos
                <i class="bi bi-arrow-right ms-2"></i>
              </router-link>
            </div>
          </div>

          <div v-if="favorites.length === 0" class="alert alert-info">
            <i class="bi bi-info-circle me-2"></i>
            No has agregado ningún favorito aún.
          </div>
          <div v-else>
            <div class="d-flex justify-content-between align-items-start mb-4 mt-4">
              <div>
                <h3 class="h4 mb-1">Mis Favoritos Recientes</h3>
                <p class="text-muted mb-0">Lugares que has marcado como favoritos recientemente</p>
              </div>
              <router-link to="/favorites" class="btn btn-outline-secondary d-none d-md-flex align-items-center">
                Ver todos
                <i class="bi bi-arrow-right ms-2"></i>
              </router-link>
            </div>

            <div class="row g-3">
              <div v-for="favorite in favorites" :key="favorite.id" class="col-md-6">
                <SiteCard :site="favorite" />
              </div>
            </div>

            <div class="d-md-none text-center mt-4">
              <router-link to="/favorites" class="btn btn-outline-secondary">
                Ver todos
                <i class="bi bi-arrow-right ms-2"></i>
              </router-link>
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
import { useProfileReviewStore } from '@/stores/profileReviewStore'
import { useFavoritesStore } from '@/stores/profileFavoriteStore'
import ReviewComponent from '@/components/ReviewComponent.vue'
import SiteCard from '@/components/SiteCard.vue'
import GoogleLogout from '@/components/google/GoogleLogoutComponent.vue'


const sessionStore = useSessionStore()
const profileReviewStore = useProfileReviewStore()
const profileFavoritesStore = useFavoritesStore()

const user = sessionStore.user
const reviews = ref([])
const favorites = ref([])

onMounted(async () => {
  reviews.value = await profileReviewStore.loadRecentReviews(user.id) 
  favorites.value = await profileFavoritesStore.loadRecentFavorites() 
  //reviews.value = profileReviewStore.getHardcodedReviews() // --> descomentar para testear
  // favorites.value = favoritesStore.getHardcodedFavorites() // --> descomentar para testear
})

</script>