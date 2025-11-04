<template>
  <div class="about-page">
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <div class="card shadow-sm">
            <div class="card-body p-5">
              <h1 class="h2 fw-bold mb-4">Programa Nacional de Registro y Preservación de Sitios Históricos</h1>
              
              <p class="lead mb-4">
                Una iniciativa orientada a documentar, proteger y difundir el patrimonio cultural 
                de las distintas regiones del país.
              </p>

              <h3 class="h4 fw-bold mt-5 mb-3">Nuestra Misión</h3>
              <p class="text-muted">
                A través del relevamiento y la sistematización de datos, buscamos facilitar el acceso 
                a información precisa sobre sitios históricos, monumentos y espacios de valor cultural, 
                promoviendo su conservación y puesta en valor para las generaciones presentes y futuras.
              </p>

              <h3 class="h4 fw-bold mt-5 mb-3">Alcance del Programa</h3>
              <p class="text-muted">
                La propuesta contempla la recopilación de información histórica, geográfica y fotográfica 
                de cada sitio, así como la integración de datos sobre su accesibilidad y relevancia cultural. 
                Esta información será administrada y centralizada para permitir consultas rápidas y seguras.
              </p>

              <h3 class="h4 fw-bold mt-5 mb-3">¿Quiénes pueden acceder?</h3>
              <div class="row g-3 mt-3">
                <div class="col-md-6">
                  <div class="card h-100 border-primary">
                    <div class="card-body">
                      <h5 class="card-title">
                        <i class="bi bi-people text-primary me-2"></i>
                        Usuarios Públicos
                      </h5>
                      <ul class="list-unstyled small mb-0">
                        <li class="mb-2">✓ Explorar el mapa de sitios históricos</li>
                        <li class="mb-2">✓ Publicar reseñas y comentarios</li>
                        <li class="mb-2">✓ Marcar sitios como favoritos</li>
                        <li class="mb-2">✓ Acceso completo a la información pública</li>
                      </ul>
                    </div>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="card h-100 border-success">
                    <div class="card-body">
                      <h5 class="card-title">
                        <i class="bi bi-pencil-square text-success me-2"></i>
                        Editores
                      </h5>
                      <ul class="list-unstyled small mb-0">
                        <li class="mb-2">✓ Administrar sitios históricos</li>
                        <li class="mb-2">✓ Validar información publicada</li>
                        <li class="mb-2">✓ Moderar reseñas de usuarios</li>
                        <li class="mb-2">✓ Actualizar datos y fotografías</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              <h3 class="h4 fw-bold mt-5 mb-3">¿Qué Ofrecemos?</h3>
              <ul class="list-unstyled">
                <li class="mb-3">
                  <i class="bi bi-check-circle-fill text-success me-2"></i>
                  <strong>Información Completa:</strong> Datos históricos, geográficos y fotográficos detallados
                </li>
                <li class="mb-3">
                  <i class="bi bi-check-circle-fill text-success me-2"></i>
                  <strong>Búsqueda Avanzada:</strong> Encuentra sitios por nombre, ubicación o categoría
                </li>
                <li class="mb-3">
                  <i class="bi bi-check-circle-fill text-success me-2"></i>
                  <strong>Accesibilidad:</strong> Información sobre acceso y servicios disponibles
                </li>
                <li class="mb-3">
                  <i class="bi bi-check-circle-fill text-success me-2"></i>
                  <strong>Comunidad:</strong> Sistema de reseñas y favoritos para compartir experiencias
                </li>
                <li class="mb-3">
                  <i class="bi bi-check-circle-fill text-success me-2"></i>
                  <strong>Preservación:</strong> Contribuye a la conservación del patrimonio cultural
                </li>
              </ul>

              <div class="alert alert-info mt-5" role="alert">
                <i class="bi bi-info-circle me-2"></i>
                <strong>Para autoridades, investigadores y guías turísticos:</strong> El sistema permite 
                consultas especializadas y acceso a datos técnicos para fines académicos y profesionales.
              </div>

              <h3 class="h4 fw-bold mt-5 mb-3">Contacto</h3>
              <p class="text-muted">
                ¿Tienes información sobre un sitio histórico? ¿Necesitas más detalles sobre el programa? 
                Estamos aquí para ayudarte.
              </p>
              
              <div class="d-flex gap-3 mt-4">
                <a href="mailto:info@sitioshistoricos.gob.ar" class="btn btn-primary">
                  <i class="bi bi-envelope me-2"></i>
                  Contactar
                </a>
                <router-link to="/" class="btn btn-outline-secondary">
                  <i class="bi bi-house me-2"></i>
                  Volver al Inicio
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// No logic needed for this page
</script>

<style scoped>
.about-page {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.card {
  border: none;
}

.list-unstyled li {
  font-size: 1.05rem;
}

.lead {
  color: #6c757d;
}

.card.border-primary {
  border-width: 2px !important;
}

.card.border-success {
  border-width: 2px !important;
}
</style>
