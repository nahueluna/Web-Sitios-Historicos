<template>
    <div>
        <h1>Mis Favoritos</h1>
        <div v-for="value in hardcodeFavorites" style="display: block;">
            <FavoriteComponent :favorite="value"/>
            <br>
        </div>
    </div>
</template>

<script setup>
import FavoriteComponent from '@/components/FavoriteComponent.vue';
import { useFavoritesStore } from '@/stores/favoriteStore';
import { ref } from 'vue';

const hardcodeFavorites = ref(useFavoritesStore().favorites);
</script>