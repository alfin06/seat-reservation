<script setup>
import { useRouter, useRoute } from 'vue-router';
import { useSidebarStore } from '@/store/sidebar';
import { onMounted, ref, watch } from 'vue';
import logo from '@/assets/app_logo.png';
import { useAuthStore } from "../store/auth.js";
import * as bootstrap from 'bootstrap';

const props = defineProps({
  buttons: {
    type: Array,
    required: true,
  },
});

const router = useRouter();
const route = useRoute();
const sidebarStore = useSidebarStore();
const activeRoute = ref(route.path);
const authStore = useAuthStore();

watch(() => route.path, (newVal) => {
  activeRoute.value = newVal;
  localStorage.setItem('lastActiveRoute', newVal);
});

onMounted(() => {
  sidebarStore.init();

  // Restore last route
  const savedRoute = localStorage.getItem('lastActiveRoute');
  if (savedRoute && savedRoute !== route.path) {
    router.replace(savedRoute);
  }

  // Enable Bootstrap tooltips
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipTriggerList.forEach(el => {
    new bootstrap.Tooltip(el);
  });
});

const go = (path) => {
  router.push(path);
};

const logout = async () => {
  try {
    // Ensure Bootstrap's offcanvas instance is closed properly
    const offcanvasEl = document.getElementById('mobileSidebar');
    const instance = bootstrap.Offcanvas.getInstance(offcanvasEl)
      || new bootstrap.Offcanvas(offcanvasEl);
    instance.hide(); // This triggers full cleanup (backdrop, classes, etc.)

    // Wait a short time to let Bootstrap clean up the UI
    setTimeout(async () => {
      await authStore.logout(router);
    }, 300); // Adjust if needed (usually matches the transition duration)
  } catch (err) {
    console.error('Logout failed:', err);
  }
};
</script>

<template>
  <!-- Sidebar for desktop -->
  <div :class="['d-none d-md-block', 'bg-light', 'border-end', 'sidebar', { collapsed: sidebarStore.isCollapsed }]">
    <div class="p-3">
      <button class="btn btn-sm btn-outline-primary mb-3" @click="sidebarStore.toggle">
        <i class="bi" :class="sidebarStore.isCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"></i>
      </button>

      <div class="text-center mb-3">
        <img :src="logo" alt="App Logo" class="img-fluid" style="max-height: 150px;" />
      </div>

      <ul class="nav flex-column">
        <li v-for="(btn, index) in buttons" :key="index">
          <hr v-if="btn.type === 'divider'" class="my-2" />
          <div
            v-else
            :class="['nav-item', 'sidebar-item', 'mb-2', { active: activeRoute === btn.route }]"
            @click="go(btn.route)">
            <i :class="['bi', btn.icon, 'me-3', 'fs-4']"></i>
            <span v-if="!sidebarStore.isCollapsed">{{ btn.label }}</span>
          </div>
        </li>

        <!-- Fix: logout button should be in its own <li> -->
        <li class="nav-item sidebar-item mb-2 mt-auto"
            title="Logout"
            data-bs-toggle="tooltip"
            data-bs-placement="right"
            @click="logout">
          <i class="bi bi-box-arrow-right me-3 fs-4"></i>
          <span v-if="!sidebarStore.isCollapsed">Logout</span>
        </li>
      </ul>
    </div>
  </div>

  <!-- Offcanvas sidebar for mobile -->
  <div class="offcanvas offcanvas-start d-md-none"
    tabindex="-1"
    id="mobileSidebar"
    aria-labelledby="mobileSidebarLabel">
    <div class="offcanvas-header">
      <div class="text-center mb-3">
        <img :src="logo" alt="App Logo" class="img-fluid" style="max-height: 100px;" />
      </div>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <ul class="nav flex-column">
        <li v-for="(btn, index) in buttons" :key="index">
          <hr v-if="btn.type === 'divider'" class="my-2" />
          <div
            v-else
            class="nav-item sidebar-item mb-2"
            @click="go(btn.route)">
            <i :class="['bi', btn.icon, 'me-3', 'fs-5']"></i>
            {{ btn.label }}
          </div>
        </li>
        <li class="nav-item sidebar-item mb-2" @click="logout">
          <i class="bi bi-box-arrow-right me-3 fs-4"></i>
          <span>Logout</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  width: 250px;
  height: 100vh;
  overflow-y: auto; /* allow vertical scrolling */
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
}

.sidebar.collapsed {
  width: 70px;
}

.sidebar.collapsed ul.nav {
  padding-left: 0;
}

.sidebar.collapsed .sidebar-item {
  justify-content: center;
  text-align: center;
}

.sidebar.collapsed .sidebar-item i {
  margin-right: 0; /* Remove spacing from icon */
}

.sidebar.collapsed .sidebar-item span {
  display: none; /* Hide label when collapsed */
}

.sidebar-item {
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.375rem;
  transition: background-color 0.2s ease;
}

.sidebar-item:hover {
  background-color: #f8f9fa;
}

.sidebar-item.active {
  background-color: #e9f2ff;
  font-weight: bold;
  color: #0d6efd;
}
</style>