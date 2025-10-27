import type { Site, SortOption, FeaturedSitesResponse } from "../types"

// Mock data for demonstration - Historic sites from Argentina
const MOCK_SITES: Site[] = [
  {
    id: "1",
    name: "Casa Rosada",
    slug: "casa-rosada",
    coverImage: "/historic-plaza.jpg",
    city: "Buenos Aires",
    province: "Buenos Aires",
    rating: 4.8,
    visitCount: 25420,
    createdAt: "2024-01-15T10:00:00Z",
    description: "Sede del Poder Ejecutivo Nacional y símbolo histórico de la República Argentina",
  },
  {
    id: "2",
    name: "Cabildo de Buenos Aires",
    slug: "cabildo-buenos-aires",
    coverImage: "/old-quebec-city-historic.jpg",
    city: "Buenos Aires",
    province: "Buenos Aires",
    rating: 4.6,
    visitCount: 18350,
    createdAt: "2024-02-20T14:30:00Z",
    description: "Edificio colonial que fue sede del gobierno durante la época virreinal",
  },
  {
    id: "3",
    name: "Ruinas de San Ignacio Miní",
    slug: "ruinas-san-ignacio-mini",
    coverImage: "/coastal-lighthouse.jpg",
    city: "San Ignacio",
    province: "Misiones",
    rating: 4.9,
    visitCount: 22870,
    createdAt: "2024-03-10T09:15:00Z",
    description: "Patrimonio de la Humanidad UNESCO, antigua misión jesuítica guaraní",
  },
  {
    id: "4",
    name: "Quebrada de Humahuaca",
    slug: "quebrada-humahuaca",
    coverImage: "/mountain-trail.png",
    city: "Humahuaca",
    province: "Jujuy",
    rating: 4.9,
    visitCount: 20200,
    createdAt: "2024-01-25T11:45:00Z",
    description: "Valle montañoso con 10.000 años de historia, Patrimonio de la Humanidad",
  },
  {
    id: "5",
    name: "Manzana Jesuítica",
    slug: "manzana-jesuitica",
    coverImage: "/urban-art-district.jpg",
    city: "Córdoba",
    province: "Córdoba",
    rating: 4.7,
    visitCount: 16900,
    createdAt: "2024-02-05T16:20:00Z",
    description: "Conjunto de edificios históricos jesuitas, Patrimonio de la Humanidad UNESCO",
  },
  {
    id: "6",
    name: "Cueva de las Manos",
    slug: "cueva-manos",
    coverImage: "/river-gardens.jpg",
    city: "Perito Moreno",
    province: "Santa Cruz",
    rating: 4.8,
    visitCount: 14650,
    createdAt: "2024-03-15T13:00:00Z",
    description: "Arte rupestre con más de 9.000 años de antigüedad, Patrimonio de la Humanidad",
  },
]

export async function fetchSites(params: {
  sort?: SortOption
  search?: string
  limit?: number
}): Promise<FeaturedSitesResponse> {
  // Simulate API delay
  await new Promise((resolve) => setTimeout(resolve, 500))

  let filteredSites = [...MOCK_SITES]

  // Apply search filter
  if (params.search) {
    const query = params.search.toLowerCase()
    filteredSites = filteredSites.filter(
      (site) =>
        site.name.toLowerCase().includes(query) ||
        site.city.toLowerCase().includes(query) ||
        site.province.toLowerCase().includes(query),
    )
  }

  // Apply sorting
  if (params.sort) {
    switch (params.sort) {
      case "top-rated":
        filteredSites.sort((a, b) => (b.rating || 0) - (a.rating || 0))
        break
      case "most-visited":
        filteredSites.sort((a, b) => (b.visitCount || 0) - (a.visitCount || 0))
        break
      case "recently-added":
        filteredSites.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
        break
      case "favorites":
        filteredSites = filteredSites.filter((site) => site.isFavorite)
        break
    }
  }

  // Apply limit
  if (params.limit) {
    filteredSites = filteredSites.slice(0, params.limit)
  }

  return {
    sites: filteredSites,
    total: filteredSites.length,
  }
}

export async function fetchSiteBySlug(slug: string): Promise<Site | null> {
  await new Promise((resolve) => setTimeout(resolve, 300))
  return MOCK_SITES.find((site) => site.slug === slug) || null
}

export async function trackSiteVisit(siteId: string): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve, 100))
  console.log(`[API] Tracked visit for site: ${siteId}`)
}
