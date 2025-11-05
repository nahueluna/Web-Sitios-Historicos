<template>
  <div class="container py-5">
    <h1 class="mb-4">Mis Reseñas</h1>
    <div v-if="reviews.length === 0" class="alert alert-info">
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
import { useReviewsStore } from '@/stores/reviewsStore'
import { useSessionStore } from '@/stores/sessionStore'
import { computed, onMounted } from 'vue'

const reviewsStore = useReviewsStore()
const sessionStore = useSessionStore()

const reviews = computed(() => {
  if (!sessionStore.user) return []
  return reviewsStore.getReviewsByUser(sessionStore.user.id)
})

onMounted(() => {
  reviewsStore.fetchReviews()
})
</script>