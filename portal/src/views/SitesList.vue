<template>
  <div class="sites-list-page">
    <div class="container py-5">
      <div class="row mb-4">
        <div class="col">
          <h1 class="h2 fw-bold">Explorar Sitios</h1>
          <p v-if="searchQuery" class="text-muted">
            Resultados para: <strong>{{ searchQuery }}</strong>
          </p>
          <p v-else-if="orderBy" class="text-muted">
            Ordenado por: <strong>{{ getOrderByLabel(orderBy) }}</strong>
          </p>
          <p v-else class="text-muted">
            Sitios históricos ordenados por fecha de registro
          </p>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="row g-4">
        <div v-for="i in 6" :key="i" class="col-12 col-md-6 col-lg-4">
          <div class="card placeholder-glow">
            <div class="placeholder col-12" style="height: 200px;"></div>
            <div class="card-body">
              <span class="placeholder col-6"></span>
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

      <!-- Empty -->
      <div v-else class="text-center py-5">
        <i class="bi bi-inbox display-1 text-muted"></i>
        <h4 class="mt-3">No se encontraron sitios</h4>
        <p class="text-muted">Intenta ajustar tu búsqueda</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSitesStore } from '@/stores/sitesStore'
import SiteCard from '../components/SiteCard.vue'

const route = useRoute()
const sitesStore = useSitesStore()
const sites = ref([])
const loading = ref(true)
const searchQuery = ref('')
const orderBy = ref(undefined)

const getOrderByLabel = (order) => {
  const labels = {
    'rating-5-1': 'Mejor Puntuados',
    'rating-1-5': 'Peor Puntuados',
    'latest': 'Recientemente Agregados',
    'oldest': 'Más Antiguos',
  }
  return labels[order] || 'Sin ordenar'
}

const loadSites = async () => {
  loading.value = true
  try {
    searchQuery.value = route.query.search || ''
    orderBy.value = route.query.order_by || undefined

    const response = await sitesStore.fetchSites({
      search: searchQuery.value,
      order_by: orderBy.value,
    })

    sites.value = response.sites
  } catch (err) {
    console.error('[SitesList] Error:', err)
  } finally {
    loading.value = false
  }
}

onMounted(loadSites)
watch(() => route.query, loadSites)
</script>

<style scoped>
.sites-list-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}
</style>
