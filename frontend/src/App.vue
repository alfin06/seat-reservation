<script setup>
import SidebarMenu from './components/SideBarMenu.vue';
import { useAuthStore } from './store/auth';
import { computed } from 'vue';

const authStore = useAuthStore();

const buttons = computed(() => {
  const base = [
    { label: "Home", route: "/home", icon: "bi-house" },  
    { label: "Book a Seat", route: "/booking", icon: "bi-journal-plus" },
    { label: "Check‑in", route: "/check-in", icon: "bi-clipboard-check" },
    { label: "Instant Booking", route: "/instant", icon: "bi-lightning" },
    { label: "Booking History", route: "/history", icon: "bi-clock-history" },
  ];
  return authStore.user?.role === 'ADMIN'
    ? [{ label: "Admin Dashboard", route: "/admin-dashboard", icon: "bi-speedometer2" }, ...base]
    : base;
});
</script>

<template>
  <div class="container-fluid g-0">
    <div class="row flex-nowrap">
      <SidebarMenu :buttons="buttons" class="col-auto" />

      <main class="col ps-0 pe-0">
        <button
          class="btn btn-primary d-md-none m-3"
          type="button"
          data-bs-toggle="offcanvas"
          data-bs-target="#mobileSidebar"
          aria-controls="mobileSidebar">
          <i class="bi bi-list"></i> Menu
        </button>

        <router-view />
      </main>
    </div>

    <notifications position="top center" />

    <footer class="text-center py-3 border-top mt-auto bg-white">
      <div class="translation-controls mb-2">
        <button @click="$i18n.locale = 'en'" class="lang-btn">English</button>
        <button @click="$i18n.locale = 'zh'" class="lang-btn">中文</button>
      </div>
      <div class="footer text-muted">
        &copy; {{ new Date().getFullYear() }} Seat Reservation App | Developed by International Students
      </div>
    </footer>
  </div>
</template>

<style scoped>
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
</style>
