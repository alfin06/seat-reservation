<script setup>
import SidebarMenu from './components/SideBarMenu.vue';
import { useAuthStore } from './store/auth';
import { computed } from 'vue';

const authStore = useAuthStore();


const buttons = computed(() => {
  if (!authStore.user) return [];

  const shared = [
    { label: "Book a Seat", route: "/booking", icon: "bi-journal-plus" },
    { label: "Check‑in", route: "/check-in", icon: "bi-clipboard-check" },
    { label: "Instant Booking", route: "/instant", icon: "bi-lightning" },
    { label: "Booking History", route: "/history", icon: "bi-clock-history" },
  ];

  if (authStore.user.role === 'ADMIN') {
    const adminOnly = [
      { label: "Admin Dashboard", route: "/admin-dashboard", icon: "bi-speedometer2" },
      { label: "Manage Classroom", route: "/manage-rooms", icon: "bi-door-open" },
      { label: "Manage Seat", route: "/manage-seats", icon: "bi-journal" },
      { label: "General Settings", route: "/settings", icon: "bi-gear" },
      { type: 'divider' }, // Horizontal line
    ];
    return [...adminOnly, ...shared];
  }

  // For students and other users
  return [
    { label: "Home", route: "/home", icon: "bi-house" },
    ...shared
  ];
});
</script>

<template>
  <div class="app-container d-flex flex-column min-vh-100">
    <!-- Body: Sidebar + Main -->
    <div class="flex-grow-1 d-flex overflow-hidden">
      <SidebarMenu :buttons="buttons" class="d-none d-md-block" v-if="!$route.meta.hideSidebar" />
      <main class="flex-grow-1 overflow-auto">
        <!-- Mobile menu toggle -->
        <button v-if="!$route.meta.hideSidebar"
                class="btn d-md-none m-3"
                type="button"
                data-bs-toggle="offcanvas"
                data-bs-target="#mobileSidebar"
                aria-controls="mobileSidebar">
          <i class="bi bi-list"></i>
        </button>
        <router-view />
      </main>
    </div>

    <!-- Notifications -->
    <notifications position="top center" class="notif" />

    <!-- Sticky footer -->
    <footer class="footer text-center border-top bg-white py-2 mt-auto">
      <div class="translation-controls mb-1">
        <button @click="$i18n.locale = 'en'" class="lang-btn">English</button>
        <button @click="$i18n.locale = 'zh'" class="lang-btn">中文</button>
      </div>
      <div class="text-muted small">
        &copy; {{ new Date().getFullYear() }} Seat Reservation App | Developed by International Students
      </div>
    </footer>
  </div>
</template>

<style scoped>
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.footer {
  z-index: 10;
  background-color: white;
  border-top: 1px solid #dee2e6;
}

.lang-btn {
  margin: 0 5px;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background: #f8f9fa;
  color: #495057;
  cursor: pointer;
  transition: all 0.3s ease;
}

.lang-btn:hover {
  background: #e9ecef;
}

.notif {
  font-size: 20pt;
}
</style>
