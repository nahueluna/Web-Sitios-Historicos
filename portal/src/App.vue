<script setup>
import { RouterView } from 'vue-router'
import HeaderComponent from './components/HeaderComponent.vue';
import FooterComponent from '@/components/FooterComponent.vue';
import LoginModal from '@/components/LoginModal.vue';
</script>

<template>
  <div class="app-shell">
    <header>
      <HeaderComponent />
    </header>

    <main>
      <RouterView />
    </main>

    <footer>
      <FooterComponent />
    </footer>

    <LoginModal/>
  </div>
</template>


<style scoped>
.app-shell {
  min-height: 100vh; /* at least the viewport height */
  display: flex;
  flex-direction: column;
}

.app-shell > main {
  flex: 1 1 auto; /* grow to fill available space */
  overflow: auto; /* internal scrolling to avoid page overflow */
}

</style>
