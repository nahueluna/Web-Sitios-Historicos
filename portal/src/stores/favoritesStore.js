import { defineStore } from "pinia";
import api from "@/service/api";

export const useFavoritesStore = defineStore('favorites', {
  state: () => ({
    favorites: [],      // Array of site objects returned by GET /favorites
    favoriteIds: new Set(), // Fast lookups → store only IDs here too
    loading: false,
  }),

  getters: {
    isFavorite: (state) => (siteId) => state.favoriteIds.has(siteId),
  },

  actions: {
    // Fetch all favorites from backend
    async fetchFavorites() {
      try {
        this.loading = true;
        const response = await api.get('/api/favorites');

        const sites = response.data.favorites || [];

        this.favorites = sites;
        this.favoriteIds = new Set(sites.map(s => s.id));

        return sites;
      } catch (error) {
        console.error("[FavoritesStore] Error fetching favorites:", error);
        return [];
      } finally {
        this.loading = false;
      }
    },

    // Check if a site is favorite (server check)
    async checkFavorite(siteId) {
      try {
        const response = await api.get(`/api/favorites/check/${siteId}`);
        const isFav = response.data.is_favorite;

        if (isFav) {
          this.favoriteIds.add(siteId);
        } else {
          this.favoriteIds.delete(siteId);
        }

        return isFav;
      } catch (error) {
        console.error(`[FavoritesStore] Error checking favorite (${siteId}):`, error);
        return false;
      }
    },

    // Add to favorites
    async addFavorite(siteId) {
      try {
        const response = await api.post(`/api/favorites/${siteId}`);

        if (response.status === 200 || response.status === 201) {
          this.favoriteIds.add(siteId);
          return true;  // success
        }

        return false;  // unexpected status
      } catch (error) {
        console.error("[FavoritesStore] Error adding favorite:", error);
        return null;
      }
    },

    // Remove from favorites
    async removeFavorite(siteId) {
      try {
        const response = await api.delete(`/api/favorites/${siteId}`);

        if (response.status === 200) {
          this.favoriteIds.delete(siteId);
          return true; // success
        }

        return false;
      } catch (error) {
        console.error("[FavoritesStore] Error removing favorite:", error);
        return null;
      }
    },
  },
});
