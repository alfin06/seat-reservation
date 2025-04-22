<template>
  <div class="app">
    <header class="app-header">
      <h1>Study Seat Reservation System</h1>
      <nav class="main-nav">
        <router-link to="/register" class="nav-link">Register</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/login" class="nav-link">Login</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/reservation" class="nav-link">Study Room & Seat Reservation</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/checkin" class="nav-link">Check-In & No-show Management</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/instant-booking" class="nav-link">Seat Availability & Instant Booking</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/booking-history" class="nav-link">Booking History</router-link>
        <span class="nav-divider">|</span>
        <router-link to="/admin" class="nav-link">Admin Dashboard</router-link>
      </nav>
    </header>

    <main class="app-content">
      <router-view />
    </main>
  </div>
</template>

<style>
/* ===== EXISTING STYLES (UNCHANGED) ===== */
.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.app-header {
  text-align: center;
  margin-bottom: 30px;
}

.app-header h1 {
  font-size: 2rem;
  margin-bottom: 15px;
  color: #2c3e50;
}

.app-content {
  padding: 20px 0;
}

/* ===== ENHANCED NAVIGATION (ONLY THIS SECTION IS NEW) ===== */
.main-nav {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 0;
  padding: 12px 24px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  margin-bottom: 24px;
}

.nav-link {
  font-weight: 500;
  color: #2c3e50;
  text-decoration: none;
  padding: 8px 16px;
  position: relative;
  transition: all 0.2s ease;
  border-radius: 4px;
}

.nav-link:hover {
  color: #646cff;
  background: rgba(100, 108, 255, 0.08);
}

.nav-link.router-link-exact-active {
  color: #646cff;
  font-weight: 600;
}

.nav-link.router-link-exact-active::after {
  content: '';
  position: absolute;
  bottom: -13px;
  left: 16px;
  right: 16px;
  height: 3px;
  background: #646cff;
  border-radius: 3px;
}

.nav-divider {
  color: rgba(0,0,0,0.1);
  font-weight: bold;
}

/* Mobile responsiveness */
@media (max-width: 768px) {
  .main-nav {
    overflow-x: auto;
    justify-content: flex-start;
    padding-bottom: 12px;
    -webkit-overflow-scrolling: touch;
  }
  
  .nav-link {
    white-space: nowrap;
  }
}
</style>