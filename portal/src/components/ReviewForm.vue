<template>
  <div class="modal fade show d-block" style="background-color: rgba(0,0,0,0.5);" @click.self="$emit('close')">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Escribir Reseña</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="submitReview">
            <div class="mb-3">
              <label class="form-label">Calificación</label>
              <div class="rating-stars">
                <i v-for="i in 5" :key="i"
                   :class="i <= rating ? 'bi bi-star-fill text-warning' : 'bi bi-star text-muted'"
                   @click="rating = i"
                   style="cursor: pointer; font-size: 1.5rem;"></i>
              </div>
            </div>
            <div class="mb-3">
              <label for="reviewText" class="form-label">Tu reseña</label>
              <textarea
                id="reviewText"
                v-model="content"
                class="form-control"
                rows="4"
                placeholder="Comparte tu experiencia en este sitio histórico..."
                required
              ></textarea>
            </div>
            <div class="d-flex gap-2">
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <i class="bi bi-send"></i>
                {{ loading ? 'Enviando...' : 'Enviar Reseña' }}
              </button>
              <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancelar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useReviewsStore } from '@/stores/reviewsStore'
import { useSessionStore } from '@/stores/sessionStore'

const props = defineProps({
  siteId: {   // Recibo de SiteDetail.vue
    type: String,
    required: true
  }
})

const emit = defineEmits(['close', 'reviewAdded'])

const reviewsStore = useReviewsStore()
const sessionStore = useSessionStore()

const rating = ref(5)
const content = ref('')
const loading = ref(false)

const submitReview = async () => {
  if (!sessionStore.isAuthenticated) {
    alert('Debes iniciar sesión para enviar una reseña.')
    
    emit('close')
    return
  }
  if (!content.value.trim()) {
    alert('Por favor, escribe tu comentario antes de enviar la reseña.')
    return
  }

  loading.value = true
  try {
    await reviewsStore.addReview(props.siteId, {
      rating: rating.value,
      content: content.value.trim()
    })

    emit('reviewAdded')
    emit('close')
    alert('Tu reseña ha sido enviada exitosamente!')
  } catch (err) {
    alert('Error al enviar la reseña. Por favor, intenta nuevamente.')
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
</style>