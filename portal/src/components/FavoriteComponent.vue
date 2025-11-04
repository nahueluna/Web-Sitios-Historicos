<template>
  <div class="card favorite-card">
    <div class="card-body">
      <h5 class="card-title">{{ favorite.historicalSites.name }}</h5>
      <p class="card-text">{{ favorite.shortDescription }}</p>
      <p class="card-text"><small class="text-muted">Categoría: {{ favorite.category }}</small></p>
    </div>
  </div>
</template>

<style scoped>
.favorite-card {
  transition: transform 0.2s ease;
}

.favorite-card:hover {
  transform: translateY(-2px);
}
</style>

<script setup>
defineProps({
  favorite: {
    type: Object,
    required: true
  }
})
</script>