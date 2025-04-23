<!-- Home.vue -->
<script>
import { useAuthStore } from "../store/auth.js";
import { useRouter } from "vue-router";

export default {
  name: "Home",
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    // quick‑action buttons
    const buttons = [
        { label: "Book a Seat",       route: "/booking",  icon: "bi-journal-plus" },
        { label: "Check‑in",          route: "/check-in", icon: "bi-clipboard-check" },
        { label: "Instant Booking", route: "/instant", icon: "bi-lightning" },
        { label: "Booking History",   route: "/history",  icon: "bi-clock-history" },
    ];

    // navigation helper
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
  <div class="container-lg py-5">
    <!-- Profile card -->
    <section
      v-if="authStore.isAuthenticated"
      class="card shadow-sm mb-4 animate__animated animate__fadeIn"
    >
      <div
        class="card-body d-flex flex-column flex-md-row align-items-center gap-3"
      >
        <div class="flex-grow-1">
          <h2 class="h5 mb-1">
            Welcome, {{ authStore.user?.name || authStore.user?.username }} !
            <span class="badge bg-light text-secondary fw-normal ms-2 text-uppercase">
              {{ authStore.user?.role || "Student" }}
            </span>
          </h2>
          <div class="small text-muted">
            Last login:
            {{ new Date(authStore.user?.last_login).toLocaleString() }}
          </div>
        </div>

        <button class="btn btn-outline-danger px-4" @click="logout">
          Logout
        </button>
      </div>
    </section>

    <!-- Action buttons -->
    <section class="card shadow-sm animate__animated animate__fadeIn">
      <div class="card-body">
        <h2 class="h5 mb-4 text-primary">Quick actions</h2>

        <div class="row g-3">
          <div class="col-6 col-md-3" v-for="btn in buttons" :key="btn.label">
            <button
              class="w-100 btn btn-outline-primary py-3 d-flex flex-column align-items-center justify-content-center"
              @click="go(btn.route)"
            >
              <i :class="`bi ${btn.icon} fs-3 mb-2`"></i>
              {{ btn.label }}
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
@import "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css";
.card:hover {
  transform: translateY(-2px);
  transition: transform 0.2s;
}
</style>
