<template>
  <div class="reviews-section">
    <!-- Header con estadísticas -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h3 class="mb-1">Reseñas de Visitantes</h3>
        <div v-if="reviewCount > 0" class="text-muted">
          <span class="fw-bold text-warning fs-5">{{ averageRating }}</span>
          <span class="ms-2" role="img" :aria-label="`Calificación promedio: ${averageRating} de 5 estrellas`">
            <i v-for="i in 5" :key="i"
               :class="i <= Math.round(averageRating) ? 'bi bi-star-fill text-warning' : 'bi bi-star text-warning'"
               aria-hidden="true">
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

    <!-- Block feature state -->
    <div v-else-if="error && error.code === 'feature_disabled'" class="text-center py-5">
      <i class="bi bi-cone-striped fs-1 text-muted" aria-hidden="true"></i>
      <p class="text-muted mt-2">{{ error.details || error.message || 'Esta función estará disponible pronto.' }}</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="reviews.length === 0" class="alert alert-info" role="alert">
      <div class="text-center py-3">
        <i class="bi bi-chat-square-text fs-1 text-muted" aria-hidden="true"></i>
        <p class="mb-0 mt-2">No hay reseñas para este sitio aún.</p>
        <p class="text-muted small">¡Sé el primero en compartir tu experiencia!</p>
      </div>
    </div>

    <!-- Reviews List -->
    <div v-else class="reviews-list">
      <div v-for="review in reviews" :key="review.id" class="review-item mb-3">
        <div class="card shadow-sm review-card">
          <div class="card-body">
            <!-- Header de la reseña -->
            <div class="d-flex justify-content-between align-items-start mb-3">
              <div class="flex-grow-1">
                <div class="d-flex align-items-center mb-2" style="gap: 0.5rem;">
                  <div class="user-avatar">
                    <i class="bi bi-person-circle fs-3 text-secondary"></i>
                  </div>
                  <div>
                    <h6 class="mb-0 fw-bold">{{ review.userName }}</h6>
                    <small class="text-muted">{{ formatDate(review.insertedAt) }}</small>
                  </div>
                </div>
              </div>

              <!-- Rating and Delete Button -->
              <div class="d-flex align-items-center gap-2">
                <div class="review-rating">
                  <span class="badge bg-warning text-dark">
                    <i class="bi bi-star-fill"></i>
                    {{ review.rating }}.0
                  </span>
                </div>
                <button
                  v-if="canDeleteReview(review)"
                  @click="confirmDelete(review)"
                  class="btn btn-sm btn-outline-danger"
                  type="button"
                  aria-label="Eliminar reseña"
                  title="Eliminar reseña"
                >
                  <i class="bi bi-trash" aria-hidden="true"></i>
                </button>
              </div>
            </div>

            <!-- Stars Display -->
            <div class="mb-2" role="img" :aria-label="`Calificación: ${review.rating} de 5 estrellas`">
              <i v-for="i in 5" :key="i"
                 :class="i <= review.rating ? 'bi bi-star-fill text-warning' : 'bi bi-star text-muted'"
                 aria-hidden="true">
              </i>
            </div>

            <!-- Comment -->
            <p class="card-text mb-0">{{ review.content }}</p>
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
import { useSessionStore } from '@/stores/sessionStore'
import { useProfileReviewStore } from '@/stores/profileReviewStore'
import PaginationComponent from '@/components/PaginationComponent.vue'

const props = defineProps({
  siteId: {
    type: [String, Number],
    required: true
  },
  refreshTrigger: {
    type: Number,
    default: 0
  }
})

const reviewsStore = useReviewsStore()
const sessionStore = useSessionStore()
const profileReviewStore = useProfileReviewStore()
const loading = ref(false)
const userReviewIds = ref(new Set())

const reviews = computed(() => reviewsStore.getSiteReviews)
const currentPage = computed(() => reviewsStore.getSiteReviewsMeta.page)
const averageRating = computed(() => reviewsStore.averageRating)
const reviewCount = computed(() => reviewsStore.reviewCount)
const error = computed(() => reviewsStore.getError)

const totalPages = computed(() => {
  const meta = reviewsStore.getSiteReviewsMeta
  return meta.total ? Math.ceil(meta.total / meta.per_page) : 1
})

watch(error, (newError) => {
  if (newError && newError.message) {
    // No mostrar alert ni limpiar para errores que se manejan en la UI
    if (newError.code === 'feature_disabled') {
      return
    } else if(newError.code === 'duplicate') {
      return
    } else {
      alert('Error al cargar reseñas')
    }

    dismissError()
  }
})


const handlePageChange = async (page) => {
  await fetchReviews(page)
}

const fetchReviews = async (page = 1) => {
  loading.value = true
  try {
    await reviewsStore.fetchReviewsBySite(props.siteId, { page, per_page: 10 })

    // Si está autenticado, obtener IDs de sus reseñas
    if (sessionStore.isAuthenticated) {
      await fetchUserReviewIds()
    }
  } catch (error) {
    console.error('Error al cargar reseñas:', error)
  } finally {
    loading.value = false
  }
}

// Si el usuario está autenticado, hace una petición adicional a /api/reviews/users/{user_id}/reviews para obtener todas las reseñas del usuario
// Guarda los IDs de las reseñas del usuario en un Set para búsqueda rápida
// Compara cada reseña pública con el Set de IDs del usuario
const fetchUserReviewIds = async () => {
  try {
    const reviews = await profileReviewStore.loadAllReviews(sessionStore.user.id)
    if (reviews) {
      userReviewIds.value = new Set(reviews.map(r => r.id))
    }
  } catch (error) {
    console.error('Error al cargar IDs de reseñas del usuario:', error)
  }
}

const dismissError = () => {
  reviewsStore.clearReviews()
}

const formatDate = (dateString) => {
  if (!dateString) return 'Fecha no disponible'

  // Si la fecha viene en formato DD-MM-YYYY, convertirla a YYYY-MM-DD
  if (dateString.includes('-')) {
    const parts = dateString.split('-')
    if (parts.length === 3 && parts[0].length <= 2) {
      const [day, month, year] = parts
      dateString = `${year}-${month}-${day}`
    }
  }

  const date = new Date(dateString)
  if (isNaN(date.getTime())) {
    return dateString
  }

  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const canDeleteReview = (review) => {
  if (!sessionStore.isAuthenticated) return false

  // Verificar si el ID de la reseña está en el conjunto de reseñas del usuario
  return userReviewIds.value.has(review.id)
}

const confirmDelete = async (review) => {
  const confirmMsg = `¿Estás seguro de que quieres eliminar esta reseña?\n\nCalificación: ${review.rating} estrellas\n\nEsta acción no se puede deshacer.`

  if (confirm(confirmMsg)) {
    try {
      await reviewsStore.removeReview(props.siteId, review.id)
      await fetchReviews(currentPage.value)
      alert('✓ Reseña eliminada exitosamente.')
    } catch (error) {
      console.error('Error al eliminar la reseña:', error)

      if (error.response?.status === 403) {
        alert('✗ No tienes permiso para eliminar esta reseña.')
      } else if (error.response?.status === 404) {
        alert('✗ La reseña no existe o ya fue eliminada.')
      } else {
        alert('✗ Error al eliminar la reseña. Por favor, intenta nuevamente.')
      }
    }
  }
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

// Watch for refresh trigger
watch(() => props.refreshTrigger, () => {
  fetchReviews()
})
</script>

<style scoped>
.reviews-section {
  margin-top: 2rem;
}

.review-card {
  transition: transform 0.2s ease;
}

.review-card:hover {
  transform: translateY(-2px);
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
