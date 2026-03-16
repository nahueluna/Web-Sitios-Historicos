import { defineStore } from 'pinia'
import api from '@/service/api'

export const useProfileReviewStore = defineStore('profileReview', {
    state: () => ({
        profile_reviews: [],
    }),
    actions: {
        async loadAllReviews(userId) {
            const id = userId
            const response = await api.get(`/api/reviews/users/${id}/reviews`)
            this.profile_reviews = response.data.reviews ?? []
            return this.profile_reviews
        },

        // Carga paginada de reseñas del usuario
        async loadReviews(userId, page = 1, per_page = 12) {
            const id = userId
            const response = await api.get(`/api/reviews/users/${id}/reviews`, {
                params: { page, per_page }
            })
            const data = response.data || {}
            this.profile_reviews = data.reviews ?? []
            return {
                reviews: this.profile_reviews,
                total: data.total ?? this.profile_reviews.length,
                page: data.page ?? page,
                per_page: data.per_page ?? per_page,
            }
        },

        async loadRecentReviews(userId, count = 4) {
            const reviews = await this.loadAllReviews(userId)
            this.profile_reviews = Array.isArray(reviews) ? reviews.slice(0, count) : []
            return this.profile_reviews
        },

        getReviews() {
            return this.profile_reviews
        },
    }
})
