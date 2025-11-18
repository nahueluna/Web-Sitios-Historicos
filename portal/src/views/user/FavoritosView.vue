<template>
    <div class="container py-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="mb-0">Mis Favoritos <small class="text-muted ms-2">({{ favoritesList.length }})</small></h1>
            <router-link to="/profile" class="btn btn-outline-secondary d-none d-md-inline">Volver al perfil</router-link>
        </div>

        <div v-if="favoritesList.length === 0" class="alert alert-info">
            <i class="bi bi-heart me-2"></i>
            No has agregado ningún favorito aún.
        </div>

        <div v-else class="row g-3">
            <div v-for="site in favoritesList" :key="site.id" class="col-md-6 col-lg-4">
                <SiteCard :site="site" />
            </div>
        </div>
    </div>
</template>

<script setup>
import SiteCard from '@/components/SiteCard.vue'
import { computed, onMounted, ref } from 'vue'
import { useSessionStore } from '@/stores/sessionStore'
import { useFavoritesStore } from '@/stores/profileFavoriteStore'
const sessionStore = useSessionStore()
const favoritesStore = useFavoritesStore()
const favoritesList = ref([])

onMounted(async () => {
    favoritesList.value = await favoritesStore.loadAllFavorites(sessionStore.user.id) 
    //favoritesList.value = favoritesStore.getHardcodedFavorites() // --> descomentar para testear
})
</script>