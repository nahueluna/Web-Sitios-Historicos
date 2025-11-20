<template>
    <div class="container py-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
                <h1 class="mb-0">Mis Favoritos <small class="text-muted ms-2">({{ total }})</small></h1>
                <router-link to="/profile" class="btn btn-outline-secondary d-none d-md-inline">Volver al perfil</router-link>
            </div>

            <div v-if="!loading && favoritesList.length === 0" class="alert alert-info">
                <i class="bi bi-heart me-2"></i>
                No has agregado ningún favorito aún.
            </div>

            <div v-else class="row g-3">
                <div v-for="site in favoritesList" :key="site.id" class="col-md-6 col-lg-4">
                    <SiteCard :site="site" />
                </div>

                <div class="col-12 mt-4">
                  <PaginationComponent
                    :current-page="currentPage"
                    :total-pages="totalPages"
                    :loading="loading"
                    @page-change="handlePageChange"
                  />
                </div>
            </div>
    </div>
</template>

<script setup>
import SiteCard from '@/components/SiteCard.vue'
import PaginationComponent from '@/components/PaginationComponent.vue'
import { onMounted, ref, watchEffect } from 'vue'
import { useSitesStore } from '@/stores/sitesStore'

const sitesStore = useSitesStore()
const favoritesList = ref([])
const loading = ref(true)
const currentPage = ref(1)
const perPage = 12
const totalPages = ref(1)
const total = ref(0)

const loadFavorites = async () => {
    loading.value = true
    try {
        const response = await sitesStore.fetchSites({ favorites: true, page: currentPage.value, per_page: perPage })
        favoritesList.value = response.sites || []
        total.value = response.total || (response.per_page ? (response.per_page * (response.page || 1)) : favoritesList.value.length)
        totalPages.value = response.per_page ? Math.ceil((response.total || favoritesList.value.length) / response.per_page) : 1
    } catch (err) {
        console.error('[FavoritosView] Error cargando favoritos:', err)
        favoritesList.value = []
        total.value = 0
        totalPages.value = 1
    } finally {
        loading.value = false
    }
}

const handlePageChange = async (page) => {
    currentPage.value = page
    await loadFavorites()
    setTimeout(() => window.scrollTo(0, 0), 50)
}

onMounted(async () => {
    await loadFavorites()
})

watchEffect(async() => {
  await loadFavorites()
})
</script>