<template>
  <nav v-if="totalPages > 1" aria-label="Paginación de reseñas" class="d-flex justify-content-center mt-4">
    <ul class="pagination">
      <!-- Botón Anterior -->
      <li class="page-item" :class="{ disabled: currentPage === 1 || loading }">
        <button
          class="page-link"
          @click="goToPage(currentPage - 1)"
          :disabled="currentPage === 1 || loading"
          aria-label="Página anterior"
        >
          <i class="bi bi-chevron-left"></i>
        </button>
      </li>

      <!-- Páginas -->
      <li
        v-for="page in visiblePages"
        :key="page"
        class="page-item"
        :class="{ active: page === currentPage, disabled: page === '...' }"
      >
        <button
          class="page-link"
          @click="page !== '...' && goToPage(page)"
          :disabled="loading || page === '...'"
        >
          {{ page }}
        </button>
      </li>

      <!-- Botón Siguiente -->
      <li class="page-item" :class="{ disabled: currentPage === totalPages || loading }">
        <button
          class="page-link"
          @click="goToPage(currentPage + 1)"
          :disabled="currentPage === totalPages || loading"
          aria-label="Página siguiente"
        >
          <i class="bi bi-chevron-right"></i>
        </button>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['pageChange'])

const visiblePages = computed(() => {
  const total = props.totalPages
  const current = props.currentPage

  if (total <= 7) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }

  const pages = []

  // Always show first page
  pages.push(1)

  if (current > 3) {
    pages.push('...')
  }

  // Pages around current
  const start = Math.max(2, current - 1)
  const end = Math.min(total - 1, current + 1)

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  if (current < total - 2) {
    pages.push('...')
  }

  // Always show last page
  pages.push(total)

  return pages
})

const goToPage = (page) => {
  if (page >= 1 && page <= props.totalPages && !props.loading) {
    emit('pageChange', page)
  }
}
</script>