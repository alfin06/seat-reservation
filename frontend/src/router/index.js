import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import Reservation from '../views/Reservation.vue'
import CheckIn from '../views/CheckIn.vue'
import InstantBooking from '../views/InstantBooking.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import ForgotPassword from '../views/ForgotPassword.vue' // NEW IMPORT

const routes = [
  { path: '/register', component: Register },
  { path: '/login', component: Login },
  { path: '/reservation', component: Reservation },
  { path: '/checkin', component: CheckIn },
  { path: '/instant-booking', component: InstantBooking },
  { path: '/admin', component: AdminDashboard },
  { path: '/forgot-password', component: ForgotPassword }, // NEW ROUTE
  { path: '/', redirect: '/register' }
]

export default createRouter({
  history: createWebHistory(),
  routes
})