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
          <p v-else class="text-muted">Sitios históricos ordenados por fecha de registro</p>
        </div>
      </div>

      <CAccordion class="mb-4">
        <CAccordionItem :item-key="1">
          <CAccordionHeader> Filtros y ordenamientos </CAccordionHeader>
          <CAccordionBody>
            <CAccordion class="mb-4">
              <CAccordionItem :item-key="2" @click="renderMap">
                <CAccordionHeader> Mapa interactivo </CAccordionHeader>
                <CAccordionBody>
                  <div v-if="mapShouldRender" class="map-container mb-4">
                    <LeafletMap
                      :markers="markers"
                      :initialParams="mapParams"
                      @update-map-params="handleMapSearch"
                    />
                  </div>
                </CAccordionBody>
              </CAccordionItem>
            </CAccordion>
            <div class="row g-3">
              <!-- Búsqueda -->
              <div class="col-12">
                <label for="searchInput" class="form-label">Buscar sitio</label>
                <input
                  id="searchInput"
                  v-model="filterForm.search"
                  type="text"
                  class="form-control"
                  placeholder="Buscar por nombre o descripción corta..."
                />
              </div>

              <!-- Ordenamiento -->
              <div class="col-md-6">
                <label for="orderBySelect" class="form-label">Ordenar por</label>
                <div class="input-group">
                  <select id="orderBySelect" v-model="filterForm.orderBy" class="form-select">
                    <option value="registration_date">Fecha de registro</option>
                    <option value="site_name">Nombre</option>
                    <option value="rating">Calificación</option>
                  </select>
                  <button
                    type="button"
                    class="btn btn-outline-secondary"
                    @click="toggleOrder"
                    :disabled="!filterForm.orderBy"
                    :title="filterForm.orderDir === 'asc' ? 'Ascendente' : 'Descendente'"
                  >
                    <i
                      :class="filterForm.orderDir === 'asc' ? 'bi bi-sort-up' : 'bi bi-sort-down'"
                    ></i>
                  </button>
                </div>
              </div>

              <!-- Búsqueda por ciudad -->
              <div class="col-md-6">
                <label for="citySearchInput" class="form-label">Ciudad</label>
                <input
                  id="citySearchInput"
                  v-model="filterForm.citySearch"
                  type="text"
                  class="form-control"
                  placeholder="Ej.: La Plata"
                />
              </div>

              <!-- Selector de provincia -->
              <div class="col-md-6">
                <label for="provinceSelect" class="form-label">Provincia</label>
                <div class="input-group">
                  <select id="provinceSelect" v-model="filterForm.province" class="form-select">
                    <option :value="undefined">Todas las provincias</option>
                    <option value="Buenos Aires">Buenos Aires</option>
                    <option value="Catamarca">Catamarca</option>
                    <option value="Chaco">Chaco</option>
                    <option value="Chubut">Chubut</option>
                    <option value="Córdoba">Córdoba</option>
                    <option value="Corrientes">Corrientes</option>
                    <option value="Entre Ríos">Entre Ríos</option>
                    <option value="Formosa">Formosa</option>
                    <option value="Jujuy">Jujuy</option>
                    <option value="La Pampa">La Pampa</option>
                    <option value="La Rioja">La Rioja</option>
                    <option value="Mendoza">Mendoza</option>
                    <option value="Misiones">Misiones</option>
                    <option value="Neuquén">Neuquén</option>
                    <option value="Río Negro">Río Negro</option>
                    <option value="Salta">Salta</option>
                    <option value="San Juan">San Juan</option>
                    <option value="San Luis">San Luis</option>
                    <option value="Santa Cruz">Santa Cruz</option>
                    <option value="Santa Fe">Santa Fe</option>
                    <option value="Santiago del Estero">Santiago del Estero</option>
                    <option value="Tierra del Fuego">Tierra del Fuego</option>
                    <option value="Tucumán">Tucumán</option>
                  </select>
                </div>
              </div>

              <!-- Multiselector de etiquetas -->
              <div class="col-md-6">
                <label class="form-label">Etiquetas</label>
                <Multiselect
                  v-model="filterForm.selectedTags"
                  :options="tags"
                  :multiple="true"
                  :close-on-select="false"
                  placeholder="Selecciona etiquetas"
                  select-label="Presiona enter para seleccionar"
                  diselect-label="Presiona enter para quitar"
                  label="name"
                  track-by="id"
                />
              </div>

              <div v-if="isAuthenticated" class="col-md-6">
                <div class="form-check">
                  <input
                    id="favoritesCheckbox"
                    v-model="filterForm.favorites"
                    type="checkbox"
                    class="form-check-input"
                  />
                  <label for="favoritesCheckbox" class="form-check-label">
                    Mostrar solo mis favoritos
                  </label>
                </div>
              </div>

              <!-- Botones -->
              <div class="col-12 d-flex gap-2">
                <button @click="applyFilters" class="btn btn-primary">
                  <i class="bi bi-funnel"></i> Aplicar Filtros
                </button>
                <button @click="clearFilters" class="btn btn-outline-secondary">
                  <i class="bi bi-x-circle"></i> Limpiar
                </button>
              </div>
            </div>
          </CAccordionBody>
        </CAccordionItem>
      </CAccordion>

      <!-- Loading -->
      <div v-if="loading" class="row g-4">
        <div v-for="i in 6" :key="i" class="col-12 col-md-6 col-lg-4">
          <div class="card placeholder-glow">
            <div class="placeholder col-12" style="height: 200px"></div>
            <div class="card-body">
              <span class="placeholder col-6"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Sites Grid -->
      <div v-else-if="sites.length > 0" class="row g-4">
        <div v-for="site in sites" :key="site.id" class="col-12 col-md-6 col-lg-4">
          <SiteCard :site="site">
            <span :class="stateConfig(site).classes" class="badge rounded-pill mb-4">
              <i :class="stateConfig(site).icon"></i>
              {{ site.state }}
            </span>
            <TagList :tags="site.tags" />
          </SiteCard>
        </div>

        <!-- Pagination -->
        <PaginationComponent
          :current-page="currentPage"
          :total-pages="totalPages"
          :loading="loading"
          @page-change="handlePageChange"
        />
      </div>

      <!-- Empty -->
      <div v-else class="text-center py-5">
        <i class="bi bi-inbox display-1 text-muted"></i>
        <h4 class="mt-3">No se encontraron sitios</h4>
        <p class="text-muted">Intenta ajustar tu búsqueda</p>
      </div>
    </div>

    <CToast
      v-if="showErrorToast"
      :visible="showErrorToast"
      @close="showErrorToast = false"
      color="danger"
      class="position-fixed top-0 end-0 m-3"
      style="z-index: 9999"
    >
      <CToastHeader closeButton>
        <strong class="me-auto">Error de búsqueda</strong>
      </CToastHeader>
      <CToastBody>
        <i class="bi bi-exclamation-triangle-fill me-2"></i>
        {{ errorMessage }}
      </CToastBody>
    </CToast>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, reactive, toRaw, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Multiselect } from 'vue-multiselect'
import 'vue-multiselect/dist/vue-multiselect.css'
import { CAccordion, CAccordionHeader, CAccordionBody, CAccordionItem, CToast, CToastBody, CToastHeader } from '@coreui/vue'
import { useSitesStore } from '@/stores/sitesStore'
import SiteCard from '../components/SiteCard.vue'
import PaginationComponent from '@/components/PaginationComponent.vue'
import TagList from '@/components/TagList.vue'
import api from '@/service/api'
import { useSessionStore } from '@/stores/sessionStore'
import LeafletMap from '@/components/LeafletMap.vue'

const route = useRoute()
const router = useRouter()
const sitesStore = useSitesStore()
const sites = ref([])
const tags = ref([])
const loading = ref(true)
const searchQuery = ref('')
const orderBy = ref(undefined)
const orderDir = ref('desc')
const city = ref('')
const province = ref(undefined)
const selectedTags = ref([])
const favorites = ref(false)
const lat = ref(undefined)
const long = ref(undefined)
const radius = ref(undefined)
const currentPage = ref(1)
const totalPages = ref(1)
const markers = ref([])
const mapParams = ref(undefined)
const mapZoom = ref(16)
const errorMessage = ref('')
const showErrorToast = ref(false)

// Construye un diccionario reactivo (dinámico con v-model)
const filterForm = reactive({
  search: '',
  orderBy: 'registration_date',
  orderDir: 'desc',
  citySearch: '',
  province: undefined,
  selectedTags: [],
  favorites: false,
  lat: undefined,
  long: undefined,
  radius: undefined,
})

const handleMapSearch = ({lat, long, radius, zoom}) => {
  filterForm.lat = lat
  filterForm.long = long
  filterForm.radius = radius
  mapZoom.value = zoom

}

const toggleOrder = () => {
  filterForm.orderDir = filterForm.orderDir === 'asc' ? 'desc' : 'asc'
}

// Navega a la ruta definida de nombre 'sites' con los parámetros indicados. Dispara el watch de route.query
const applyFilters = () => {
  router.push({
    name: 'sites',
    query: {
      search: filterForm.search || undefined,
      order_by: filterForm.orderBy || undefined,
      order_dir: filterForm.orderBy ? filterForm.orderDir : undefined,
      city: filterForm.citySearch || undefined,
      province: filterForm.province || undefined,
      tags: filterForm.selectedTags.map((tag) => tag.id) || [],
      favorites: filterForm.favorites || undefined,
      lat: filterForm.lat || undefined,
      long: filterForm.long || undefined,
      radius: filterForm.radius || undefined,
    },
  })

  localStorage.setItem('mapZoom', mapZoom.value.toString())
}

const clearFilters = () => {
  filterForm.search = ''
  filterForm.orderBy = 'registration_date'
  filterForm.orderDir = undefined
  filterForm.citySearch = ''
  filterForm.province = undefined
  filterForm.selectedTags = []
  filterForm.favorites = false
  filterForm.lat = undefined
  filterForm.long = undefined
  filterForm.radius = undefined

  localStorage.removeItem('mapZoom')
  router.push({ name: 'sites' })
}

const getOrderByLabel = (order) => {
  const labels = {
    registration_date: 'Fecha de registro',
    site_name: 'Nombre',
    rating: 'Calificación',
  }
  return labels[order] || 'Sin ordenar'
}

// Maneja el cambio de página desde el componente de paginación
const handlePageChange = async (page) => {
  currentPage.value = page
  await loadSites()
  setTimeout(() => {
    window.scrollTo(0, 0)
  }, 50)
}

const loadSites = async () => {
  loading.value = true
  try {
    searchQuery.value = route.query.search || ''
    orderBy.value = route.query.order_by || 'registration_date'
    orderDir.value = route.query.order_dir || 'desc'
    city.value = route.query.city || ''
    province.value = route.query.province || ''
    favorites.value = route.query.favorites || undefined
    selectedTags.value = route.query.tags || []
    lat.value = route.query.lat || undefined
    long.value = route.query.long || undefined
    radius.value = route.query.radius || undefined

    const response = await sitesStore.fetchSites({
      search: searchQuery.value,
      order_by: orderBy.value,
      order_dir: orderDir.value,
      city: city.value,
      province: province.value,
      favorites: favorites.value,
      tags: toRaw(selectedTags.value),
      lat: lat.value,
      long: long.value,
      radius: radius.value,
      page: currentPage.value,
      per_page: 25,
    })

    sites.value = response.sites
    totalPages.value = Math.ceil(response.total / response.per_page)

    markers.value = sites.value.map(site => ({
      id: site.id,
      lat: site.lat,
      lon: site.long,
      title: site.name,
      description: site.short_description,
      coverImage: site.coverImage,
    }))
  } catch (err) {
    console.error('[SitesList] Error:', err)

    if (err?.status === 400) {
      errorMessage.value = 'Los valores de coordenadas y/o radio exceden los permitidos. Por favor, ajusta el área de búsqueda.'
      // Limpia los parámetros del mapa
      filterForm.lat = undefined
      filterForm.long = undefined
      filterForm.radius = undefined
      mapParams.value = undefined
    } else {
      errorMessage.value = 'Error al cargar los sitios. Intenta nuevamente.'
    }

    showErrorToast.value = true

    setTimeout(() => {
      showErrorToast.value = false
    }, 10000)
  } finally {
    loading.value = false
  }
}

// Maneja cambios en los parámetros de consulta
const handleQueryChange = () => {
  currentPage.value = 1
  loadSites()
}

onMounted(async () => {
  filterForm.search = route.query.search || ''
  filterForm.orderBy = route.query.order_by || 'registration_date'
  filterForm.orderDir = route.query.order_dir || undefined
  filterForm.citySearch = route.query.city || undefined
  filterForm.province = route.query.province || undefined
  filterForm.favorites = route.query.favorites === 'true'
  filterForm.lat = route.query.lat || undefined
  filterForm.long = route.query.long || undefined
  filterForm.radius = route.query.radius || undefined

  await fetchTags()

  const tagsIds = route.query.tags
    ? Array.isArray(route.query.tags)
      ? route.query.tags
      : [route.query.tags]
    : []
  filterForm.selectedTags = tags.value.filter((tag) => tagsIds.includes(String(tag.id)))

  const savedZoom = localStorage.getItem('mapZoom')
  mapZoom.value = savedZoom ? Number(savedZoom) : 16

  mapParams.value = {
    lat: route.query.lat || undefined,
    long: route.query.long || undefined,
    radius: route.query.radius || undefined,
    zoom: mapZoom.value,
  }

  await loadSites()
})

const fetchTags = async () => {
  const response = await api.get('/api/tags')
  tags.value = response.data.map((tag) => ({
    id: tag.id,
    name: tag.name,
  }))
}

watch(() => route.query, handleQueryChange)

const sessionStore = useSessionStore()
const isAuthenticated = ref(sessionStore.isAuthenticated)

// Observar cambios en la autenticación
watchEffect(() => {
  isAuthenticated.value = sessionStore.isAuthenticated
})

// Configuración de clase para etiqueta de estado de sitio
function stateConfig(site) {
  const configMap = {
    Bueno: {
      classes: 'bg-success text-white',
      icon: 'bi bi-check-circle-fill',
    },
    Regular: {
      classes: 'bg-warning text-dark',
      icon: 'bi bi-exclamation-triangle-fill',
    },
    Malo: {
      classes: 'bg-danger text-white',
      icon: 'bi bi-x-circle-fill',
    },
  }
  return (
    configMap[site.state] || {
      classes: 'bg-secondary text-white',
      icon: 'bi bi-question-circle-fill',
    }
  )
}

const mapShouldRender = ref(false)
const renderMap = () => {
  if(!mapShouldRender.value) {
    mapShouldRender.value = true
  }
}
</script>

<style scoped>
.sites-list-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.map-container {
  position: relative;
  width: 100%;
  max-width: 100%;
  overflow: hidden;
  z-index: 1;
}

/* Asegurar que el mapa no se superponga */
.map-container :deep(#map) {
  position: relative !important;
  width: 100%;
  height: 600px !important;
}
</style>
