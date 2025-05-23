<script setup>
import { useAuthStore, getCSRFToken } from "@/store/auth.js";
import { useRouter } from "vue-router";
import { computed, onMounted, ref } from "vue";
import { notify } from "@kyvg/vue3-notification";

const authStore = useAuthStore();
const router = useRouter();

const stats = ref({ total: 0, active: 0, completed: 0, cancelled: 0 });
const activeReservations = ref([]);

const isToday = (date) => {
  const d = new Date(date);
  const now = new Date();
  return d.getDate() === now.getDate() &&
         d.getMonth() === now.getMonth() &&
         d.getFullYear() === now.getFullYear();
};

const getLabel = (date) => (isToday(date) ? "Today" : "Upcoming");
const getBadgeClass = (date) =>
  isToday(date) ? "bg-success-subtle text-success" : "bg-warning-subtle text-warning";
const getCardClass = (date) =>
  isToday(date) ? "bg-success bg-opacity-10" : "bg-warning bg-opacity-10";

const buttons = computed(() => {
  const baseButtons = [
    { label: "Book", route: "/booking", icon: "bi-journal-plus" },
    { label: "Check‑in", route: "/check-in", icon: "bi-clipboard-check" },
    { label: "Instant", route: "/instant", icon: "bi-lightning" },
  ];
  if (authStore.user?.role === "ADMIN") {
    return [{ label: "Admin", route: "/admin-dashboard", icon: "bi-speedometer2" }, ...baseButtons];
  }
  return baseButtons;
});

const go = (path) => router.push(path);

const cancelReservation = async (reservationId) => {
  if (!window.confirm("Are you sure you want to cancel this reservation?")) return;

  try {
    const res = await fetch(`http://localhost:8000/dashboard/api/reservations/${reservationId}/cancel/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${localStorage.getItem("token")}`,
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({ user_id: authStore.user?.id }),
    });

    if (!res.ok) throw new Error("Cancel failed");

    notify({ type: "success", title: "Cancelled", text: "Reservation cancelled", duration: 2500 });
    await fetchStatsAndReservations();
  } catch (error) {
    notify({ type: "error", title: "Error", text: "Could not cancel reservation", duration: 3000 });
    console.error("Cancel failed:", error);
  }
};

const fetchStatsAndReservations = async () => {
  try {
    const token = localStorage.getItem("token");

    const statsRes = await fetch("http://localhost:8000/dashboard/api/reservations/stats/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({ user_id: authStore.user?.id }),
    });

    if (statsRes.ok) {
      const data = await statsRes.json();
      stats.value = {
        total: data.total_reservations,
        active: data.active_reservations,
        completed: data.completed_reservations,
        cancelled: data.cancelled_reservations,
      };
    }

    const activeRes = await fetch("http://localhost:8000/dashboard/api/reservations/active/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Token ${token}`,
        "X-CSRFToken": getCSRFToken(),
      },
      body: JSON.stringify({ user_id: authStore.user?.id }),
    });

    if (activeRes.ok) {
      activeReservations.value = await activeRes.json();
    }
  } catch (err) {
    console.error("Error loading data:", err);
  }
};

onMounted(async () => {
  await authStore.fetchUser();
  await fetchStatsAndReservations();
});
</script>

<template>
  <div class="container-fluid py-4">
    <section v-if="authStore.isAuthenticated" class="card shadow-sm p-4 mb-4">
      <h5>Welcome, {{ authStore.user?.name || authStore.user?.username }}!</h5>
      <p class="text-muted small">Last login: {{ new Date(authStore.user?.last_login).toLocaleString() }}</p>

      <div class="d-flex flex-wrap gap-2 mt-3">
        <button v-for="btn in buttons" :key="btn.route" class="btn btn-outline-primary" @click="go(btn.route)">
          <i :class="`bi ${btn.icon} me-2`"></i>{{ btn.label }}
        </button>
      </div>
    </section>

    <section class="card shadow-sm p-4">
      <h5>Reservation Stats</h5>
      <div class="row text-center mb-4 mt-3">
        <div class="col-6 col-md-3" v-for="(value, key) in stats" :key="key">
          <div class="p-3 bg-light rounded">
            <div class="fw-bold fs-5">{{ value }}</div>
            <div class="small text-muted text-capitalize">{{ key }}</div>
          </div>
        </div>
      </div>

      <div v-if="activeReservations.length" class="mt-4">
        <h6>Upcoming Reservations</h6>
        <div class="row">
          <div v-for="res in activeReservations" :key="res.id" class="col-12 col-md-6 col-lg-4">
            <div class="card shadow-sm mb-3 p-3" :class="getCardClass(res.reserved_start_time)">
              <div class="mb-2">
                <h6 class="text-primary mb-1">{{ res.classroom }}</h6>
                <span class="badge" :class="getBadgeClass(res.reserved_start_time)">
                  {{ getLabel(res.reserved_start_time) }}
                </span>
              </div>
              <div class="small mb-1">Seat {{ res.seat_id }}</div>
              <div class="small mb-2">
                {{ new Date(res.reserved_start_time).toLocaleString() }} — 
                {{ new Date(res.reserved_end_time).toLocaleTimeString() }}
              </div>
              <button class="btn btn-sm btn-outline-success w-100 mb-1" @click="$router.push('/check-in')">
                <i class="bi bi-clipboard-check me-2"></i>Check In
              </button>
              <button class="btn btn-sm btn-outline-danger w-100" @click="cancelReservation(res.id)">
                <i class="bi bi-x-circle me-2"></i>Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 0.75rem 1.25rem rgba(0, 0, 0, 0.05);
}
</style>
