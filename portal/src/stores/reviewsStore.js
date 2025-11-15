import { defineStore } from "pinia";
import api from "@/service/api";

/**
 * Reviews Store
 * 
 * Gestiona las reseñas de sitios históricos.
 * Endpoint principal: GET /api/sites/<site_id>/reviews
 */

export const useReviewsStore = defineStore('reviews', {
  state: () => ({
    siteReviews: [],
    siteReviewsMeta: {
      page: 1,
      per_page: 10,
      total: 0
    },
    loading: false,
  }),
  
  getters: {
    getSiteReviews: (state) => state.siteReviews,
    getSiteReviewsMeta: (state) => state.siteReviewsMeta,
    hasMoreSiteReviews: (state) => {
      const { page, per_page, total } = state.siteReviewsMeta;
      return (page * per_page) < total;
    },
    averageRating: (state) => {
      if (state.siteReviews.length === 0) return 0;
      const sum = state.siteReviews.reduce((acc, review) => acc + review.rating, 0);
      return (sum / state.siteReviews.length).toFixed(1);
    },
    reviewCount: (state) => state.siteReviewsMeta.total
  },
  
  actions: {
    /**
     * Obtiene las reseñas aprobadas de un sitio histórico
     * @param {number} siteId - ID del sitio histórico
     * @param {object} params - Parámetros de paginación { page, per_page }
     * @returns {object} { reviews, meta }
     */
    async fetchReviewsBySite(siteId, params = {}) {
      this.loading = true;
      try {
        const queryParams = {
          page: params.page || 1,
          per_page: params.per_page || 10,
        };

        console.log('Reviews Store - Fetching reviews for site:', siteId, queryParams);

        const response = await api.get(`/api/sites/${siteId}/reviews`, { 
          params: queryParams 
        });

        console.log('Reviews Store - Response:', response.data);

        const { data: reviewsData, meta } = response.data;

        // Transformar las reseñas del backend al formato interno
        const transformedReviews = reviewsData.map(review => ({
          id: review.id,
          siteId: review.site_id,
          rating: review.rating,
          comment: review.comment,
          userName: review.user_name,
          insertedAt: review.inserted_at,
        }));

        // Actualizar estado
        if (queryParams.page > 1) {
          // Agregar reseñas para paginación
          this.siteReviews = [...this.siteReviews, ...transformedReviews];
        } else {
          // Reemplazar para primera página
          this.siteReviews = transformedReviews;
        }
        this.siteReviewsMeta = meta;

        console.log('Reviews Store - Loaded:', transformedReviews.length, 'Total:', meta.total);

        return {
          reviews: transformedReviews,
          meta: meta
        };

      } catch (error) {
        console.error('Reviews Store - Error:', error);

        // Estado vacío en caso de error
        this.siteReviews = [];
        this.siteReviewsMeta = { page: 1, per_page: 10, total: 0 };

        return {
          reviews: [],
          meta: { page: 1, per_page: 10, total: 0 }
        };
      } finally {
        this.loading = false;
      }
    },

    /**
     * Limpia las reseñas del store
     */
    clearReviews() {
      this.siteReviews = [];
      this.siteReviewsMeta = { page: 1, per_page: 10, total: 0 };
    }
  }
});
