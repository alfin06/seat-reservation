import { createRouter, createWebHistory } from 'vue-router'

// Views
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import ForgotPassword from './pages/auth/ForgotPassword.vue'
import VerifyEmail from './pages/auth/VerifyEmail.vue'
import ResetPassword from './pages/auth/ResetPassword.vue'
import CheckIn from './pages/student/CheckIn.vue'
import Reservation from './pages/student/Reservation.vue'
import AdminDashboard from './pages/admin/AdminDashboard.vue'
import InstantBooking from './pages/student/InstantBooking.vue'
import ManageRooms from './pages/admin/ManageRooms.vue'
import ManageSeats from './pages/admin/ManageSeats.vue'
import Settings from './pages/admin/SystemSettings.vue'
import History from './pages/student/BookingHistory.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'login', component: Login, meta: { hideSidebar: true }},
  { path: '/register', name: 'register', component: Register, meta: { hideSidebar: true }},
  { path: '/forgot-password', name: 'forgot-password', component: ForgotPassword, meta: { hideSidebar: true }},
  { path: '/verify-email/:token', name: 'verify-email', component: VerifyEmail, meta: { hideSidebar: true }},
  { path: '/reset-password/:token', name: 'reset-password', component: ResetPassword, meta: { hideSidebar: true }},
  
  { path: '/admin-dashboard', name: 'admin-dashboard', component: AdminDashboard, meta: { requiresAuth: true, requiresAdmin: true }},
  { path: '/manage-rooms', name: 'manage-rooms', component: ManageRooms, meta: { requiresAuth: true, requiresAdmin: true }},
  { path: '/manage-seats', name: 'manage-seats', component: ManageSeats, meta: { requiresAuth: true, requiresAdmin: true }},
  { path: '/settings', name: 'settings', component: Settings, meta: { requiresAuth: true, requiresAdmin: true }},

  { path: '/home', name: 'home', component: Home, meta: { requiresAuth: true } },
  { path: '/check-in', name: 'check-in', component: CheckIn, meta: { requiresAuth: true } },
  { path: '/booking', name: 'booking', component: Reservation, meta: { requiresAuth: true } },
  { path: '/student/instant-booking', name: 'instant-booking', component: InstantBooking, meta: { requiresAuth: true } },
  { path: '/instant', redirect: '/student/instant-booking' },
  { path: '/booking-success', name: 'booking-success', component: BookingSuccess, meta: { requiresAuth: true } },
  { path: '/history', name: 'history', component: History, meta: { requiresAuth: true } },
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
  
  const publicRoutes = ['reset-password', 'verify-email'];
  if (publicRoutes.includes(to.name)) {
    next();
    return;
  }

  // Redirect authenticated users away from login/register/forgot-password
  if ((to.name === 'login' || to.name === 'register' || to.name === 'forgot-password') && isAuthenticated) {
    next({ name: 'home' });
  } else if (to.meta.requiresAdmin && (!isAuthenticated || userRole !== 'ADMIN')) {
    next({ name: 'home' });
  } else if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login' });
  } else {
    next();
  }
})

export default router