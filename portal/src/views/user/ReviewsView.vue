<template>
  <div class="container py-5">
    <h1 class="mb-4">Mis Reseñas</h1>
    <div v-if="reviews.length === 0" class="alert alert-info">
      <i class="bi bi-chat-square-text me-2"></i>
      No has escrito ninguna reseña aún.
    </div>
    <div v-else class="row g-3">
      <div v-for="review in reviews" class="col-md-6 col-lg-4">
        <ReviewComponent :review="review" />
      </div>
    </div>
  </div>
</template>

<script setup>
import ReviewComponent from '@/components/ReviewComponent.vue'
import { useSessionStore } from '@/stores/sessionStore'
import { onMounted, ref } from 'vue'
import api from '@/service/api'

const sessionStore = useSessionStore()

const reviews = ref([])

onMounted(async () => {
  const response = await api.get(`/api/reviews/users/${sessionStore.user.id}/reviews`)
  if (response.data.reviews){
    reviews.value = response.data.reviews
  }
})
</script>