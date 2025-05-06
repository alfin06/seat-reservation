import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import Reservation from '../views/Reservation.vue'
import CheckIn from '../views/CheckIn.vue'
import InstantBooking from '../views/InstantBooking.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import ForgotPassword from '../views/ForgotPassword.vue'
import BookingHistory from '../views/BookingHistory.vue' // NEW IMPORT

const routes = [
  // ALL EXISTING ROUTES REMAIN UNCHANGED
  { path: '/register', component: Register },
  { path: '/login', component: Login },
  { path: '/reservation', component: Reservation },
  { path: '/checkin', component: CheckIn },
  { path: '/instant-booking', component: InstantBooking },
  { path: '/admin', component: AdminDashboard },
  { path: '/forgot-password', component: ForgotPassword },
  
  // ONLY NEW ADDITION (placed at the end)
  {
    path: '/booking-history',
    name: 'BookingHistory',
    component: BookingHistory,
    meta: { requiresAuth: true } // Optional: if you want to protect this route
  },
  
  // EXISTING ROOT REDIRECT
  { path: '/', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router