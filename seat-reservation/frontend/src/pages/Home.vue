<script>
import { useAuthStore } from "../store/auth.js";
import { useRouter } from "vue-router";
import { computed } from 'vue';

export default {
  name: "Home",
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const buttons = computed(() => {
      const baseButtons = [
        { label: "Book a Seat", route: "/booking", icon: "bi-journal-plus" },
        { label: "Check‑in", route: "/check-in", icon: "bi-clipboard-check" },
        { label: "Instant Booking", route: "/instant", icon: "bi-lightning" },
        { label: "Booking History", route: "/history", icon: "bi-clock-history" },
      ];

      if (authStore.user?.role === 'ADMIN') {
        return [
          { label: "Admin Dashboard", route: "/admin-dashboard", icon: "bi-speedometer2" },
          ...baseButtons
        ];
      }

      return baseButtons;
    });

    const go = (path) => router.push(path);

    return { authStore, router, buttons, go };
  },

  methods: {
    async logout() {
      try {
        await this.authStore.logout(this.$router);
      } catch (err) {
        console.error(err);
      }
    },
  },

  async mounted() {
    await this.authStore.fetchUser();
  },
};
</script>

<template>
  <div class="container-fluid px-3 px-md-5 py-4">
    <!-- User Info Card -->
    <section
      v-if="authStore.isAuthenticated"
      class="card shadow-sm mb-4 rounded-4 border-0 animate__animated animate__fadeIn bg-light">
      <div class="card-body d-flex flex-column flex-md-row align-items-center gap-3">
        <div class="flex-grow-1 text-center text-md-start">
          <h2 class="h5 mb-1 fw-semibold text-dark">
            {{ $t('welcome') }}, {{ authStore.user?.name || authStore.user?.username }}!
            <span class="badge bg-secondary-subtle text-dark fw-normal ms-2 text-uppercase">
              {{ authStore.user?.role || $t('student') }}
            </span>
          </h2>
          <p class="small text-muted mb-0">
            {{ $t('lastLogin') }}:
            {{ new Date(authStore.user?.last_login).toLocaleString() }}
          </p>
        </div>

        <button class="btn btn-danger px-4" @click="logout">
          <i class="bi bi-box-arrow-right me-2"></i>
          {{ $t('logout') }}
        </button>
      </div>
    </section>

    <!-- Quick Actions -->
    <section class="card shadow-sm rounded-4 border-0 animate__animated animate__fadeIn">
      <div class="card-body">
        <h2 class="h5 mb-4 text-primary fw-semibold text-center text-md-start">
          {{ $t('quickAction') }}
        </h2>

        <div class="row g-3">
          <div
            class="col-6 col-sm-4 col-md-3"
            v-for="btn in buttons"
            :key="btn.route">
            <div
              class="action-tile text-center bg-white border rounded-4 p-4 h-100 d-flex flex-column align-items-center justify-content-center shadow-sm"
              @click="go(btn.route)"
              role="button">
              <i :class="`bi ${btn.icon} text-primary fs-2 mb-2`"></i>
              <div class="fw-semibold text-dark">{{ btn.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
@import "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css";

.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 0.75rem 1.5rem rgba(0, 0, 0, 0.05);
}

button.btn:hover {
  background-color: #e9f2ff;
}

.action-tile {
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-tile:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
  box-shadow: 0 0.75rem 1.25rem rgba(0, 0, 0, 0.05);
}
</style>
