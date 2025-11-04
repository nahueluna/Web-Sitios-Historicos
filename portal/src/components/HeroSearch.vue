<template>
  <form @submit.prevent="handleSearch" class="d-flex gap-2">
    <div class="input-group flex-grow-1">
      <span class="input-group-text bg-white">
        <i class="bi bi-search"></i>
      </span>
      <input
        v-model="searchQuery"
        type="search"
        class="form-control"
        placeholder="Buscar sitios históricos por nombre, ubicación o categoría..."
      />
    </div>
    <button type="submit" class="btn btn-primary px-4">
      Buscar
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const searchQuery = ref('')
const router = useRouter()

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      name: 'sites',
      query: { search: searchQuery.value.trim() },
    })
  }
}
</script>

<style scoped>
.input-group-text {
  border-right: 0;
}

.form-control {
  border-left: 0;
}

.form-control:focus {
  border-left: 0;
  box-shadow: none;
}

.input-group:focus-within .input-group-text {
  border-color: #86b7fe;
}
</style>
