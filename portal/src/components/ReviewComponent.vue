  <template>
    <router-link :to="`/sites/${review.historic_site?.id}`" class="text-decoration-none">
      <div class="card h-100 review-card">
        <div class="card-body d-flex flex-column">
          <div class="d-flex justify-content-between align-items-start mb-2">
            <h5 class="card-title mb-0 text-truncate">{{ review.historic_site?.name || 'Sitio' }}</h5>
            <span v-if="review.rating" class="badge bg-light text-dark align-self-start">
              <i class="bi bi-star-fill text-warning"></i>
              {{ Number(review.rating).toFixed(1) }}
            </span>
          </div>

          <p class="card-text mb-0">{{ review.content }}</p>
        </div>
      </div>
<<<<<<< HEAD
      <p class="card-text">{{ review.content }}</p>
      <p class="card-text"><small class="text-muted">Calificación: {{ review.rating }}/5</small></p>
      <p class="card-text"><small class="text-muted">Fecha: {{ formatDate(review.createdAt) }}</small></p>
    </div>
  </div>
</template>
=======
    </router-link>
  </template>
>>>>>>> dev

  <style scoped>
  .review-card {
    transition: all 0.2s ease;
    border: 1px solid rgba(0, 0, 0, 0.06);
  }

  .review-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 0.5rem 0.8rem rgba(0, 0, 0, 0.08);
  }

  .card-title {
    font-weight: 600;
    margin-bottom: 0.25rem;
  }

  .badge {
    font-size: 0.9rem;
  }
  </style>

  <script setup>
  const props = defineProps({
    review: { type: Object, required: true }
  })
  </script>
