<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section bg-light border-bottom">
      <div class="container py-5">
        <div class="row justify-content-center">
          <div class="col-lg-8 text-center">
            <h1 class="display-4 fw-bold mb-3">Explora el Patrimonio Histórico Nacional</h1>
            <p class="lead text-muted mb-4">
              Descubre sitios históricos, monumentos y espacios de valor cultural de todo el país.
            </p>
            <div class="mx-auto" style="max-width: 600px;">
              <HeroSearch />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Sections -->
    <div class="container py-5">
      <!-- Top Rated Section -->
      <FeaturedSection
        section-id="top-rated"
        title="Mejor Puntuados"
        description="Destinos con mejor calificación amados por los visitantes"
        sort-by="top-rated"
      />

      <hr class="my-5" />

      <!-- Most Visited Section -->
      <FeaturedSection
        section-id="most-visited"
        title="Más Visitados"
        description="Sitios populares que están en tendencia ahora"
        sort-by="most-visited"
      />

      <hr class="my-5" />

      <!-- Recently Added Section -->
      <FeaturedSection
        section-id="recently-added"
        title="Recientemente Agregados"
        description="Nuevos lugares por descubrir"
        sort-by="recently-added"
      />

      <!-- Favorites Section - Only visible when logged in -->
      <template v-if="isAuthenticated">
        <hr class="my-5" />
        <FeaturedSection
          section-id="favorites"
          title="Tus Favoritos"
          description="Sitios que has guardado para después"
          sort-by="favorites"
          :show-if-empty="false"
          :require-auth="true"
        />
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HeroSearch from '../components/HeroSearch.vue'
import FeaturedSection from '../components/FeaturedSection.vue'

// TODO: Implementar lógica de autenticación
// Por ahora, simular estado de autenticación
const isAuthenticated = ref(false)
</script>

<style scoped>
.hero-section {
  background: linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%);
}

.home-page {
  min-height: 100vh;
  background-color: #ffffff;
}
</style>
