<template>
  <div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1 class="mb-0">Mis Reseñas <small class="text-muted ms-2">({{ total }})</small></h1>
        <router-link to="/profile" class="btn btn-outline-secondary d-none d-md-inline">Volver al perfil</router-link>
      </div>

      <div v-if="!loading && reviews.length === 0" class="alert alert-info">
        <i class="bi bi-chat-square-text me-2"></i>
        No has escrito ninguna reseña aún.
      </div>

      <div v-else class="row g-3">
        <div v-for="review in reviews" :key="review.id" class="col-md-6 col-lg-4">
          <ReviewComponent :review="review" />
        </div>

        <div class="col-12 mt-4">
          <PaginationComponent
            :current-page="currentPage"
            :total-pages="totalPages"
            :loading="loading"
            @page-change="handlePageChange"
          />
        </div>
      </div>
  </div>
</template>

<script setup>
import ReviewComponent from '@/components/ReviewComponent.vue'
import PaginationComponent from '@/components/PaginationComponent.vue'
import { useProfileReviewStore } from '@/stores/profileReviewStore'
import { useSessionStore } from '@/stores/sessionStore'
import { onMounted, ref, watchEffect } from 'vue'

const sessionStore = useSessionStore()
const profileReviewStore = useProfileReviewStore()

const reviews = ref([])
const loading = ref(true)
const currentPage = ref(1)
const perPage = 12
const totalPages = ref(1)
const total = ref(0)

const loadUserReviews = async () => {
  loading.value = true
  try {
    const res = await profileReviewStore.loadReviews(sessionStore.user.id, currentPage.value, perPage)
    reviews.value = res.reviews || []
    total.value = res.total || reviews.value.length
    totalPages.value = res.per_page ? Math.ceil(res.total / res.per_page) : Math.ceil(total.value / perPage)
  } catch (err) {
    console.error('[ReviewsView] Error cargando reseñas:', err)
    reviews.value = []
    total.value = 0
    totalPages.value = 1
  } finally {
    loading.value = false
  }
}

const handlePageChange = async (page) => {
  currentPage.value = page
  await loadUserReviews()
  setTimeout(() => window.scrollTo(0, 0), 50)
}

onMounted(async () => {
  await loadUserReviews()
})

watchEffect(async() => {
  await loadUserReviews() 
})
</script>