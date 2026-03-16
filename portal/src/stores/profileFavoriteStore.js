import { defineStore } from "pinia";
import api from "@/service/api";

export const useProfileFavoriteStore = defineStore('profile_favorites', {
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

    getFavorites() {
      return this.favorites
    },
  },
});
