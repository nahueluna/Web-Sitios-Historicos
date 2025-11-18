/**
 * Utilidad para transformar datos de reseñas del formato backend (snake_case)
 * al formato frontend (camelCase)
 * 
 * @param {Object} review - Reseña en formato backend
 * @returns {Object} Reseña en formato frontend
 */
export const transformReview = (review) => ({
  id: review.id,
  userId: review.user_id,
  siteId: review.historic_site?.id || review.site_id || null,
  siteName: review.historic_site?.name || 'Sitio desconocido',
  rating: review.rating,
  content: review.content,
  userName: review.user?.email || review.user_name || 'Usuario',
  insertedAt: review.inserted_at,
})

/**
 * Transforma un array de reseñas
 * 
 * @param {Array} reviews - Array de reseñas en formato backend
 * @returns {Array} Array de reseñas en formato frontend
 */
export const transformReviews = (reviews) => {
  if (!Array.isArray(reviews)) return []
  return reviews.map(transformReview)
}
