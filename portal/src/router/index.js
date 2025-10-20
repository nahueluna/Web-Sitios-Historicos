import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProfileView from '../views/ProfileView.vue'
import LoginView from '../views/LoginView.vue'
import { useSessionStore } from '@/stores/sessionStore'

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
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false, guestOnly: true }
    }
  ],
})

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const guestOnly = to.matched.some(record => record.meta.guestOnly);
  const sessionStore = useSessionStore();

  if (requiresAuth && !sessionStore.isAuthenticated()) {
    alert("Debe iniciar sesión para acceder a esta página.");
    next("/login");
  } else if (guestOnly && sessionStore.isAuthenticated()) {
    alert("Ya ha iniciado sesión.");
    next("/profile");
  } else {
    next();
  }
});

export default router
