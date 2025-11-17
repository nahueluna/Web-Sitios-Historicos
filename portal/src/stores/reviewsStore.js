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
    error: null, // Nuevo estado para errores
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
    reviewCount: (state) => state.siteReviewsMeta.total,
    getError: (state) => state.error, // Nuevo getter para el error
  },
  
  actions: {
    async fetchReviewsBySite(siteId, params = {}) {
      this.loading = true;
      this.error = null; // Limpiar error anterior
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
        console.log('Reviews Store - Response Data:', response.data.data);
        console.log('Reviews Store - Response meta:', response.data.meta);
        const { data: reviewsData, meta } = response.data;


        // Transformar las reseñas del backend al formato interno
        const transformedReviews = reviewsData.map(review => ({
          id: review.id,
          siteId: review.site_id,
          rating: review.rating,
          content: review.comment,
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

        // Capturar error específico del backend
        if (error.response?.status === 403 && error.response?.data?.error) {
          this.error = error.response.data.error;
        }

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

    // Agregar una nueva reseña para un sitio
    async addReview(siteId, reviewData) {
      this.loading = true;
      this.error = null;

      try {
        const payload = {
          rating: reviewData.rating,
          content: reviewData.content // backend expects 'content' field
        };
        console.log('Reviews Store - Adding review for site:', siteId, payload);

        const response = await api.post(`/api/sites/${siteId}/reviews`, payload);
        console.log('Reviews Store - Add review response:', response.data);

        // Después de agregar, recargar las reseñas desde la primera página
        await this.fetchReviewsBySite(siteId, { page: 1, per_page: this.siteReviewsMeta.per_page });
        
        return response.data;

      } catch (error) {
        console.error('Reviews Store - Error adding review:', error);
        if (error.response?.status === 401) {
          this.error = { message: 'Debes iniciar sesión para agregar una reseña.' };
        } else if (error.response?.data?.error) {
          this.error = error.response.data.error;
        } else {
          this.error = { message: 'Error al agregar la reseña. Por favor, intenta de nuevo.' };
        }
        throw error;
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
      this.error = null; // Limpiar error también
    }
  }
});
