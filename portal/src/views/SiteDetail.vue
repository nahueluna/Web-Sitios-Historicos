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
                <span v-if="site.rating" class="badge bg-warning text-dark fs-6">
                  <i class="bi bi-star-fill"></i>
                  {{ site.rating.toFixed(1) }}
                </span>
              </div>

              <p class="text-muted mb-3">
                <i class="bi bi-geo-alt"></i>
                {{ site.city }}, {{ site.province }}
              </p>

              <!-- Carousel -->
              <div v-if="site.images && site.images.length > 0" class="mb-4">
                <div id="siteCarousel" class="carousel slide" data-bs-ride="carousel"
                  data-bs-interva="false">

                  <div class="carousel-indicators">
                    <button
                      v-for="(img, index) in site.images"
                      :key="'ind-' + index"
                      type="button"
                      data-bs-target="#siteImagesCarousel"
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

              <p v-if="site.description" class="lead">
                {{ site.description }}
              </p>

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
                  ref="reviewsList"
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
import { ref, onMounted, computed, watchEffect} from 'vue'
import { useRoute } from 'vue-router'
import { useSitesStore } from '@/stores/sitesStore'
import { useSessionStore } from '@/stores/sessionStore'
import { useReviewsStore } from '@/stores/reviewsStore'
import { useFavoritesStore } from '@/stores/favoritesStore'
import { useLoginModalStore } from '@/stores/LoginModalStore'
import ReviewForm from '@/components/ReviewForm.vue'
import ReviewsList from '@/components/ReviewsList.vue'
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker, LPopup} from "@vue-leaflet/vue-leaflet";
import api from '@/service/api'
import { transformReview } from '@/utils/reviewTransformer'

const route = useRoute()
const sitesStore = useSitesStore()
const sessionStore = useSessionStore()
const favoritesStore = useFavoritesStore()
const loginModalStore = useLoginModalStore()
const isAuthenticated = ref(sessionStore.isAuthenticated)
const isFavorite = ref(false)
const favoriteLoading = ref(false)
const reviewsStore = useReviewsStore()
const site = ref(null)
const user = ref(sessionStore.user)
const loading = ref(true)
const showReviewForm = ref(false)
const zoom = ref(12)
const center = ref([0, 0])
const reviewsList = ref(null)
const userReview = ref(null)
const editingReview = ref(null)

const sortedImages = computed(() => {
  if (!site.value?.images) return [];
  return [...site.value.images].sort((a, b) => a.orden - b.orden);
});

watchEffect(() => {
    isAuthenticated.value = sessionStore.isAuthenticated
    user.value = sessionStore.user
})

const checkUserReview = async () => {
  if (!sessionStore.isAuthenticated || !site.value) return

  try {
    const response = await api.get(`/api/reviews/users/${sessionStore.user.id}/reviews`)
    if (response.data.reviews) {
      const existingReview = response.data.reviews.find(
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
    loading.value = true
    site.value = await sitesStore.fetchSiteById(site_id)
    console.log("site: ",site.value)
    console.log("user: ",user.value)
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

const onReviewAdded = async () => {
  if (reviewsList.value && reviewsList.value.refresh) {
    reviewsList.value.refresh()
  }
  await checkUserReview()
  showReviewForm.value = false
}

const handleFavorite = async () => {
  if (!site.value) return;

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
</style>
