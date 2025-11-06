import { defineStore } from "pinia";
import api from "@/service/api";
import { useSitesStore } from "@/stores/sitesStore";

/**
 * Reviews Store
 *
 * Estado actual:
 * - ✅ fetchReviewsBySite: Implementado con nuevo endpoint /api/historic-sites/<site_id>/reviews
 * - ⚠️ fetchReviews, addReview, removeReview: Usan endpoints antiguos (/reviews) - necesitan actualización
 * - ⚠️ getReviewsByUser: Funciona con datos locales - necesita endpoint de backend para reseñas por usuario
 *
 * TODO: Actualizar funciones obsoletas cuando estén disponibles los nuevos endpoints del backend
 */

export const useReviewsStore = defineStore('reviews', {
  state: () => ({
    reviews: [], // Mantener para compatibilidad con componentes existentes
    siteReviews: [], // Reviews específicas de un sitio
    siteReviewsMeta: { // Metadata de paginación para reviews de sitio
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
    }
  },
  actions: {
    // TODO: Esta función usa el endpoint antiguo /reviews - necesita actualizarse cuando esté disponible el nuevo endpoint
    async fetchReviews() {
      this.loading = true;
      try {
        const response = await api.get('/reviews');
        const apiReviews = response.data.map(review => ({
          ...review,
          siteName: this.getSiteName(review.siteId),
          userName: this.getUserName(review.userId)
        }));

        this.reviews = apiReviews;
      } catch (error) {
        console.error('Error fetching reviews:', error);
        this.reviews = [];
      } finally {
        this.loading = false;
      }
    },

    // TODO: Esta función usa el endpoint antiguo /reviews - necesita actualizarse cuando esté disponible el nuevo endpoint
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

    // TODO: Esta función usa el endpoint antiguo /reviews/{id} - necesita actualizarse cuando esté disponible el nuevo endpoint
    async removeReview(reviewId) {
      try {
        await api.delete(`/reviews/${reviewId}`);
        this.reviews = this.reviews.filter(review => review.id !== reviewId);
      } catch (error) {
        console.error('Error removing review:', error);
        throw error;
      }
    },
    async fetchReviewsBySite(siteId, params = {}) {
      this.loading = true;
      try {
        const queryParams = {
          page: params.page || 1,
          per_page: params.per_page || 10,
        };

        console.log('📤 [Reviews Store] Fetching reviews for site:', siteId, 'with params:', queryParams);

        const response = await api.get(`/api/historic-sites/${siteId}/reviews`, { params: queryParams });

        console.log('📥 [Reviews Store] Response received:', response.data);

        const { data: reviewsData, meta } = response.data;

        // Transformar las reseñas del backend al formato interno
        const transformedReviews = reviewsData.map(review => ({
          id: review.id,
          siteId: siteId,
          userId: review.user_id,
          text: review.comment,
          rating: review.rating,
          createdAt: review.created_at,
          // Agregar información adicional si está disponible
          userName: review.user_name || this.getUserName(review.user_id),
          siteName: this.getSiteName(siteId)
        }));

        // Actualizar estado
        if (queryParams.page > 1) {
          // Agregar reseñas a las existentes para paginación
          this.siteReviews = [...this.siteReviews, ...transformedReviews];
        } else {
          // Reemplazar reseñas para la primera página
          this.siteReviews = transformedReviews;
        }
        this.siteReviewsMeta = meta;

        console.log('✅ [Reviews Store] Reviews loaded:', transformedReviews.length, 'Total:', meta.total);

        return {
          reviews: transformedReviews,
          meta: meta
        };

      } catch (error) {
        console.error('❌ [Reviews Store] Error fetching reviews by site:', error);

        // En caso de error, devolver datos vacíos pero con estructura correcta
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
    getReviewsByUser(userId) {
      return this.reviews.filter(review => review.userId === userId);
    },
    getSiteName(siteId) {
      const sitesStore = useSitesStore();
      const site = sitesStore.sites.find(s => s.id === siteId);
      return site ? site.name : 'Sitio Desconocido';
    },
    getUserName(userId) {
      // En una implementación real, esto vendría de un servicio de usuarios
      return `Usuario ${userId}`;
    }
  }
});
