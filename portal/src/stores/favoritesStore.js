import { defineStore } from "pinia";
import api from "@/service/api";
import { useSitesStore } from "@/stores/sites";

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

        // Update local state
        this.favoriteIds.add(siteId);

        // Optional: re-fetch favorites if you need complete objects
        // await this.fetchFavorites();

        return response.data.message;
      } catch (error) {
        console.error("[FavoritesStore] Error adding favorite:", error);
        return null;
      }
    },

    // Remove from favorites
    async removeFavorite(siteId) {
      try {
        const response = await api.delete(`/api/favorites/${siteId}`);

        // Update local state
        this.favoriteIds.delete(siteId);

        // Optional: re-fetch favorites
        // await this.fetchFavorites();

        return response.data.message;
      } catch (error) {
        console.error("[FavoritesStore] Error removing favorite:", error);
        return null;
      }
    },

    // Toggle favorite state
    async toggleFavorite(siteId) {
      if (this.favoriteIds.has(siteId)) {
        return await this.removeFavorite(siteId);
      } else {
        return await this.addFavorite(siteId);
      }
    },
  },
});
