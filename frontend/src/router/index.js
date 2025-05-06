import { createRouter, createWebHistory } from 'vue-router'

import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import Reservation from '../views/Reservation.vue'
import CheckIn from '../views/CheckIn.vue'
import InstantBooking from '../views/InstantBooking.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import ForgotPassword from '../views/ForgotPassword.vue'
import BookingHistory from '../views/BookingHistory.vue'
import GeneralSettings from '../views/GeneralSettings.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/register', component: Register, meta: { guestOnly: true } },
  { path: '/login', component: Login, meta: { guestOnly: true } },
  { path: '/reservation', component: Reservation, meta: { requiresAuth: true } },
  { path: '/check-in', component: CheckIn, meta: { requiresAuth: true } },
  { path: '/instant-booking', component: InstantBooking, meta: { requiresAuth: true } },
  { path: '/admin-dashboard', component: AdminDashboard, meta: { requiresAuth: true } },
  { path: '/forgot-password', component: ForgotPassword, meta: { guestOnly: true } },
  { path: '/booking-history', component: BookingHistory, meta: { requiresAuth: true } },
  { path: '/general-settings', component: GeneralSettings, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
