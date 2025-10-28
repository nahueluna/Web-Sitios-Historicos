import { defineStore } from "pinia";

export const useReviewsStore = defineStore('reviews', {
  state: () => ({
    reviews: [
        {
            historicalSites: { name: "Sitio Histórico A" },
            text: "Una experiencia maravillosa, muy educativa.",
            rating: 5
        },
        {
            historicalSites: { name: "Sitio Histórico B" },
            text: "Interesante pero un poco desorganizado.",
            rating: 3
        },
        {
            historicalSites: { name: "Sitio Histórico C" },
            text: "No cumplió con mis expectativas.",
            rating: 2
        },
        { 
            historicalSites: { name: "Sitio Histórico D" },
            text: "Excelente conservación y guías muy amables.",
            rating: 4
        },
        {
            historicalSites: { name: "Sitio Histórico E" },
            text: "Un lugar fascinante lleno de historia.",
            rating: 5
        },
        { 
            historicalSites: { name: "Sitio Histórico F" },
            text: "Demasiado turístico, perdió su encanto.",
            rating: 2
        },
        {
            historicalSites: { name: "Sitio Histórico G" },
            text: "Una joya escondida, vale la pena visitarlo.",
            rating: 4
        }
    ],
  }),
  actions: {
    addReview(review) {
      this.reviews.push(review);
    },
    removeReview(reviewId) {
      this.reviews = this.reviews.filter(review => review.id !== reviewId);
    },
    getReviews(count) {
      return this.reviews.slice(0, count);
    }
  },
});
