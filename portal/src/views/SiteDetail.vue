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
                <h3 class="mb-4">Reseñas</h3>
                <div v-if="siteReviews.length === 0" class="alert alert-info">
                  <i class="bi bi-chat-square-text me-2"></i>
                  No hay reseñas para este sitio aún. ¡Sé el primero en escribir una!
                </div>
                <div v-else class="row g-3">
                  <div v-for="review in siteReviews" :key="review.id" class="col-md-6">
                    <div class="card">
                      <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                          <div>
                            <strong>{{ review.userName || 'Usuario' }}</strong>
                            <div class="text-warning">
                              <i v-for="i in 5" :key="i" :class="i <= review.rating ? 'bi bi-star-fill' : 'bi bi-star'"></i>
                            </div>
                          </div>
                          <small class="text-muted">{{ formatDate(review.createdAt) }}</small>
                        </div>
                        <p class="card-text">{{ review.text }}</p>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Pagination Controls -->
                <div v-if="hasMoreReviews" class="text-center mt-4">
                  <button
                    class="btn btn-outline-primary"
                    @click="loadMoreReviews"
                    :disabled="loading"
                  >
                    <i class="bi bi-arrow-down-circle me-2"></i>
                    Cargar Más Reseñas
                  </button>
                </div>
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
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useSitesStore } from '@/stores/sitesStore'
import { useReviewsStore } from '@/stores/reviewsStore'
import ReviewForm from '@/components/ReviewForm.vue'

const route = useRoute()
const sitesStore = useSitesStore()
const site = ref(null)
const loading = ref(true)
const showReviewForm = ref(false)

const reviewsStore = useReviewsStore()

const siteReviews = computed(() => {
  return reviewsStore.getSiteReviews
})

const hasMoreReviews = computed(() => {
  return reviewsStore.hasMoreSiteReviews
})

onMounted(async () => {
  const slug = route.params.slug
  try {
    loading.value = true
    site.value = await sitesStore.fetchSiteBySlug(slug)

    if (site.value) {
      await sitesStore.trackSiteVisit(site.value.id)
      await reviewsStore.fetchReviewsBySite(site.value.id)
    }
  } catch (err) {
    console.error('[SiteDetail] Error loading site:', err)
  } finally {
    loading.value = false
  }
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES')
}

const onReviewAdded = () => {
  // Refresh reviews
  if (site.value) {
    reviewsStore.fetchReviewsBySite(site.value.id)
  }
}

const loadMoreReviews = async () => {
  if (!site.value || !hasMoreReviews.value) return

  const currentMeta = reviewsStore.getSiteReviewsMeta
  const nextPage = currentMeta.page + 1

  try {
    await reviewsStore.fetchReviewsBySite(site.value.id, { page: nextPage, per_page: currentMeta.per_page })
  } catch (error) {
    console.error('[SiteDetail] Error loading more reviews:', error)
  }
}
</script>

<style scoped>
.site-detail-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}
</style>
