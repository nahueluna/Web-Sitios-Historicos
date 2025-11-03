import { defineStore } from "pinia";
import api from "@/service/api";
import { MOCK_SITES } from "@/api/sites";

export const useReviewsStore = defineStore('reviews', {
  state: () => ({
    reviews: [],
    loading: false,
  }),
  actions: {
    async fetchReviews() {
      this.loading = true;
      try {
        const response = await api.get('/reviews');
        this.reviews = response.data.map(review => ({
          ...review,
          siteName: this.getSiteName(review.siteId),
          userName: this.getUserName(review.userId)
        }));
      } catch (error) {
        console.error('Error fetching reviews:', error);
      } finally {
        this.loading = false;
      }
    },
    async addReview(reviewData) {
      try {
        const response = await api.post('/reviews', reviewData);
        const reviewWithSiteName = {
          ...response.data,
          siteName: this.getSiteName(response.data.siteId),
          userName: this.getUserName(response.data.userId)
        };
        this.reviews.push(reviewWithSiteName);
      } catch (error) {
        console.error('Error adding review:', error);
        throw error;
      }
    },
    async removeReview(reviewId) {
      try {
        await api.delete(`/reviews/${reviewId}`);
        this.reviews = this.reviews.filter(review => review.id !== reviewId);
      } catch (error) {
        console.error('Error removing review:', error);
        throw error;
      }
    },
    async fetchReviewsBySite(siteId) {
      try {
        const response = await api.get(`/sites/${siteId}/reviews`);
        const reviewsWithSiteName = response.data.map(review => ({
          ...review,
          siteName: this.getSiteName(review.siteId),
          userName: this.getUserName(review.userId)
        }));
        // Add to store if not already present
        reviewsWithSiteName.forEach(review => {
          if (!this.reviews.find(r => r.id === review.id)) {
            this.reviews.push(review);
          }
        });
        return reviewsWithSiteName;
      } catch (error) {
        console.error('Error fetching reviews by site:', error);
        return [];
      }
    },
    getReviewsByUser(userId) {
      return this.reviews.filter(review => review.userId === userId);
    },
    getSiteName(siteId) {
      const site = MOCK_SITES.find(s => s.id === siteId);
      return site ? site.name : 'Sitio Desconocido';
    },
    getUserName(userId) {
      // Mock user names - in real app, this would come from user service
      const mockUsers = {
        'user1': 'Juan Pérez',
        'user2': 'María García',
        'user3': 'Carlos López'
      };
      return mockUsers[userId] || 'Usuario Anónimo';
    }
  },
});
