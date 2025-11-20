import { createRouter, createWebHistory } from 'vue-router'
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
      meta: { requiresAuth: false }
    },
    {
      path: '/sites/:site_id',
      name: 'site-detail',
      component: () => import('../views/SiteDetail.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/user/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reviews',
      name: 'reviews',
      component: () => import('../views/user/ReviewsView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/favorites',
      name: 'favorites',
      component: () => import('../views/user/FavoritosView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/my-reviews',
      name: 'my-reviews',
      component: () => import('../views/user/ReviewsView.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const sessionStore = useSessionStore();
  const loginModalStore = useLoginModalStore();

  // Solo intentar restaurar sesión si no estamos autenticados
  if (!sessionStore.isAuthenticated) {
    await sessionStore.restoreSession();
  }

  // Verificar autenticación después de restaurar la sesión
  if (requiresAuth && !sessionStore.isAuthenticated) {
    sessionStore.redirect_uri = to.fullPath;
    loginModalStore.openLoginModal();
    next(false);
  } else {
    next();
  }
});


export default router
