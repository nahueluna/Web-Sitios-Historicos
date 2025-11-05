<template>
    <footer class="site-footer bg-light">
        <div class="container d-flex flex-column flex-md-row align-items-center justify-content-between py-3">
            <div class="footer-left">
                <strong>Portal de Sitios Históricos</strong>
                <p class="muted mb-0">Hecho con ❤️ · 2025</p>
            </div>

            <nav class="footer-links d-flex gap-3" aria-label="Enlaces del pie de página">
                <RouterLink to="/" class="nav-link">Home</RouterLink>
                <RouterLink to="/perfil" class="nav-link">Perfil</RouterLink>
            </nav>
        </div>

        <div class="text-center mt-2">
            <button class="btn btn-sm btn-outline-secondary" @click="scrollTop">↑ Arriba</button>
        </div>
    </footer>
</template>

<script setup>
function scrollTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.footer-left { font-weight: 600; }
.muted { color: #6b7280; }
.footer-links .nav-link { color: inherit; padding: 0.25rem; }
.footer-social .icon { display: inline-flex; padding: 0.25rem; border-radius: 6px; }
.footer-social .icon:hover { background: rgba(0,0,0,0.03); }
</style>