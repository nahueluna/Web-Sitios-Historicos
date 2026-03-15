<script setup>
import { RouterView } from 'vue-router'
import AppHeader from './components/AppHeader.vue'
import AppFooter from './components/AppFooter.vue'
import LoginModal from './components/LoginModal.vue';
</script>

<template>
  <div id="app">
    <!-- Navigation -->
    <AppHeader />

    <!-- Main Content -->
    <main>
      <RouterView />
    </main>

    <!-- Login Modal (global) -->
    <LoginModal />

    <!-- Footer -->
    <AppFooter />
  </div>
</template>


<style scoped>
</style>
