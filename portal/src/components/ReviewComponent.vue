<template>
    <div>
        <h3>Reseña de {{ review.historicalSites.name }}</h3>
        <p><strong>Reseña:</strong> {{ review.text }}</p>
        <p><strong>Calificación:</strong> {{ review.rating }}</p>
    </div>
</template> 

<script setup>
const props = defineProps({
  review: {
    type: Object,
    required: true
  }
})
</script>
