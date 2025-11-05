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
            <h3 class="h4 mb-3">
              <router-link to="/reviews" class="text-decoration-none">Mis Reseñas Recientes</router-link>
            </h3>
            <div class="row g-3">
              <div v-for="review in reviews" :key="review.id" class="col-md-6">
                <ReviewComponent :review="review" />
              </div>
              <!-- d-none d-md-flex: oculto en móvil, flex en tablet/desktop, align-items-center: centra verticalmente -->
              <router-link to="/mis-reseñas" class="btn btn-outline-secondary d-none d-md-flex align-items-center">
                Ver todos
                <!-- ms-2: margen izquierdo 2 -->
                <i class="bi bi-arrow-right ms-2"></i>
              </router-link>
            </div>
            <!-- row: fila flexbox, g-3: gap 3 entre elementos -->
            <div class="row g-3">
              <!-- col-md-6: 6/12 columnas en medium y arriba -->
              <div v-for="review in reviews" :key="review.id" class="col-md-6">
                <!-- REVIEW COMPONENT -->
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

<<<<<<< HEAD
          <div v-if="favorites.length === 0" class="alert alert-info mt-3">
            <i class="bi bi-star me-2"></i>
            No has agregado ningún favorito aún.
          </div>
          <div v-else>
            <h3 class="h4 mb-3 mt-4">
              <router-link to="/favorites" class="text-decoration-none">Mis Favoritos Recientes</router-link>
            </h3>
            <div class="row g-3">
              <div v-for="favorite in favorites" :key="favorite.id" class="col-md-6">
                <SiteCard :site="favorite" />
              </div>
            </div>
          </div>
=======
          <FeaturedSection
            section-id="profile-favorites"
            title="Mis Favoritos Recientes"
            description="Sitios que has guardado para después"
            order-by="latest"
            :show-if-empty="false"
          />
>>>>>>> feature/resenas-y-calificaciones
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useSessionStore } from "@/stores/sessionStore"
import { useReviewsStore } from '@/stores/reviewsStore'
import ReviewComponent from '@/components/ReviewComponent.vue'
import GoogleLogout from '@/components/google/GoogleLogoutComponent.vue'
import FeaturedSection from '@/components/FeaturedSection.vue'

const sessionStore = useSessionStore()
const reviewsStore = useReviewsStore()

const user = sessionStore.user
const reviews = computed(() => {
  if (!sessionStore.user) return []
  return reviewsStore.getReviewsByUser(sessionStore.user.id).slice(0, 3)
})


</script>