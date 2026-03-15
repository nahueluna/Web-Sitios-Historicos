<template>
  <div class="site-detail-page">
    <div class="container py-5">
      <!-- Loading State -->
      <div v-if="loading" class="row">
        <div class="col-lg-8 mx-auto">
          <div class="card">
            <div class="placeholder-glow">
              <div class="placeholder col-12" style="height: 400px;"></div>
            </div>
            <div class="card-body">
              <h1 class="placeholder-glow">
                <span class="placeholder col-6"></span>
              </h1>
              <p class="placeholder-glow">
                <span class="placeholder col-8"></span>
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Site Details -->
      <div v-else-if="site" class="row">
        <div class="col-lg-8 mx-auto">
          <div class="card shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <h1 class="h2 fw-bold mb-0">{{ site.name }}</h1>
              </div>

              <!-- Estado de conservación -->
              <div class="my-1 d-flex align-items-center gap-2">
                <span class="fw-semibold">Estado de conservación:</span>

                <span
                  :class="getStateConfig(site.state_of_conservation).classes"
                  class="d-inline-flex align-items-center gap-1 px-2 py-1 rounded-pill"
                >
                  <i :class="getStateConfig(site.state_of_conservation).icon"></i>
                  {{ site.state_of_conservation }}
                </span>
              </div>

              <!-- TAGS -->
              <div class="mt-2">
                <span
                  v-for="tag in mappedTags"
                  :key="tag.id"
                  @click="onTagClick(tag.id)"
                  class="badge fs-8 me-1 mb-1 tag-clickable"
                  style="border: 1px solid #71898d; cursor: pointer"
                >
                  {{ tag.name }}
                </span>
              </div>

              <p class="text-muted mb-3">
                <i class="bi bi-geo-alt"></i>
                {{ site.city }}, {{ site.province }}
              </p>

              <!-- Carousel -->
              <div v-if="site.images && site.images.length > 0" class="mb-4">
                <div id="siteCarousel" class="carousel slide">

                  <div class="carousel-indicators">
                    <button
                      v-for="(img, index) in sortedImages"
                      :key="'ind-' + index"
                      type="button"
                      data-bs-target="#siteCarousel"
                      :data-bs-slide-to="index"
                      :class="{ active: index === 0 }"
                      aria-current="true"
                    ></button>
                  </div>

                  <div class="carousel-inner">
                    <div
                      v-for="(img, index) in sortedImages"
                      :key="img.url"
                      class="carousel-item"
                      :class="{ active: index === 0 }"
                    >
                      <img
                        :src="img.url"
                        class="d-block w-100"
                        style="max-height: 400px; object-fit: contain;"
                      />

                      <div class="carousel-caption d-none d-md-block bg-dark bg-opacity-50 rounded p-2">
                        <h5>{{ img.titulo }}</h5>
                        <p>{{ img.desc }}</p>
                      </div>
                    </div>
                  </div>

                  <!-- Controls -->
                  <button class="carousel-control-prev" type="button" data-bs-target="#siteCarousel" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                  </button>
                  <button class="carousel-control-next" type="button" data-bs-target="#siteCarousel" data-bs-slide="next">
                    <span class="carousel-control-next-icon" aria-hidden="true"></span>
                  </button>

                </div>
              </div>

              <!-- No images fallback -->
              <div v-else class="mb-4">
                <img
                  src="https://via.placeholder.com/800x400?text=Sin+imágenes"
                  class="d-block w-100"
                  style="max-height: 400px; object-fit: cover;"
                />
              </div>

              <!-- DESCRIPCIÓN -->
              <div v-if="site.short_description || site.description" class="mb-3">

                <!-- Texto visible -->
                <p class="lead">
                  {{ showFullDescription ? site.description : site.short_description }}
                </p>

                <!-- Botón Ver Más / Ver Menos -->
                <button
                  class="btn btn-link text-decoration-none p-0 d-inline-flex align-items-center gap-1"
                  @click="showFullDescription = !showFullDescription"
                >
                  <span>{{ showFullDescription ? 'Ver menos' : 'Ver más' }}</span>
                  <i :class="showFullDescription ? 'bi bi-chevron-up' : 'bi bi-chevron-down'"></i>
                </button>

              </div>

              <!-- Mapa -->
              <div class="map-wrapper">
                <l-map ref="map" v-model:zoom="zoom" :center="[site.lat, site.long]">
                  <l-tile-layer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    layer-type="base"
                    name="OpenStreetMap"
                  ></l-tile-layer>
                  <l-marker :lat-lng="[site.lat, site.long]">
                    <l-popup>{{ site.name }}</l-popup>
                  </l-marker>
                </l-map>
              </div>

              <div class="d-flex gap-3 mt-4">
                <button class="btn btn-primary" @click="handleFavorite">
                  <i :class="isFavorite ? 'bi bi-heart-fill' : 'bi bi-heart'"></i>
                  {{ isFavorite ? "Quitar de Favoritos" : "Agregar a Favoritos" }}
                </button>
                <button
                  class="btn btn-success"
                  @click="handleWriteReview"
                >
                  <i :class="userReview ? 'bi bi-pencil' : 'bi bi-star'"></i>
                  {{ userReview ? 'Editar mi Reseña' : 'Escribir Reseña' }}
                </button>
                <router-link to="/sites" class="btn btn-outline-secondary">
                  <i class="bi bi-arrow-left"></i>
                  Volver a Sitios
                </router-link>
              </div>

              <!-- Reviews Section -->
              <div class="mt-5">
                <ReviewsList
                  v-if="site"
                  :site-id="site.id"
                  :refresh-trigger="refreshTrigger"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Not Found -->
      <div v-else class="text-center py-5">
        <i class="bi bi-exclamation-circle display-1 text-muted"></i>
        <h2 class="mt-3">Sitio No Encontrado</h2>
        <p class="text-muted">El sitio que buscas no existe.</p>
        <router-link to="/" class="btn btn-primary">
          Ir al Inicio
        </router-link>
      </div>
    </div>

    <!-- Review Form Modal -->
    <ReviewForm
      v-if="showReviewForm && site"
      :site-id="site.id"
      :review="editingReview"
      @close="showReviewForm = false; editingReview = null"
      @review-added="onReviewAdded"
      @review-updated="onReviewAdded"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useSitesStore } from '@/stores/sitesStore'
import { useSessionStore } from '@/stores/sessionStore'
import { useFavoritesStore } from '@/stores/favoritesStore'
import { useLoginModalStore } from '@/stores/LoginModalStore'
import { useProfileReviewStore } from '@/stores/profileReviewStore'
import ReviewForm from '@/components/ReviewForm.vue'
import ReviewsList from '@/components/ReviewsList.vue'
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker, LPopup} from "@vue-leaflet/vue-leaflet";
import { transformReview } from '@/utils/reviewTransformer'
import { getStateConfig } from '@/utils/stateConfig'
import { Carousel } from 'bootstrap'

const route = useRoute()
const router = useRouter()
const sitesStore = useSitesStore()
const sessionStore = useSessionStore()
const favoritesStore = useFavoritesStore()
const loginModalStore = useLoginModalStore()
const profileReviewStore = useProfileReviewStore()
const { isAuthenticated } = storeToRefs(sessionStore)
const isFavorite = ref(false)
const site = ref(null)
const loading = ref(true)
const showReviewForm = ref(false)
const zoom = ref(12)
const userReview = ref(null)
const editingReview = ref(null)
const refreshTrigger = ref(0)
const showFullDescription = ref(false)

const sortedImages = computed(() => {
  if (!site.value?.images) return [];
  return [...site.value.images].sort((a, b) => a.orden - b.orden);
});

// Inicialización manual del carousel de Bootstrap tras renderizado dinámico
let carouselInstance = null

watch(site, async (newSite) => {
  carouselInstance?.dispose()
  carouselInstance = null

  if (newSite?.images?.length > 0) {
    await nextTick()
    const el = document.getElementById('siteCarousel')
    if (el) {
      carouselInstance = new Carousel(el, { interval: false })
    }
  }
})

onBeforeUnmount(() => {
  carouselInstance?.dispose()
  carouselInstance = null
})

const checkUserReview = async () => {
  if (!sessionStore.isAuthenticated || !site.value) return

  try {
    const reviews = await profileReviewStore.loadAllReviews(sessionStore.user.id)
    if (reviews) {
      const existingReview = reviews.find(
        r => r.historic_site?.id === site.value.id
      )

      if (existingReview) {
        userReview.value = transformReview(existingReview)
      }
    }
  } catch (error) {
    console.error('Error al verificar reseña del usuario:', error)
  }
}

const handleWriteReview = () => {
  if (!sessionStore.isAuthenticated) {
    loginModalStore.openLoginModal()

    sessionStore.redirect_uri = `/sites/${route.params.site_id}`

    return
  }

  if (userReview.value) {
    // Usuario ya tiene una reseña, ofrecer editar
    if (confirm('Ya tienes una reseña para este sitio. ¿Deseas editarla?')) {
      editingReview.value = userReview.value
      showReviewForm.value = true
    }
  } else {
    // Nueva reseña
    editingReview.value = null
    showReviewForm.value = true
  }
}

onMounted(async () => {
  const site_id = route.params.site_id
  try {
    if (!sitesStore.allTags.length) {
      await sitesStore.fetchAllTags()
    }
    loading.value = true
    site.value = await sitesStore.fetchSiteById(site_id)
    if (site.value) {
      await checkUserReview()
      if (isAuthenticated.value) {
        isFavorite.value = await favoritesStore.checkFavorite(site.value.id);
      } else {
        isFavorite.value = false
      }
    }
  } catch (err) {
    console.error('[SiteDetail] Error loading site:', err)
  } finally {
    loading.value = false
  }
})

const mappedTags = computed(() => {
  if (!site.value || !site.value.tags || !sitesStore.allTags) return []
  return site.value.tags
    .map(tagName => sitesStore.allTags.find(t => t.name === tagName))
    .filter(Boolean)
})

function onTagClick(tagId) {
  router.push(`/sites?tags=${tagId}`)
}

const onReviewAdded = async () => {
  refreshTrigger.value++
  await checkUserReview()
  showReviewForm.value = false
}

const handleFavorite = async () => {
  if (!site.value) return;

  if (!sessionStore.isAuthenticated) {
    loginModalStore.openLoginModal();
    sessionStore.redirect_uri = `/sites/${route.params.site_id}`;
    return;
  }

  try {
    if (isFavorite.value) {
      const ok = await favoritesStore.removeFavorite(site.value.id);
      if (ok) isFavorite.value = false;
    } else {
      const ok = await favoritesStore.addFavorite(site.value.id);
      if (ok) isFavorite.value = true;
    }
  } catch (error) {
    console.error("[SiteDetail] Error toggling favorite:", error);
  }
};
</script>

<style scoped>
.site-detail-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}
.carousel-control-prev-icon,
.carousel-control-next-icon {
  filter: invert(1) brightness(0.2);
}

.map-wrapper {
  width: 100%;
  max-width: 100%;
  height: 500px;
}

@media (max-width: 760px) {
  .map-wrapper {
    height: 350px;
  }
}

.badge {
  color: #594747;
  background-color: #a2bec2;
}
</style>
