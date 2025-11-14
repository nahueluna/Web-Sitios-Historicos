import { defineStore } from "pinia";
import api from "@/service/api";

function generateSlug(name) {
  return name.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '');
}

export const useSitesStore = defineStore('sites', {
  state: () => ({
    sites: [],
    loading: false,
  }),
  actions: {
    async fetchSites(params = {}) {
      this.loading = true;
      try {
        const queryParams = {
          page: params.page || 1,
          per_page: params.per_page || params.limit || 25,
        };

        console.log('Fetching sites with params:', queryParams);
        
        if (params.search) {
          const searchValue = params.search.trim();
          queryParams.name = searchValue;
          queryParams.city = searchValue;
          queryParams.province = searchValue;
        }
        if (params.order_by) queryParams.order_by = params.order_by;
        if (params.city) queryParams.city = params.city;
        if (params.province) queryParams.province = params.province;
        if (params.tags) queryParams.tags = params.tags;
        if (params.description) queryParams.description = params.description;
        if (params.lat) queryParams.lat = params.lat;
        if (params.long) queryParams.long = params.long;
        if (params.radius) queryParams.radius = params.radius;

        const response = await api.get('/api/sites', { params: queryParams });
        console.log('Fetched sites response:', response.data);
        const { data, meta } = response.data;

        const sites = data.map(site => ({
          id: site.id,
          name: site.name,
          slug: generateSlug(site.name),
          description: site.description,
          short_description: site.short_description,
          city: site.city,
          province: site.province,
          lat: site.lat,
          long: site.long,
          tags: site.tags,
          coverImage: '/placeholder.svg',
          rating: null,
        }));

        // Guardar los sites en el estado del store
        this.sites = sites;

        return { sites, total: meta.total, page: meta.page, per_page: meta.per_page };
      } catch (error) {
        console.error('[SitesStore] Error:', error);
        return { sites: [], total: 0, page: 1, per_page: 25 };
      } finally {
        this.loading = false;
      }
    },
    async fetchSiteBySlug(slug) {
      try {
        const response = await this.fetchSites({ per_page: 100 });
        return response.sites.find(site => site.slug === slug) || null;
      } catch (error) {
        console.error('[SitesStore] Error:', error);
        return null;
      }
    },
    
    async trackSiteVisit(siteId) {
      try {
        console.log(`[API] Tracked visit for site: ${siteId}`);
      } catch (error) {
        console.error('[SitesStore] Error:', error);
      }
    },
    async fetchFavoriteSites(params = {}) {
      return []; // Implementar la lógica para obtener los sitios favoritos del usuario
    }
  },
});