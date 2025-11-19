<template>
  <div class="modal fade show d-block" style="background-color: rgba(0,0,0,0.5);" @click.self="$emit('close')" role="dialog" aria-modal="true" aria-labelledby="reviewModalTitle">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 id="reviewModalTitle" class="modal-title">{{ isEditMode ? 'Editar Reseña' : 'Escribir Reseña' }}</h5>
          <button type="button" class="btn-close" @click="$emit('close')" aria-label="Cerrar"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitReview">
            <div class="mb-3">
              <label class="form-label" for="rating-stars">Calificación</label>
              <div id="rating-stars" class="rating-stars" role="radiogroup" aria-label="Calificación de 1 a 5 estrellas">
                <button 
                  v-for="i in 5" 
                  :key="i"
                  type="button"
                  class="btn-star"
                  :class="{ 'active': i <= rating }"
                  @click="rating = i"
                  :aria-label="`${i} estrella${i !== 1 ? 's' : ''}`"
                  :aria-pressed="i === rating"
                >
                  <i :class="i <= rating ? 'bi bi-star-fill text-warning' : 'bi bi-star text-muted'" aria-hidden="true"></i>
                </button>
              </div>
            </div>
            <div class="mb-3">
              <label for="reviewText" class="form-label">
                Tu reseña 
                <span class="text-muted small">({{ content.length }}/1000 caracteres)</span>
              </label>
              <textarea
                id="reviewText"
                v-model="content"
                class="form-control"
                :class="{ 'is-invalid': contentError }"
                rows="4"
                minlength="20"
                maxlength="1000"
                placeholder="Comparte tu experiencia en este sitio histórico (mínimo 20 caracteres)..."
                required
              ></textarea>
              <div v-if="contentError" class="invalid-feedback">
                {{ contentError }}
              </div>
              <div v-else class="form-text">
                Mínimo 20 caracteres, máximo 1000 caracteres.
              </div>
            </div>
            <div v-if="isEditMode" class="alert alert-info small mb-3">
              <i class="bi bi-info-circle me-1"></i>
              Tu reseña será enviada a moderación nuevamente.
            </div>
            <div class="d-grid gap-2 d-md-flex">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <i :class="isEditMode ? 'bi bi-check-lg' : 'bi bi-send'" aria-hidden="true"></i>
                <span class="ms-1">{{ loading ? (isEditMode ? 'Guardando...' : 'Enviando...') : (isEditMode ? 'Guardar Cambios' : 'Enviar Reseña') }}</span>
              </button>
              <button type="button" class="btn btn-secondary" @click="$emit('close')">
                Cancelar
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useReviewsStore } from '@/stores/reviewsStore'
import { useSessionStore } from '@/stores/sessionStore'

const props = defineProps({
  siteId: {
    type: [String, Number],
    required: true
  },
  review: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'reviewAdded', 'reviewUpdated'])

const reviewsStore = useReviewsStore()
const sessionStore = useSessionStore()

const rating = ref(5)
const content = ref('')
const loading = ref(false)
const contentError = ref('')

const isEditMode = computed(() => props.review !== null)

const validateContent = () => {
  const trimmedContent = content.value.trim()
  
  if (!trimmedContent) {
    contentError.value = 'La reseña no puede estar vacía.'
    return false
  }
  
  if (trimmedContent.length < 20) {
    contentError.value = `La reseña debe tener al menos 20 caracteres (actual: ${trimmedContent.length}).`
    return false
  }
  
  if (trimmedContent.length > 1000) {
    contentError.value = `La reseña no puede superar los 1000 caracteres (actual: ${trimmedContent.length}).`
    return false
  }
  
  contentError.value = ''
  return true
}

onMounted(() => {
  if (isEditMode.value) {
    rating.value = props.review.rating
    content.value = props.review.content
  }
})

const submitReview = async () => {
  if (!sessionStore.isAuthenticated && !isEditMode.value) {
    alert('Debes iniciar sesión para enviar una reseña.')
    emit('close')
    return
  }

  // Validar contenido
  if (!validateContent()) {
    return
  }

  // Validar rating (1-5)
  if (rating.value < 1 || rating.value > 5) {
    alert('La puntuación debe estar entre 1 y 5 estrellas.')
    return
  }

  loading.value = true
  try {
    const reviewData = {
      rating: rating.value,
      content: content.value.trim()
    }

    if (isEditMode.value) {
      await reviewsStore.updateReview(props.siteId, props.review.id, reviewData)
      emit('reviewUpdated')
      alert('Reseña actualizada exitosamente. Será revisada por un moderador.')
    } else {
      await reviewsStore.addReview(props.siteId, reviewData)
      emit('reviewAdded')
      alert('Reseña enviada exitosamente. Será revisada por un moderador.')
    }

    emit('close')
  } catch (error) {
    console.error('Error al procesar reseña:', error)
    
    // Manejar errores específicos
    if (error.response?.status === 403) {
      alert('✗ No tienes permiso para ' + (isEditMode.value ? 'editar' : 'crear') + ' esta reseña.')
    } else if (error.response?.status === 404) {
      alert('✗ La reseña o el sitio no existe.')
    } else if (error.response?.status === 409) {
      alert('✗ Ya has enviado una reseña para este sitio. Puedes editarla desde "Mis Reseñas".')
    } else if (error.response?.data?.error?.message) {
      alert('✗ ' + error.response.data.error.message)
    } else {
      alert('✗ Error al ' + (isEditMode.value ? 'actualizar' : 'enviar') + ' la reseña. Por favor, intenta nuevamente.')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.rating-stars {
  display: flex;
  gap: 0.25rem;
}

.btn-star {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  font-size: 1.5rem;
  transition: transform 0.1s;
}

.btn-star:hover {
  transform: scale(1.1);
}

.btn-star:focus {
  outline: 2px solid #0d6efd;
  outline-offset: 2px;
  border-radius: 4px;
}
</style>