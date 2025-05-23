import { createRouter, createWebHistory } from 'vue-router'

// Views
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import ForgotPassword from './pages/auth/ForgotPassword.vue'
import VerifyEmail from './pages/auth/VerifyEmail.vue'
import ResetPassword from './pages/auth/ResetPassword.vue'
import CheckIn from './views/CheckIn.vue'
import Reservation from './views/Reservation.vue'
import BookingHistory from './views/BookingHistory.vue'
import AdminDashboard from './views/AdminDashboard.vue'
import InstantBooking from './views/InstantBooking.vue'
import GeneralSettings from './views/GeneralSettings.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login, name: 'login' },
  { path: '/register', component: Register, name: 'register' },
  { path: '/forgot-password', component: ForgotPassword, name: 'forgot-password' },
  { path: '/verify-email/:token', component: VerifyEmail, name: 'verify-email' },
  { path: '/reset-password/:token', component: ResetPassword, name: 'reset-password' },
  { path: '/check-in', component: CheckIn, name: 'check-in' },
  { path: '/reservation', component: Reservation, name: 'reservation' },
  { path: '/booking-history', component: BookingHistory, name: 'booking-history' },
  { path: '/admin-dashboard', component: AdminDashboard, name: 'admin-dashboard' },
  { path: '/instant-booking', component: InstantBooking, name: 'instant-booking' },
  { path: '/general-settings', component: GeneralSettings, name: 'general-settings' },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
