<template>
  <nav aria-label="Paginación de reseñas" class="d-flex justify-content-center mt-4">
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
        :class="{ active: page === currentPage }"
      >
        <button
          class="page-link"
          @click="goToPage(page)"
          :disabled="loading"
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
  return Array.from({ length: props.totalPages }, (_, i) => i + 1)
})

const goToPage = (page) => {
  if (page >= 1 && page <= props.totalPages && !props.loading) {
    emit('pageChange', page)
  }
}
</script>