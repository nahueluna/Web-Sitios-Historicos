<template>
  <div class="card review-card">
    <div class="card-body">
      <h5 class="card-title">{{ review.historicalSites.name }}</h5>
      <p class="card-text">{{ review.text }}</p>
      <p class="card-text"><small class="text-muted">Calificación: {{ review.rating }}/5</small></p>
    </div>
  </div>
</template>

<style scoped>
.review-card {
  transition: transform 0.2s ease;
}

.review-card:hover {
  transform: translateY(-2px);
}
</style>

<script setup>
defineProps({
  review: {
    type: Object,
    required: true
  }
})
</script>
