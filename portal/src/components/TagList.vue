<template>
  <div v-if="tags">
    <span v-for="(tag, index) in tags.slice(0, 5)"
          :key="index"
          class="badge fs-8 me-1 mb-1"
          style="border: 1px solid #71898d"
    >
      {{ tag }}
    </span>
  </div>
</template>

<script setup>
defineProps({
  tags: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.badge {
  color: #594747;
  background-color: #a2bec2;
}
</style>
