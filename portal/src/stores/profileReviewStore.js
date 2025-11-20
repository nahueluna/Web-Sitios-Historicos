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

        // pequeña utilidad para obtener la lista memorizada
        getReviews() {
            return this.profile_reviews
        },
        getHardcodedReviews() {
            return [
                {
                    "id": 1,
                    "content": "Excelente lugar, lo recomiendo para fotos y paseos.",
                    "rating": 5,
                    "status": { "name": "APPROVED", "value": "Aprobada" },
                    "inserted_at": "01-06-2024",
                    "updated_at": "2024-06-01",
                    "historic_site": { "id": 1, "name": "Sitio Ejemplo 1", "cover": "/placeholder.svg" },
                    "rejection_reason": null
                },
                {
                    "id": 2,
                    "content": "Buena visita, atención amable pero algo de cola para entrar.",
                    "rating": 4,
                    "status": { "name": "APPROVED", "value": "Aprobada" },
                    "inserted_at": "15-05-2024",
                    "updated_at": "2024-05-15",
                    "historic_site": { "id": 2, "name": "Sitio Ejemplo 2", "cover": "/placeholder.svg" },
                    "rejection_reason": null
                },
                {
                    "id": 3,
                    "content": "Interesante, con buenas placas informativas, ideal para familias.",
                    "rating": 4,
                    "status": { "name": "APPROVED", "value": "Aprobada" },
                    "inserted_at": "03-04-2024",
                    "updated_at": "2024-04-03",
                    "historic_site": { "id": 3, "name": "Sitio Ejemplo 3", "cover": "/placeholder.svg" },
                    "rejection_reason": null
                },
                {
                    "id": 4,
                    "content": "No me gustó mucho, esperaba más información histórica.",
                    "rating": 2,
                    "status": { "name": "APPROVED", "value": "Aprobada" },
                    "inserted_at": "20-03-2024",
                    "updated_at": "2024-03-20",
                    "historic_site": { "id": 4, "name": "Sitio Ejemplo 4", "cover": "/placeholder.svg" },
                    "rejection_reason": null
                }
            ]
        }
    }
})
