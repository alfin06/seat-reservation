import { createRouter, createWebHistory } from 'vue-router'
import Home from './pages/Home.vue'
import Login from './pages/auth/Login.vue'
import Register from './pages/auth/Register.vue'
import ForgotPassword from './pages/auth/ForgotPassword.vue'
import VerifyEmail from './pages/auth/VerifyEmail.vue'
import ResetPassword from './pages/auth/ResetPassword.vue'
import CheckIn from './pages/student/CheckIn.vue'
import Reservation from './pages/student/Reservation.vue'
import AdminDashboard from './pages/admin/AdminDashboard.vue'
import InstantBooking from './pages/student/InstantBooking.vue'

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/login', name: 'login', component: Login, },
  { path: '/register', name: 'register', component: Register, },
  { path: '/forgot-password', name: 'forgot-password', component: ForgotPassword, },
  { path: '/verify-email/:token', name: 'verify-email', component: VerifyEmail, },
  { path: '/reset-password/:token', name: 'reset-password', component: ResetPassword, },
  { path: '/home', name: 'home', component: Home, meta: { requiresAuth: true } },
  { path: '/admin-dashboard', name: 'admin-dashboard', component: AdminDashboard, meta: { requiresAuth: true, requiresAdmin: true }},
  { path: '/check-in', name: 'check-in', component: CheckIn, meta: { requiresAuth: true } },
  { path: '/booking', name: 'booking', component: Reservation, meta: { requiresAuth: true } },
  { path: '/student/instant-booking', name: 'instant-booking', component: InstantBooking, meta: { requiresAuth: true } },
  { path: '/instant', redirect: '/student/instant-booking' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation Guard for Auth
router.beforeEach((to, from, next) => {
  const storedState = JSON.parse(localStorage.getItem('authState'))
  const isAuthenticated = storedState?.isAuthenticated
  const userRole = storedState?.user?.role

  // Redirect authenticated users away from login/register/forgot-password
  if ((to.name === 'login' || to.name === 'register' || to.name === 'forgot-password') && isAuthenticated) {
    next({ name: 'home' })
  }

  // Check for admin role requirement
  else if (to.meta.requiresAdmin && (!isAuthenticated || userRole !== 'ADMIN')) {
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