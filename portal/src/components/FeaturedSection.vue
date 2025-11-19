<template>
  <section class="featured-section">
    <!-- Header -->
    <!-- d-flex: display flexbox, justify-content-between: espacio entre elementos, align-items-start: alinea al inicio verticalmente, mb-4: margen inferior 4 -->
    <div class="d-flex justify-content-between align-items-start mb-4">
      <div>
        <h2 class="h3 fw-bold mb-1">{{ title }}</h2>
        <p v-if="description" class="text-muted mb-0">{{ description }}</p>
      </div>
      <!-- d-none d-md-flex: oculto en móvil, flex en tablet+, align-items-center: centra verticalmente -->
      <router-link
        v-if="!loading && sites &&  sites.length > 0"
        :to="{ name: 'sites', query: { order_by: orderBy, ...(props.sectionId === 'favorites' ? { favorites: true } : {}) } }"
        class="btn btn-outline-secondary d-none d-md-flex align-items-center"
      >
        Ver todos
        <!-- ms-2: margen izquierdo 2 -->
        <i class="bi bi-arrow-right ms-2"></i>
      </router-link>
    </div>

    <!-- Loading State -->
    <!-- row: fila flexbox, g-3: gap 3 -->
    <div v-if="loading" class="row g-3">
      <!-- col-12 col-md-6 col-lg-4: columnas responsivas (12 en móvil, 6 en tablet, 4 en desktop) -->
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
      <!-- me-2: margen derecho 2 -->
      <i class="bi bi-exclamation-triangle me-2"></i>
      {{ error }}
    </div>

    <!-- Empty State -->
    <!-- text-center: texto centrado, py-5: padding vertical 5 -->
    <div v-else-if="sites && sites.length === 0 && showIfEmpty" class="text-center py-5">
      <i class="bi bi-inbox display-1 text-muted"></i>
      <h4 class="mt-3">No se encontraron sitios</h4>
      <p class="text-muted">Vuelve más tarde para ver nuevo contenido</p>
    </div>

    <!-- Sites Grid/Carousel -->
    <div v-else-if="sites && sites.length > 0">
      <!-- Mobile: Carousel -->
      <!-- d-md-none: visible solo en móvil
        d: display
        md: medium devices (a partir de dispositivos medianos (768px))
        none: ninguno
      -->
      <div class="d-md-none">
        <div :id="`carousel-${sectionId}`" class="carousel slide" data-bs-ride="false">
          <div class="carousel-inner">
            <div
              v-for="(site, index) in sites"
              :key="site.id"
              class="carousel-item"
              :class="{ active: index === 0 }"
            >
              <!-- px-2: padding horizontal 2 -->
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
            <!-- visually-hidden: oculto visualmente pero accesible para lectores de pantalla -->
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
      <!-- row: fila flexbox, g-4: gap 4, d-none d-md-flex: oculto en móvil, flex en tablet+ -->
      <div class="row g-4 d-none d-md-flex">
        <!-- col-md-6 col-lg-4: 6 columnas en tablet, 4 en desktop -->
        <div v-for="site in sites" :key="site.id" class="col-md-6 col-lg-4">
          <SiteCard :site="site" />
        </div>
      </div>

      <!-- Mobile View All Button -->
      <!-- d-md-none: visible solo en móvil, text-center: texto centrado, mt-4: margen superior 4 -->
      <div class="d-md-none text-center mt-4">
        <router-link
          :to="{ name: 'sites', query: { order_by: orderBy, ...(props.sectionId === 'favorites' ? { favorites: true } : {}) } }"
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
import { useSitesStore } from '@/stores/sitesStore'
import { useSessionStore } from '@/stores/sessionStore'
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
  orderBy: {
    type: String,
    required: true,
    validator: (value) => ['rating', 'registration_date', 'site_name'].includes(value)
  },
  orderDir: {
    type: String,
    required: true,
    validator: (value) => ['desc', 'asc'].includes(value),
    default: 'desc'
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

const sitesStore = useSitesStore()
const sessionStore = useSessionStore()
const sites = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    loading.value = true
    error.value = null
    let response = null
    if (props.requireAuth && props.sectionId === 'favorites') {

      // Retraso para esperar a que se genere el JWT
      await new Promise(resolve => setTimeout(resolve, 100))

       response = await sitesStore.fetchSites({
        favorites: true,
        order_by: props.orderBy,
        limit: 6,
      })
    }
    else {
      response = await sitesStore.fetchSites({
      order_by: props.orderBy,
      limit: 6,
    })
    }

    console.log('[Featured] Response received:', response)
    sites.value = response.sites
  } catch (err) {
    console.error('[Featured] Error loading sites:', err)
    error.value = 'Error al cargar los sitios'
  } finally {
    //await new Promise(resolve => setTimeout(resolve, 3500))   // Retraso para simular tiempos de carga
    loading.value = false
  }
})
</script>

<style scoped>
.featured-section {
  /* margin-bottom: margen inferior de 3rem */
  margin-bottom: 3rem;
}

.carousel-control-prev,
.carousel-control-next {
  /* width/height: dimensiones de los controles */
  width: 40px;
  height: 40px;
  /* top: posiciona al 50% desde arriba */
  top: 50%;
  /* transform: traslada hacia arriba 50% de su altura para centrar verticalmente */
  transform: translateY(-50%);
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  opacity: 0.8;
}

.carousel-control-prev {
  /* left: posiciona 20px a la izquierda del contenedor */
  left: -20px;
}

.carousel-control-next {
  /* right: posiciona 20px a la derecha del contenedor */
  right: -20px;
}

.carousel-control-prev:hover,
.carousel-control-next:hover {
  opacity: 1;
}
</style>
