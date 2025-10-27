<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom sticky-top">
      <div class="container">
        <router-link to="/" class="navbar-brand fw-bold">
          <i class="bi bi-compass"></i>
          Sitios Históricos
        </router-link>
        
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/" class="nav-link">Inicio</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/sites" class="nav-link">Explorar Sitios</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/about" class="nav-link">Acerca de</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main>
      <RouterView />
    </main>

    <!-- Footer -->
    <footer class="bg-light border-top mt-5 py-4">
      <div class="container">
        <div class="row">
          <div class="col-md-6">
            <h5 class="fw-bold">Programa Nacional de Registro y Preservación de Sitios Históricos</h5>
            <p class="text-muted small">
              Documentando, protegiendo y difundiendo el patrimonio cultural del país
            </p>
          </div>
          <div class="col-md-6 text-md-end">
            <p class="text-muted small mb-0">
              &copy; 2025 Programa Nacional de Sitios Históricos. Todos los derechos reservados.
            </p>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

.navbar-brand {
  font-size: 1.5rem;
}

.nav-link {
  font-weight: 500;
  transition: color 0.2s ease;
}

.nav-link.router-link-active {
  color: var(--bs-primary) !important;
}
</style>
