<template>
  <div class="sites-list-page">
    <div class="container py-5">
      <div class="row mb-4">
        <div class="col">
          <h1 class="h2 fw-bold">Explorar Sitios</h1>
          <p class="text-muted" v-if="searchQuery">
            Resultados de búsqueda para: <strong>{{ searchQuery }}</strong>
          </p>
          <p class="text-muted" v-else-if="sortBy">
            Ordenado por: <strong>{{ getSortLabel(sortBy) }}</strong>
          </p>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="row g-4">
        <div v-for="i in 6" :key="i" class="col-12 col-md-6 col-lg-4">
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

      <!-- Sites Grid -->
      <div v-else-if="sites.length > 0" class="row g-4">
        <div v-for="site in sites" :key="site.id" class="col-12 col-md-6 col-lg-4">
          <SiteCard :site="site" />
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-5">
        <i class="bi bi-inbox display-1 text-muted"></i>
        <h4 class="mt-3">No se encontraron sitios</h4>
        <p class="text-muted">Intenta ajustar tu búsqueda o filtros</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { fetchSites } from '../api/sites'
import SiteCard from '../components/SiteCard.vue'

const route = useRoute()
const sites = ref([])
const loading = ref(true)
const searchQuery = ref('')
const sortBy = ref(undefined)

const getSortLabel = (sort) => {
  const labels = {
    'top-rated': 'Mejor Puntuados',
    'most-visited': 'Más Visitados',
    'recently-added': 'Recientemente Agregados',
    'favorites': 'Favoritos',
  }
  return labels[sort]
}

const loadSites = async () => {
  try {
    loading.value = true
    searchQuery.value = route.query.search || ''
    sortBy.value = route.query.sort || undefined

    const response = await fetchSites({
      search: searchQuery.value,
      sort: sortBy.value,
    })

    sites.value = response.sites
  } catch (err) {
    console.error('[SitesList] Error loading sites:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadSites()
})

watch(() => route.query, () => {
  loadSites()
})
</script>

<style scoped>
.sites-list-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}
</style>
