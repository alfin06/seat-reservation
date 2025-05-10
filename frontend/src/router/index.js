import { createRouter, createWebHistory } from 'vue-router'
import Register from '../views/Register.vue'
import Login from '../views/Login.vue'
import Reservation from '../views/Reservation.vue'
import CheckIn from '../views/CheckIn.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

const routes = [
  { path: '/register', component: Register },
  { path: '/login', component: Login },
  { path: '/reservation', component: Reservation },
  { path: '/checkin', component: CheckIn },
  { path: '/student/instant-booking', name: 'InstantBooking', component: () => import('../pages/student/InstantBooking.vue'), meta: { requiresAuth: true } },
  { path: '/instant', redirect: '/student/instant-booking' },
  { path: '/admin', component: AdminDashboard },
  { path: '/', redirect: '/register' }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
