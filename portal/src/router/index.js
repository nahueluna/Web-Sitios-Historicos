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
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true },
    },
  ],
})


router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const guestOnly = to.matched.some(record => record.meta.guestOnly);
  const sessionStore = useSessionStore();
  const loginModalStore = useLoginModalStore();

  const data = localStorage.getItem('user');
  if (!sessionStore.isAuthenticated() && data) {
    sessionStore.user = JSON.parse(data);
  }

  if (requiresAuth && !sessionStore.isAuthenticated()) {
    //alert("Debe iniciar sesión para acceder a este recurso.");
    sessionStore.redirect_uri = to.fullPath;
    loginModalStore.openLoginModal();
    next(false);
  } else if (guestOnly && sessionStore.isAuthenticated()) {
    alert("Ya ha iniciado sesión.");
    next(from.fullPath);
  } else {
    next();
  }
});


export default router
