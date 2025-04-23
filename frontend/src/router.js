import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import Login from './pages/auth/Login.vue'
import Register from './pages/auth/Register.vue'
import ForgotPassword from './pages/auth/ForgotPassword.vue'
import VerifyEmail from './pages/auth/VerifyEmail.vue'
import ResetPassword from './pages/auth/ResetPassword.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'login', component: Login, },
  { path: '/register', name: 'register', component: Register, },
  { path: '/forgot-password', name: 'forgot-password', component: ForgotPassword, },
  { path: '/verify-email/:token', name: 'verify-email', component: VerifyEmail, },
  { path: '/reset-password/:token', name: 'reset-password', component: ResetPassword, },

  { path: '/home', name: 'home', component: Home, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation Guard for Auth
router.beforeEach((to, from, next) => {
  const storedState = JSON.parse(localStorage.getItem('authState'))
  const isAuthenticated = storedState?.isAuthenticated

  // Redirect authenticated users away from login/register/forgot-password
  if ((to.name === 'login' || to.name === 'register' || to.name === 'forgot-password') && isAuthenticated) {
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