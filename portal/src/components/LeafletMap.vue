<template>
  <main>
    <l-map
      ref="map"
      v-model:zoom="zoom"
      :center="center"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
      @ready="onMapReady"
      id="map"
    >
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
        attribution='&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors'
      />

      <l-control>
        <button v-if="showUpdateRadiusButton" @click="updateSearchRadius" class="btn btn-primary d-none d-md-inline">
          Actualizar radio de búsqueda
        </button>
        <button v-if="showUpdateRadiusButton" @click="updateSearchRadius" class="btn btn-primary btn-sm d-inline d-md-none">
          Actualizar radio
        </button>
      </l-control>
      <l-circle :lat-lng="radiusCenter" :radius="radius" color="blue" />
      <div v-for="marker in markers" :key="marker.id">
        <l-marker :lat-lng="[marker.lat, marker.lon]">
          <l-popup :options="{ maxWidth: 400, className: 'custom-popup' }">
            <div class="card border-0 shadow-sm">
              <img
                v-if="marker.coverImage"
                :src="marker.coverImage"
                :alt="marker.title"
                class="card-img-top rounded-top"
                style="max-height: 200px; object-fit: cover;"
              />
              <div class="card-body p-3">
                <h5 class="card-title mb-2 text-primary fw-bold">{{ marker.title }}</h5>
                <p class="card-text text-muted mb-0 small">{{ marker.description }}</p>
              </div>
            </div>
          </l-popup>
        </l-marker>
      </div>
    </l-map>
  </main>
</template>

<script>
import { LControl, LCircle, LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'

export default {
  props: {
    markers: {
      type: Array,
      default: () => []
    },
    initialParams: {
      type: Object,
      default: () => undefined
    }
  },
  components: {
    LControl,
    LMap,
    LTileLayer,
    LCircle,
    LMarker,
    LPopup,
  },
  data() {
    return {
      zoom: this.initialParams?.zoom || 16,
      center: this.initialParams?.lat && this.initialParams?.long
        ? [this.initialParams.lat, this.initialParams.long]
        : [-34.9225692, -57.9531812],
      radius: this.initialParams?.radius
        ? this.initialParams.radius * 1000
        : 500,
      radiusCenter: this.initialParams?.lat && this.initialParams?.long
        ? [this.initialParams.lat, this.initialParams.long]
        : [-34.9225692, -57.9531812],
      showErrorMessage: false,
      mapReady: false,
    }
  },
  computed: {
    showUpdateRadiusButton() {
      return this.centerHasChanged() || this.radius !== this.calculateNewRadius()
    },
  },
  methods: {
    onMapReady() {
      this.mapReady = true
      this.$nextTick(() => {
        if (this.$refs.map?.leafletObject) {
          this.$refs.map.leafletObject.invalidateSize()
        }
      })
    },
    zoomUpdated(newZoom) {
      this.zoom = newZoom
    },
    centerUpdated(newCenter) {
      // Normalizar longitud
      let lng = newCenter.lng;
      while (lng > 180) lng -= 360;
      while (lng < -180) lng += 360;

      this.center = [newCenter.lat, lng]
    },
    async updateSearchRadius() {
      this.radius = this.calculateNewRadius()
      this.radiusCenter = this.center

      this.$emit('update-map-params', {
        lat: this.radiusCenter[0],
        long: this.radiusCenter[1],
        radius: this.radius / 1000, // conversión a km
        zoom: this.zoom
      })
    },
    calculateNewRadius() {
      const minRadius = 50
      const maxRadius = 5000000
      const referenceZoom = 16
      const referenceRadius = 500

      const scale = Math.pow(2, referenceZoom - this.zoom)

      return Math.round(Math.max(minRadius, Math.min(maxRadius, referenceRadius * scale)))
    },
    centerHasChanged() {
      return this.radiusCenter[0] !== this.center[0] || this.radiusCenter[1] !== this.center[1]
    },
  }
}
</script>

<style scoped>
#map {
  height: 600px !important;
  width: 100%;
  border-radius: 6px;
  border: 1px solid #c9c0c0;
  margin-top: 1em;
}

/* Eliminar estilos por defecto del popup de Leaflet */
:deep(.leaflet-popup-content-wrapper) {
  padding: 0 !important;
  border-radius: 8px !important;
  box-shadow: 0 3px 14px rgba(0, 0, 0, 0.15) !important;
  overflow: hidden;
  min-width: 250px !important;
}

:deep(.leaflet-popup-content) {
  margin: 0 !important;
  width: 100% !important;
}

:deep(.leaflet-popup-tip) {
  background: white !important;
}

/* Personalizar markers */
:deep(.leaflet-marker-icon) {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  transition: transform 0.2s ease;
}

:deep(.leaflet-marker-icon:hover) {
  transform: scale(1.1);
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
}

/* Mejorar el botón de cierre del popup */
:deep(.leaflet-popup-close-button) {
  color: #6c757d !important;
  font-size: 20px !important;
  padding: 4px 8px !important;
}

:deep(.leaflet-popup-close-button:hover) {
  color: #dc3545 !important;
}
</style>
