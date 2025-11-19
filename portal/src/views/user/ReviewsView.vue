<template>
  <div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="mb-0">Mis Reseñas <small class="text-muted ms-2">({{ reviews.length }})</small></h1>
      <router-link to="/profile" class="btn btn-outline-secondary d-none d-md-inline">Volver al perfil</router-link>
    </div>

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
import { useProfileReviewStore } from '@/stores/profileReviewStore'
import { useSessionStore } from '@/stores/sessionStore'
import { computed, onMounted, ref } from 'vue'

const sessionStore = useSessionStore()
const profileReviewStore = useProfileReviewStore()

const reviews = ref([])

onMounted(async () => {
  reviews.value = await profileReviewStore.loadAllReviews(sessionStore.user.id) 
  //reviews.value = profileReviewStore.getHardcodedReviews() // --> descomentar para testear
})
</script>