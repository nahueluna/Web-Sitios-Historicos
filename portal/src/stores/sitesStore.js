import { defineStore } from "pinia";
import api from "@/service/api";
import qs from 'qs'

export const useSitesStore = defineStore('sites', {
  state: () => ({
    sites: [],
    loading: false,
    allTags: [],
  }),
  actions: {
    async fetchSites(params = {}) {
      this.loading = true;
      try {
        const queryParams = {
          page: params.page || 1,
          per_page: params.per_page || params.limit || 25,
        };

        if (params.search) {
          const searchValue = params.search.trim();
          queryParams.name = searchValue;
          queryParams.description = searchValue;
        }
        if (params.order_dir) queryParams.order_dir = params.order_dir;
        if (params.order_by) queryParams.order_by = params.order_by;
        if (params.city) queryParams.city = params.city;
        if (params.province) queryParams.province = params.province;
        if (params.favorites) queryParams.favorites = params.favorites;
        if (params.tags) queryParams.tags = params.tags;
        if (params.lat) queryParams.lat = params.lat;
        if (params.long) queryParams.long = params.long;
        if (params.radius) queryParams.radius = params.radius;

        const response = await api.get('/api/sites', {
          params: queryParams,
          paramsSerializer: params => {
            return qs.stringify(params, { arrayFormat: 'comma' });
          }
        });
        const { data, meta } = response.data;

        const sites = data.map(site => ({
          id: site.id,
          name: site.name,
          description: site.description,
          short_description: site.short_description,
          city: site.city,
          province: site.province,
          lat: site.lat,
          long: site.long,
          tags: site.tags,
          state: site.state_of_conservation,
          coverImage: site.thumbnail_url || '/placeholder.svg',
          rating: site.rating || null,
        }));

        // Guardar los sites en el estado del store
        this.sites = sites;

        return { sites, total: meta.total, page: meta.page, per_page: meta.per_page };
      } catch (error) {
        console.error('[SitesStore] Error:', error);

        const details = error?.response?.data?.error?.details;
        if(error.status === 400 && (details?.long || details?.lat || details?.radius)) {
          throw error;
        }

        return { sites: [], total: 0, page: 1, per_page: 25 };
      } finally {
        this.loading = false;
      }
    },
    async fetchSiteById(site_id) {
      try {
        const response = await api.get(`/api/sites/${site_id}`);
        return response.data;
      } catch (error) {
        console.error('[SitesStore] Error:', error);
        return null;
      }
    },
    async fetchAllTags() {
      try {
        const response = await api.get('/api/tags')
        this.allTags = response.data.map(tag => ({
          id: tag.id,
          name: tag.name,
        }))
        return this.allTags
      } catch (error) {
        console.error("Error loading tags:", error)
        return []
      }
    },

  },
});
