<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section bg-light border-bottom">
      <!-- container: centra el contenido con ancho máximo responsivo -->
      <div class="container py-5">
        <!-- row: crea una fila flexbox, justify-content-center: centra horizontalmente el contenido -->
        <div class="row justify-content-center">
          <!-- col-lg-8: ocupa 8/12 columnas en pantallas grandes, text-center: alinea el texto al centro -->
          <div class="col-lg-8 text-center">
            <h1 class="display-4 fw-bold mb-3">Explora el Patrimonio Histórico Nacional</h1>
            <p class="lead text-muted mb-4">
              Descubre sitios históricos, monumentos y espacios de valor cultural de todo el país.
            </p>
            <!-- mx-auto: centra horizontalmente el elemento con margen automático -->
            <div class="mx-auto" style="max-width: 600px;">
              <HeroSearch />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Sections -->
    <!-- container: centra el contenido, py-5: padding vertical 5 -->
    <div class="container py-5">
      <template v-if="isAuthenticated">
        <FeaturedSection
          section-id="favorites"
          title="Tus Favoritos"
          description="Sitios que has guardado para después"
          order-by="registration_date"
          order-dir="desc"
          :show-if-empty="false"
          :require-auth="true"
        />

        <hr class="my-5" />
      </template>

      <!-- Top Rated Section -->
      <FeaturedSection
        section-id="top-rated"
        title="Mejor Puntuados"
        description="Destinos con mejor calificación amados por los visitantes"
        order-by="rating"
        order-dir="desc"
      />

      <hr class="my-5" />

      <!-- Recently Added Section -->
      <FeaturedSection
        section-id="recently-added"
        title="Recientemente Agregados"
        description="Nuevos lugares por descubrir"
        order-by="registration_date"
        order-dir="desc"
      />
    </div>
  </div>
</template>

<script setup>
import { useSessionStore } from '@/stores/sessionStore'
import { storeToRefs } from 'pinia'
import HeroSearch from '../components/HeroSearch.vue'
import FeaturedSection from '../components/FeaturedSection.vue'

const sessionStore = useSessionStore()
const { isAuthenticated } = storeToRefs(sessionStore)
</script>

<style scoped>
.hero-section {
  /* background: gradiente lineal de gris claro a blanco */
  background: linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%);
}

.home-page {
  /* min-height: altura mínima del 100% del viewport */
  min-height: 100vh;
  background-color: #ffffff;
}
</style>
