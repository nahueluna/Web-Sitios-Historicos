<template>
  <div class="card review-card">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-2">
        <h5 class="card-title mb-0">{{ review.siteName || 'Sitio' }}</h5>
        <button @click="confirmDelete" class="btn btn-sm btn-outline-danger">
          <i class="bi bi-trash"></i>
        </button>
      </div>
      <p class="card-text">{{ review.text }}</p>
      <p class="card-text"><small class="text-muted">Calificación: {{ review.rating }}/5</small></p>
      <p class="card-text"><small class="text-muted">Fecha: {{ formatDate(review.createdAt) }}</small></p>
    </div>
  </div>
</template>

<style scoped>
.review-card {
  transition: transform 0.2s ease;
}

.review-card:hover {
  transform: translateY(-2px);
}
</style>

<script setup>
import { useReviewsStore } from '@/stores/reviewsStore'

const props = defineProps({
  review: {
    type: Object,
    required: true
  }
})

const reviewsStore = useReviewsStore()

const confirmDelete = async () => {
  if (confirm('¿Estás seguro de que quieres eliminar esta reseña?')) {
    try {
      await reviewsStore.removeReview(props.review.id)
      alert('Reseña eliminada exitosamente')
    } catch {
      alert('Error al eliminar la reseña')
    }
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES')
}
</script>
