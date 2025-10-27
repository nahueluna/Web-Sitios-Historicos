<template>
  <article class="review-card">
    <header class="review-card-header">
      <h3 class="review-title">{{ favorite.historicalSites.name }}</h3>
    </header>

    <div class="review-card-body">
      <p><strong>Descripción corta:</strong> {{ favorite.shortDescription }}</p>
      <p><strong>Categoría:</strong> {{ favorite.category }}</p>
    </div>
  </article>
</template>

<style scoped>
.review-card {
  background: var(--app-bg, #ffffff);
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 6px 20px rgba(2,6,23,0.06); /* subtle raised look */
  border: 1px solid rgba(15,23,36,0.04);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.review-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(2,6,23,0.09);
}

.review-card-header {
  margin-bottom: 0.5rem;
}

.review-title {
  margin: 0;
  font-size: 1.05rem;
}

.review-card-body p { margin: 0.5rem 0; color: var(--muted, #6b7280); }

@media (max-width: 560px) {
  .review-card { padding: 0.75rem; }
}

</style>

<script setup>
const props = defineProps({
  favorite: {
    type: Object,
    required: true
  }
})
</script>
