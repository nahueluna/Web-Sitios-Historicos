<template>
  <div class="reviews-section">
    <!-- Header con estadísticas -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h3 class="mb-1">Reseñas de Visitantes</h3>
        <div v-if="reviewCount > 0" class="text-muted">
          <span class="fw-bold text-warning fs-5">{{ averageRating }}</span>
          <span class="ms-2">
            <i v-for="i in 5" :key="i" 
               :class="i <= Math.round(averageRating) ? 'bi bi-star-fill text-warning' : 'bi bi-star text-warning'">
            </i>
          </span>
          <span class="ms-2">({{ reviewCount }} {{ reviewCount === 1 ? 'reseña' : 'reseñas' }})</span>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading && reviews.length === 0" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Cargando reseñas...</span>
      </div>
      <p class="text-muted mt-2">Cargando reseñas...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="reviews.length === 0" class="alert alert-info">
      <div class="text-center py-3">
        <i class="bi bi-chat-square-text fs-1 text-muted"></i>
        <p class="mb-0 mt-2">No hay reseñas para este sitio aún.</p>
        <p class="text-muted small">¡Sé el primero en compartir tu experiencia!</p>
      </div>
    </div>

    <!-- Reviews List -->
    <div v-else class="reviews-list">
      <div v-for="review in reviews" :key="review.id" class="review-item mb-3">
        <div class="card shadow-sm">
          <div class="card-body">
            <!-- Header de la reseña -->
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div>
                <div class="d-flex align-items-center gap-2 mb-2">
                  <div class="user-avatar">
                    <i class="bi bi-person-circle fs-3 text-secondary"></i>
                  </div>
                  <div>
                    <h6 class="mb-0 fw-bold">{{ review.userName }}</h6>
                    <small class="text-muted">{{ formatDate(review.insertedAt) }}</small>
                  </div>
                </div>
              </div>
              
              <!-- Rating -->
              <div class="review-rating">
                <span class="badge bg-warning text-dark">
                  <i class="bi bi-star-fill"></i>
                  {{ review.rating }}.0
                </span>
              </div>
            </div>

            <!-- Stars Display -->
            <div class="mb-2">
              <i v-for="i in 5" :key="i" 
                 :class="i <= review.rating ? 'bi bi-star-fill text-warning' : 'bi bi-star text-muted'">
              </i>
            </div>

            <!-- Comment -->
            <p class="card-text mb-0">{{ review.comment }}</p>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <PaginationComponent
        v-if="reviews.length > 0"
        :current-page="currentPage"
        :total-pages="totalPages"
        :loading="loading"
        class="mt-4"
        @page-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useReviewsStore } from '@/stores/reviewsStore'
import PaginationComponent from '@/components/PaginationComponent.vue'

const props = defineProps({
  siteId: {
    type: [String, Number],
    required: true
  }
})

const reviewsStore = useReviewsStore()
const loading = ref(false)

const reviews = computed(() => reviewsStore.getSiteReviews)
const currentPage = computed(() => reviewsStore.getSiteReviewsMeta.page)
const averageRating = computed(() => reviewsStore.averageRating)
const reviewCount = computed(() => reviewsStore.reviewCount)

const totalPages = computed(() => {
  const meta = reviewsStore.getSiteReviewsMeta
  return meta.total ? Math.ceil(meta.total / meta.per_page) : 1
})


const handlePageChange = async (page) => {
  await fetchReviews(page)
}

const fetchReviews = async (page = 1) => {
  loading.value = true
  try {
    console.log('[ReviewsList] Fetching reviews for site:', props.siteId, 'page:', page)
    await reviewsStore.fetchReviewsBySite(props.siteId, { page, per_page: 10 })
  } catch (error) {
    console.error('[ReviewsList] Error fetching reviews:', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Lifecycle
onMounted(() => {
  fetchReviews()
})

// Watch for siteId changes
watch(() => props.siteId, () => {
  reviewsStore.clearReviews()
  fetchReviews()
})

// Expose method for parent component to refresh
defineExpose({
  refresh: fetchReviews
})
</script>

<style scoped>
.reviews-section {
  margin-top: 2rem;
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
}

.review-rating {
  min-width: 60px;
  text-align: right;
}


</style>