<script setup>
import { useRouter, useRoute } from 'vue-router';
import { useSidebarStore } from '@/store/sidebar';
import { onMounted, ref, watch } from 'vue';

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

watch(() => route.path, (newVal) => {
  activeRoute.value = newVal;
  localStorage.setItem('lastActiveRoute', newVal);
});

onMounted(() => {
  sidebarStore.init();
  const savedRoute = localStorage.getItem('lastActiveRoute');
  if (savedRoute && savedRoute !== route.path) {
    router.replace(savedRoute);
  }
});

const go = (path) => {
  router.push(path);
};
</script>

<template>
  <!-- Sidebar for desktop -->
  <div class="d-none d-md-block bg-light border-end sidebar">
    <div class="p-3">
      <button class="btn btn-sm btn-outline-primary mb-3" @click="sidebarStore.toggle">
        <i class="bi" :class="sidebarStore.isCollapsed ? 'bi-chevron-right' : 'bi-chevron-left'"></i>
      </button>

      <ul class="nav flex-column">
        <li
          v-for="btn in buttons"
          :key="btn.route"
          :class="['nav-item', 'sidebar-item', 'mb-2', { active: activeRoute === btn.route }]"
          @click="go(btn.route)">
          <i :class="['bi', btn.icon, 'me-3', 'fs-4']"></i>
          <span v-if="!sidebarStore.isCollapsed">{{ btn.label }}</span>
        </li>
      </ul>
    </div>
  </div>

  <!-- Offcanvas sidebar for mobile -->
  <div
    class="offcanvas offcanvas-start d-md-none"
    tabindex="-1"
    id="mobileSidebar"
    aria-labelledby="mobileSidebarLabel">
    <div class="offcanvas-header">
      <h5 class="offcanvas-title" id="mobileSidebarLabel">Menu</h5>
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body">
      <ul class="nav flex-column">
        <li
          v-for="btn in buttons"
          :key="btn.route"
          class="nav-item sidebar-item mb-2"
          @click="go(btn.route)">
          <i :class="['bi', btn.icon, 'me-3', 'fs-5']"></i>
          {{ btn.label }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  width: 250px;
  min-height: 100vh;
}

.sidebar.collapsed {
  width: 70px;
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