<template>
    <div>
        <h1>Mis Reseñas</h1>
        <div v-for="value in hardcodeReviews" style="display: block;">
            <ReviewComponent :review="value"/>
            <br>
        </div>
    </div>
</template>

<script setup>
import ReviewComponent from '@/components/ReviewComponent.vue';
import { useReviewsStore } from '@/stores/reviewsStore';
import { onMounted, ref } from 'vue';

const hardcodeReviews = ref(useReviewsStore().reviews);
</script>