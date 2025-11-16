<template>
  <div class="container py-5">
    <h1 class="mb-4">Mis Reseñas</h1>
    <div v-if="loading" class="text-center my-4">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Cargando...</span>
        </div>
      </div>
      <div v-else-if="reviews.length === 0" class="alert alert-info">
        <i class="bi bi-chat-square-text me-2"></i>
        No has escrito ninguna reseña aún.
      </div>
      <div v-else class="row g-3">
      <div v-for="review in reviews" :key="review.id" class="col-md-6 col-lg-4">
        <ReviewComponent :review="review" />
      </div>
    </div>
  </div>
</template>

<script setup>
import ReviewComponent from '@/components/ReviewComponent.vue'
import { useSessionStore } from '@/stores/sessionStore'
import { ref, onMounted } from 'vue'
import api from '@/service/api'


const sessionStore = useSessionStore()
const user = sessionStore.user

const reviews = ref([])
const loading = ref(true)
const error = ref(null)

async function loadReviews() {
  // Si no hay usuario en sesión, no intentamos la petición
  if (!user || !user.id) {
    reviews.value = []
    loading.value = false
    return
  }

  try {
    const response = await api.get(`/api/reviews/users/${user.id}/reviews`)
    // Aseguramos que sea un array
    reviews.value = response && response.data ? response.data : []
  } catch (e) {
    // En caso de error dejamos el array vacío (y registramos el error si se quiere)
    reviews.value = []
    error.value = e
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadReviews()
})
</script>