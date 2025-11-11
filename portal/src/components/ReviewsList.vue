<template>
  <div class="reviews-list">
    <h3 class="mb-4">Reseñas</h3>
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Cargando reseñas...</span>
      </div>
    </div>
    <div v-else-if="reviews.length === 0" class="alert alert-info">
      <i class="bi bi-chat-square-text me-2"></i>
      No hay reseñas para este sitio aún. ¡Sé el primero en escribir una!
    </div>
    <div v-else class="g-3">
      <div v-for="review in reviews" :key="review.id" class="">
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
    <PaginationComponent
      v-if="reviews.length > 0"
      :current-page="currentPage"
      :total-pages="totalPages"
      :loading="loading"
      @page-change="handlePageChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
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
    await reviewsStore.fetchReviewsBySite(props.siteId, { page, per_page: 25 })
    console.log('[ReviewsList] Reviews loaded:', reviews.value.length, 'Total pages:', totalPages.value)
  } catch (error) {
    console.error('[ReviewsList] Error fetching reviews:', error)
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES')
}

onMounted(() => {
  fetchReviews()
})
</script>