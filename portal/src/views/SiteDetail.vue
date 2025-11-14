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
            <img
              :src="site.coverImage"
              :alt="site.name"
              class="card-img-top"
              style="max-height: 400px; object-fit: cover;"
            />
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

              <p v-if="site.description" class="lead">
                {{ site.description }}
              </p>

              <!-- Mapa -->
              <div style="height:600px; width:800px">
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
                <button class="btn btn-primary">
                  <i class="bi bi-heart"></i>
                  Agregar a Favoritos
                </button>
                <button class="btn btn-success" @click="showReviewForm = true">
                  <i class="bi bi-star"></i>
                  Escribir Reseña
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
      @close="showReviewForm = false"
      @review-added="onReviewAdded"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useSitesStore } from '@/stores/sitesStore'
import ReviewForm from '@/components/ReviewForm.vue'
import ReviewsList from '@/components/ReviewsList.vue'
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { LMap, LTileLayer, LMarker, LPopup} from "@vue-leaflet/vue-leaflet";

const route = useRoute()
const sitesStore = useSitesStore()
const site = ref(null)
const loading = ref(true)
const showReviewForm = ref(false)
const zoom = ref(12)
const center = ref([0, 0])

onMounted(async () => {
  const slug = route.params.slug
  try {
    loading.value = true
    site.value = await sitesStore.fetchSiteBySlug(slug)

    if (site.value) {
      await sitesStore.trackSiteVisit(site.value.id)
    }
  } catch (err) {
    console.error('[SiteDetail] Error loading site:', err)
  } finally {
    loading.value = false
  }
})

const onReviewAdded = () => {
  // Reviews will be refreshed when component re-mounts or manually
}
</script>

<style scoped>
.site-detail-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}
</style>
