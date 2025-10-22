<script setup>
import { RouterView } from 'vue-router'
import HeaderComponent from './components/HeaderComponent.vue';
import FooterComponent from '@/components/FooterComponent.vue';
import LoginModal from '@/components/LoginModal.vue';
</script>

<template>
  <div>
    <header>
      <HeaderComponent />
    </header>

    <main >
      <RouterView />
    </main>

    <footer>
      <FooterComponent />
    </footer>

    <LoginModal/>
  </div>
</template>


<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}


@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
