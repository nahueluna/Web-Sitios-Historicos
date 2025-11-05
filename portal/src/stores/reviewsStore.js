import { defineStore } from "pinia";
import api from "@/service/api";
import { useSitesStore } from "@/stores/sitesStore";

// Mock reviews data for demonstration
const MOCK_REVIEWS = [
  {
    id: "review-1",
    siteId: "1", // Casa Rosada
    userId: "user1", // Juan Pérez
    text: "¡Una experiencia increíble! La Casa Rosada es mucho más impresionante en persona. La historia que representa es fascinante y el guía turístico fue excelente explicando todos los detalles históricos.",
    rating: 5,
    createdAt: "2024-10-15T14:30:00Z"
  },
  {
    id: "review-2",
    siteId: "1", // Casa Rosada
    userId: "user1", // Juan Pérez
    text: "Visité la Casa Rosada durante mi viaje a Buenos Aires. El edificio es majestuoso y la visita guiada realmente te transporta a través del tiempo. Recomiendo ir temprano para que no te choreen el lugar.",
    rating: 4,
    createdAt: "2024-09-22T10:15:00Z"
  },
  {
    id: "review-3",
    siteId: "3", // Ruinas de San Ignacio Miní
    userId: "user2", // María García
    text: "Las ruinas jesuíticas son un tesoro escondido. La paz y tranquilidad del lugar, combinada con la rica historia, hacen de esta visita una experiencia inolvidable. El guía local no sabe nada.",
    rating: 3,
    createdAt: "2024-08-10T16:45:00Z"
  }
];

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
        const apiReviews = response.data.map(review => ({
          ...review,
          siteName: this.getSiteName(review.siteId),
          userName: this.getUserName(review.userId)
        }));

        // Combine API reviews with mock reviews
        const allReviews = [...MOCK_REVIEWS, ...apiReviews].map(review => ({
          ...review,
          siteName: this.getSiteName(review.siteId),
          userName: this.getUserName(review.userId)
        }));

        this.reviews = allReviews;
      } catch (error) {
        console.error('Error fetching reviews:', error);
        // If API fails, at least show mock reviews
        this.reviews = MOCK_REVIEWS.map(review => ({
          ...review,
          siteName: this.getSiteName(review.siteId),
          userName: this.getUserName(review.userId)
        }));
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
        const apiReviews = response.data.map(review => ({
          ...review,
          siteName: this.getSiteName(review.siteId),
          userName: this.getUserName(review.userId)
        }));

        // Get mock reviews for this site
        const mockReviewsForSite = MOCK_REVIEWS.filter(review => review.siteId === siteId).map(review => ({
          ...review,
          siteName: this.getSiteName(review.siteId),
          userName: this.getUserName(review.userId)
        }));

        // Combine API reviews with mock reviews for this site
        const allReviewsForSite = [...mockReviewsForSite, ...apiReviews];

        // Add to store if not already present
        allReviewsForSite.forEach(review => {
          if (!this.reviews.find(r => r.id === review.id)) {
            this.reviews.push(review);
          }
        });

        return allReviewsForSite;
      } catch (error) {
        console.error('Error fetching reviews by site:', error);
        // If API fails, return mock reviews for this site
        return MOCK_REVIEWS.filter(review => review.siteId === siteId).map(review => ({
          ...review,
          siteName: this.getSiteName(review.siteId),
          userName: this.getUserName(review.userId)
        }));
      }
    },
    getReviewsByUser(userId) {
      return this.reviews.filter(review => review.userId === userId);
    },
    getSiteName(siteId) {
      const sitesStore = useSitesStore();
      const site = sitesStore.sites.find(s => s.id === siteId);
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
    },
    assignMockReviewsToUser(userId) {
      // Actualizar las reseñas hardcodeadas para que pertenezcan al usuario logueado
      this.reviews = this.reviews.map(review => {
        if (review.id.startsWith('review-')) { // Solo las reseñas hardcodeadas
          return {
            ...review,
            userId: userId,
            userName: this.getUserName(userId)
          };
        }
        return review;
      });
    }
  },
});
