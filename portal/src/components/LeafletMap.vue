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
        <button v-if="showUpdateRadiusButton" @click="updateSearchRadius">
          Actualizar radio de búsqueda
        </button>
      </l-control>
      <l-circle :lat-lng="radiusCenter" :radius="radius" color="blue" />
      <div v-for="marker in markers" :key="marker.id">
        <l-marker :lat-lng="[marker.lat, marker.lon]">
          <l-popup>
            <h3>{{ marker.title }}</h3>
            <p>
              <img
                :src="marker.coverImage || '/placeholder.svg'"
                :alt="marker.title"
                class="card-img-top mb-3"
              />
              <span>{{ marker.description }}</span>
            </p>
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
      zoom: 16,
      center: [-34.9225692, -57.9531812],
      radius: 500,
      radiusCenter: [-34.9225692, -57.9531812],
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
      this.center = [newCenter.lat, newCenter.lng]
    },
    async updateSearchRadius() {
      this.radius = this.calculateNewRadius()
      this.radiusCenter = this.center

      this.$emit('update-map-params', {
        lat: this.radiusCenter[0],
        long: this.radiusCenter[1],
        radius: this.radius / 1000 // conversión a km
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
  border: 1px solid #ddd;
  margin-top: 1em;
}
</style>
