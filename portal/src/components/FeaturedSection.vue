<template>
  <section class="featured-section">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-start mb-4">
      <div>
        <h2 class="h3 fw-bold mb-1">{{ title }}</h2>
        <p v-if="description" class="text-muted mb-0">{{ description }}</p>
      </div>
      <router-link
        v-if="!loading && sites.length > 0"
        :to="{ name: 'sites', query: { sort: sortBy } }"
        class="btn btn-outline-secondary d-none d-md-flex align-items-center"
      >
        Ver todos
        <i class="bi bi-arrow-right ms-2"></i>
      </router-link>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="row g-3">
      <div v-for="i in 3" :key="i" class="col-12 col-md-6 col-lg-4">
        <div class="card">
          <div class="placeholder-glow">
            <div class="placeholder col-12" style="height: 200px;"></div>
          </div>
          <div class="card-body">
            <h5 class="card-title placeholder-glow">
              <span class="placeholder col-6"></span>
            </h5>
            <p class="card-text placeholder-glow">
              <span class="placeholder col-8"></span>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="alert alert-danger" role="alert">
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ error }}
    </div>

    <!-- Empty State -->
    <div v-else-if="sites.length === 0 && showIfEmpty" class="text-center py-5">
      <i class="bi bi-inbox display-1 text-muted"></i>
      <h4 class="mt-3">No se encontraron sitios</h4>
      <p class="text-muted">Vuelve más tarde para ver nuevo contenido</p>
    </div>

    <!-- Sites Grid/Carousel -->
    <div v-else-if="sites.length > 0">
      <!-- Mobile: Carousel -->
      <div class="d-md-none">
        <div :id="`carousel-${sectionId}`" class="carousel slide" data-bs-ride="false">
          <div class="carousel-inner">
            <div
              v-for="(site, index) in sites"
              :key="site.id"
              class="carousel-item"
              :class="{ active: index === 0 }"
            >
              <div class="px-2">
                <SiteCard :site="site" />
              </div>
            </div>
          </div>
          <button
            class="carousel-control-prev"
            type="button"
            :data-bs-target="`#carousel-${sectionId}`"
            data-bs-slide="prev"
          >
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Anterior</span>
          </button>
          <button
            class="carousel-control-next"
            type="button"
            :data-bs-target="`#carousel-${sectionId}`"
            data-bs-slide="next"
          >
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Siguiente</span>
          </button>
        </div>
      </div>

      <!-- Desktop: Grid -->
      <div class="row g-4 d-none d-md-flex">
        <div v-for="site in sites" :key="site.id" class="col-md-6 col-lg-4">
          <SiteCard :site="site" />
        </div>
      </div>

      <!-- Mobile View All Button -->
      <div class="d-md-none text-center mt-4">
        <router-link
          :to="{ name: 'sites', query: { sort: sortBy } }"
          class="btn btn-outline-secondary"
        >
          Ver todos
          <i class="bi bi-arrow-right ms-2"></i>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchSites } from '../api/sites'
import SiteCard from './SiteCard.vue'

const props = defineProps({
  sectionId: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  description: {
    type: String,
    default: ''
  },
  sortBy: {
    type: String,
    required: true
  },
  showIfEmpty: {
    type: Boolean,
    default: true
  },
  requireAuth: {
    type: Boolean,
    default: false
  }
})

const sites = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    loading.value = true
    error.value = null

    const response = await fetchSites({
      sort: props.sortBy,
      limit: 6,
    })

    sites.value = response.sites
  } catch (err) {
    console.error('[Featured] Error loading sites:', err)
    error.value = 'Error al cargar los sitios'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.featured-section {
  margin-bottom: 3rem;
}

.carousel-control-prev,
.carousel-control-next {
  width: 40px;
  height: 40px;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  opacity: 0.8;
}

.carousel-control-prev {
  left: -20px;
}

.carousel-control-next {
  right: -20px;
}

.carousel-control-prev:hover,
.carousel-control-next:hover {
  opacity: 1;
}
</style>
