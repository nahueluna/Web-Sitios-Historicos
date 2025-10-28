export interface Site {
  id: string
  name: string
  slug: string
  description: string
  coverImage: string
  city: string
  province: string
  rating?: number
  visitCount?: number
  createdAt: string
  isFavorite?: boolean
}

export type SortOption = 'top-rated' | 'most-visited' | 'recently-added' | 'favorites'

export interface FetchSitesParams {
  search?: string
  sort?: SortOption
  limit?: number
}

export interface FeaturedSitesResponse {
  sites: Site[]
  total: number
}
