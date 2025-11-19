import { defineStore } from "pinia";
import api from "@/service/api";

export const useFavoritesStore = defineStore('profile_favorites', {
  state: () => ({
    favorites: [],
  }),
  actions: {
    async loadAllFavorites() {
      const response = await api.get(`/api/favorites/`)
      this.favorites = response.data.favorites ?? []
      return this.favorites
        },

        async loadRecentFavorites(count = 4) {
            const favorites = await this.loadAllFavorites()
            this.favorites = Array.isArray(favorites) ? favorites.slice(0, count) : []
            return this.favorites
        },

        // pequeña utilidad para obtener la lista memorizada
        getFavorites() {
            return this.favorites
        },
        getHardcodedFavorites() {
          return [
    {
      "id": 1,
      "name": "Nombre de sitio 1",
      "city": "Ciudad A",
      "province": "Provincia A",
      "rating": 4.5,
      "coverImage": "/placeholder.svg"
    },
    {
      "id": 2,
      "name": "Nombre de sitio 2",
      "city": "Ciudad B",
      "province": "Provincia B",
      "rating": 4.0,
      "coverImage": "/placeholder.svg"
    },
    {
      "id": 3,
      "name": "Nombre de sitio 3",
      "city": "Ciudad C",
      "province": "Provincia C",
      "rating": 3.8,
      "coverImage": "/placeholder.svg"
    },
    {
      "id": 4,
      "name": "Nombre de sitio 4",
      "city": "Ciudad D",
      "province": "Provincia D",
      "rating": 5.0,
      "coverImage": "/placeholder.svg"
    }
  ]

        }
  },
});
