<template>
  <router-link :to="`/sites/${site.id}`" class="text-decoration-none">
    <div class="card h-100 site-card">
      <div class="position-relative card-img-wrapper">
        <img
          :src="site.coverImage || '/placeholder.svg'"
          :alt="site.name"
          class="card-img-top"
        />
        <span v-if="site.rating" class="badge bg-light text-dark position-absolute top-0 end-0 m-2">
          <i class="bi bi-star-fill text-warning"></i>
          {{ site.rating.toFixed(1) }}
        </span>
      </div>
      <div class="card-body">
        <h5 class="card-title text-truncate">{{ site.name }}</h5>
        <p class="card-text text-muted small mb-0">
          <i class="bi bi-geo-alt"></i>
          {{ site.city }}, {{ site.province }}
        </p>
      </div>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  site: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.site-card {
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.125);
}

.site-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}

.card-img-wrapper {
  aspect-ratio: 4 / 3;
  overflow: hidden;
  background-color: #e9ecef;
}

.card-img-top {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.site-card:hover .card-img-top {
  transform: scale(1.05);
}

.card-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
}
</style>
