import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ProfileView from '@/views/user/ProfileView.vue'
import { useSessionStore } from '@/stores/sessionStore'
import { useLoginModalStore } from '@/stores/LoginModalStore'
import HomeView from '@/views/HomeView.vue'
import ProfileView from '@/views/user/ProfileView.vue'
import { useSessionStore } from '@/stores/sessionStore'
import { useLoginModalStore } from '@/stores/LoginModalStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: false }
    },
    {
      path: '/sites',
      name: 'sites',
      component: () => import('../views/SitesList.vue'),
    },
    {
      path: '/sites/:slug',
      name: 'site-detail',
      component: () => import('../views/SiteDetail.vue'),
    },
    {
      path: '/sites',
      name: 'sites',
      component: () => import('../views/SitesList.vue'),
    },
    {
      path: '/sites/:slug',
      name: 'site-detail',
      component: () => import('../views/SiteDetail.vue'),
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
  ],
})

export default router
