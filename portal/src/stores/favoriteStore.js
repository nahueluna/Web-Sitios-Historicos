import { defineStore } from "pinia";

export const useFavoritesStore = defineStore('favorites', {
  state: () => ({
    favorites: [
        {
            historicalSites: { name: "Sitio Histórico A" },
            shortDescription: "Centro colonial y museo local.",
            category: "historia"
        },
        {
            historicalSites: { name: "Sitio Histórico B" },
            shortDescription: "Ruinas con senderos interpretativos.",
            category: "arqueología"
        },
        {
            historicalSites: { name: "Sitio Histórico C" },
            shortDescription: "Casa museo con exposiciones temporales.",
            category: "cultura"
        },
        { 
            historicalSites: { name: "Sitio Histórico D" },
            shortDescription: "Iglesia barroca de gran valor arquitectónico.",
            category: "arquitectura"
        },
        {
            historicalSites: { name: "Sitio Histórico E" },
            shortDescription: "Plaza tradicional con festivales locales.",
            category: "tradición"
        },
        { 
            historicalSites: { name: "Sitio Histórico F" },
            shortDescription: "Mercado gastronómico con platos típicos.",
            category: "gastronomía"
        },
        {
            historicalSites: { name: "Sitio Histórico G" },
            shortDescription: "Paraje natural con miradores.",
            category: "naturaleza"
        }
    ],
  }),
  actions: {
    addFavorite(fav) {
      this.favorites.push(fav);
    },
    removeFavoriteByName(name) {
      this.favorites = this.favorites.filter(f => f.historicalSites?.name !== name);
    },
    getFavorites(count) {
      return this.favorites.slice(0, count);
    }
  },
});
