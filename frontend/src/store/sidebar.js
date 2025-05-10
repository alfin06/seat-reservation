import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSidebarStore = defineStore('sidebar', () => {
  const isCollapsed = ref(false);

  // Load from localStorage on init
  const init = () => {
    const saved = localStorage.getItem('sidebarCollapsed');
    isCollapsed.value = saved === 'true';
  };

  const toggle = () => {
    isCollapsed.value = !isCollapsed.value;
    localStorage.setItem('sidebarCollapsed', isCollapsed.value.toString());
  };

  return { isCollapsed, toggle, init };
});
