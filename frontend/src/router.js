import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import Login from './pages/Login.vue'
import Register from './pages/Register.vue'

const routes = [
  { 
    path: '/', 
    redirect: '/login' 
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
  },
  {
    path: '/home',
    name: 'home',
    component: Home,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation Guard for Auth
router.beforeEach((to, from, next) => {
  const storedState = JSON.parse(localStorage.getItem('authState'))
  const isAuthenticated = storedState?.isAuthenticated

  // Redirect authenticated users away from login/register
  if ((to.name === 'login' || to.name === 'register') && isAuthenticated) {
    next({ name: 'home' })
  }

  // Redirect unauthenticated users trying to access protected pages
  else if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login' })
  }

  // Allow navigation
  else {
    next()
  }
})

export default router