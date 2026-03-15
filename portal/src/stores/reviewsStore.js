import { defineStore } from "pinia";
import api from "@/service/api";

/**
 * Reviews Store
 * 
 * Gestiona las reseñas de sitios históricos.
 * Endpoints:
 * - GET /api/sites/<site_id>/reviews
 * - POST /api/sites/<site_id>/reviews
 * - PUT /api/sites/<site_id>/reviews/<review_id>
 * - DELETE /api/sites/<site_id>/reviews/<review_id>
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
    // Obtener reseñas para un sitio específico
    async fetchReviewsBySite(siteId, params = {}) {
      this.loading = true;
      this.error = null;
      try {
        const queryParams = {
          page: params.page || 1,
          per_page: params.per_page || 10,
        };

        const response = await api.get(`/api/sites/${siteId}/reviews`, { 
          params: queryParams 
        });

        const { data: reviewsData, meta } = response.data;

        const transformedReviews = reviewsData.map(review => ({
          id: review.id,
          userId: review.user_id,
          siteId: review.site_id,
          rating: review.rating,
          content: review.content,
          userName: review.user_name,
          insertedAt: review.inserted_at,
        }));

        this.siteReviews = transformedReviews;
        this.siteReviewsMeta = meta;

        return {
          reviews: transformedReviews,
          meta: meta
        };

      } catch (error) {
        console.error('Error al cargar reseñas:', error);

        if (error.response?.status === 403 && error.response?.data?.error) {
          this.error = error.response.data.error;
        }

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
          content: reviewData.content
        };

        const response = await api.post(`/api/sites/${siteId}/reviews`, payload);

        await this.fetchReviewsBySite(siteId, { page: 1, per_page: this.siteReviewsMeta.per_page });
        
        return response.data;

      } catch (error) {
        console.error('Error al agregar reseña:', error);
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

    // Actualizar una reseña existente
    async updateReview(siteId, reviewId, reviewData) {
      this.loading = true;
      this.error = null;
      try {
        const payload = {
          rating: reviewData.rating,
          content: reviewData.content
        };

        const response = await api.put(`/api/sites/${siteId}/reviews/${reviewId}`, payload);

        await this.fetchReviewsBySite(siteId, { page: 1, per_page: this.siteReviewsMeta.per_page });
        
        return response.data;

      } catch (error) {
        console.error('Error al actualizar reseña:', error);
        
        if (error.response?.status === 403) {
          this.error = { message: 'No tienes permiso para editar esta reseña.' };
        } else if (error.response?.status === 404) {
          this.error = { message: 'La reseña no existe o fue eliminada.' };
        } else if (error.response?.data?.error) {
          this.error = error.response.data.error;
        } else {
          this.error = { message: 'Error al actualizar la reseña. Por favor, intenta de nuevo.' };
        }
        throw error;
      } finally {
        this.loading = false;
      }
    },

    // Eliminar una reseña
    async removeReview(siteId, reviewId) {
      this.loading = true;
      this.error = null;
      try {
        await api.delete(`/api/sites/${siteId}/reviews/${reviewId}`);

        await this.fetchReviewsBySite(siteId, { page: 1, per_page: this.siteReviewsMeta.per_page });
        
        return true;

      } catch (error) {
        console.error('Error al eliminar reseña:', error);
        if (error.response?.data?.error) {
          this.error = error.response.data.error;
        } else {
          this.error = { message: 'Error al eliminar la reseña. Por favor, intenta de nuevo.' };
        }
        throw error;
      } finally {
        this.loading = false;
      }
    },

    // Limpia las reseñas del store
    clearReviews() {
      this.siteReviews = [];
      this.siteReviewsMeta = { page: 1, per_page: 10, total: 0 };
      this.error = null;
    }
  }
});
