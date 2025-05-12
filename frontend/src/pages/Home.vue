<script>
import { useAuthStore, getCSRFToken } from "../store/auth.js";
import { useRouter } from "vue-router";
import { computed, onMounted, ref } from 'vue';
import { notify } from "@kyvg/vue3-notification";

export default {
  name: "Home",
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();

    const isToday = (date) => {
      const d = new Date(date);
      const now = new Date();
      return (
        d.getDate() === now.getDate() &&
        d.getMonth() === now.getMonth() &&
        d.getFullYear() === now.getFullYear()
      );
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

      if (authStore.user?.role === 'ADMIN') {
        return [
          { label: "Admin", route: "/admin-dashboard", icon: "bi-speedometer2" },
          ...baseButtons
        ];
      }

      return baseButtons;
    });

    const stats = ref({
      total: 0,
      active: 0,
      completed: 0,
      cancelled: 0,
    });

    const cancelReservation = async (reservationId) => {
      const confirmCancel = window.confirm("Are you sure you want to cancel this reservation?");
      if (!confirmCancel) 
        return;
      
      const token = localStorage.getItem('token');
      try {
        const res = await fetch(`http://localhost:8000/dashboard/api/reservations/${reservationId}/cancel/`, {
          method: "POST", // or "PATCH" depending on your backend
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
            'X-CSRFToken': getCSRFToken()
          },
          body: JSON.stringify({ user_id: authStore.user?.id }),
        });

        if (!res.ok)
        {
          notify({
            type: "error",
            title: "ERROR",
            text: "Failed to cancel reservation. Please try again in 5 minutes",
            duration: 3000
          });
          throw new Error("Failed to cancel reservation");
        }
          
        // Refresh stats and active reservations
        notify({
          type: "success",
          title: "Reservation Cancelled",
          text: "The reservation was successfully cancelled.",
          duration: 3000
        });

        await fetchStatsAndReservations();
      } catch (error) {
        notify({
          type: "error",
          title: "ERROR",
          text: "Failed to cancel reservation. Please try again in 5 minutes",
          duration: 3000
        });
        console.error("Cancel failed:", error);
      }
    };
    
    const activeReservations = ref([]);

    const go = (path) => router.push(path);

    const fetchStatsAndReservations = async () => {
      const token = localStorage.getItem('token');

      try {
        // Fetch stats
        const res = await fetch("http://localhost:8000/dashboard/api/reservations/stats/", {
          method: "POST",
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
            'X-CSRFToken': getCSRFToken()
          },
          body: JSON.stringify({ user_id: authStore.user?.id }),
        });

        if (!res.ok) throw new Error("Failed to fetch stats");

        const statsData = await res.json();
        stats.value = {
          total: statsData.total_reservations,
          active: statsData.active_reservations,
          completed: statsData.completed_reservations,
          cancelled: statsData.cancelled_reservations
        };

        // Fetch active reservations
        const activeRes = await fetch("http://localhost:8000/dashboard/api/reservations/active/", {
          method: "POST",
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
            'X-CSRFToken': getCSRFToken()
          },
          body: JSON.stringify({ user_id: authStore.user?.id }),
        });

        if (!activeRes.ok) throw new Error("Failed to fetch active reservations");

        const activeData = await activeRes.json();
        if (Array.isArray(activeData)) activeReservations.value = activeData;

      } catch (error) {
        console.error("Error fetching dashboard data:", error);
      }
    };

    onMounted(async () => {
      await authStore.fetchUser();
      await fetchStatsAndReservations();
    });

    return {
      authStore,
      router,
      buttons,
      stats,
      activeReservations,
      go,
      getCardClass,
      getBadgeClass,
      getLabel,
      cancelReservation
    };
  }
};
</script>

<template>
  <div class="container-fluid">
    <div class="row flex-nowrap">
      <main class="col py-4">
        <!-- Welcome & Actions -->
        <section v-if="authStore.isAuthenticated" class="card shadow-sm mb-4 p-4">
          <div class="d-flex flex-column flex-md-row align-items-center gap-3">
            <div class="flex-grow-1 text-center text-md-start">
              <h2 class="h5 fw-semibold text-dark">
                {{ $t('welcome') }}, {{ authStore.user?.name || authStore.user?.username }}!
                <span class="badge bg-secondary-subtle text-dark ms-2 text-uppercase">
                  {{ authStore.user?.role || $t('student') }}
                </span>
              </h2>
              <p class="small text-muted mb-3">
                {{ $t('lastLogin') }}: {{ new Date(authStore.user?.last_login).toLocaleString() }}
              </p>

              <!-- Small action buttons: only visible on small screens -->
              <div class="d-flex flex-wrap gap-2 d-md-none">
                <button
                  v-for="btn in buttons"
                  :key="btn.route"
                  class="btn btn-outline-primary btn-sm d-flex align-items-center"
                  @click="go(btn.route)">
                  <i :class="`bi ${btn.icon} me-2`"></i> {{ btn.label }}
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- Dashboard & Active Reservation -->
        <section class="card shadow-sm mb-4 p-4">
          <h2 class="h5 fw-semibold mb-4">
            {{ $t('dashboard') }}
          </h2>

          <div class="row text-center mb-4">
            <div class="col-3">
              <div class="p-3 bg-light rounded">
                <div class="fs-4 fw-bold">{{ stats.total }}</div>
                <div class="small text-muted">Total</div>
              </div>
            </div>
            <div class="col-3">
              <div class="p-3 bg-light rounded">
                <div class="fs-4 fw-bold text-warning">{{ stats.active }}</div>
                <div class="small text-muted">Active</div>
              </div>
            </div>
            <div class="col-3">
              <div class="p-3 bg-light rounded">
                <div class="fs-4 fw-bold text-success">{{ stats.completed }}</div>
                <div class="small text-muted">Completed</div>
              </div>
            </div>
            <div class="col-3">
              <div class="p-3 bg-light rounded">
                <div class="fs-4 fw-bold text-danger">{{ stats.cancelled }}</div>
                <div class="small text-muted">Cancelled</div>
              </div>
            </div>
          </div>

          <!-- Active reservations -->
          <div v-if="activeReservations.length" class="bg-white p-3 rounded border">
            <h6 class="fw-semibold mb-3">Active Reservations</h6>
            <div class="row">
              <div v-for="reservation in activeReservations"
                :key="reservation.id"
                class="col-12 col-sm-6 col-md-4 col-lg-3 mb-3">
                <div class="card h-100 border-0 shadow-sm rounded-3"
                  :class="getCardClass(reservation.reserved_start_time)">
                  <div class="card-body p-3">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                      <h6 class="fw-bold text-primary mb-0">{{ reservation.classroom }}</h6>
                      <span class="badge rounded-pill" :class="getBadgeClass(reservation.reserved_start_time)">
                        {{ getLabel(reservation.reserved_start_time) }}
                      </span>
                    </div>
                    <p class="mb-1 small text-muted">
                      <i class="bi bi-chair me-1"></i><strong>Seat {{ reservation.seat_id }}</strong>
                    </p>
                    <p class="mb-0 small text-muted">
                      <i class="bi bi-clock me-1"></i>
                      {{
                        new Date(reservation.reserved_start_time).toLocaleString('en-US', {
                          month: 'short',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit',
                          hour12: true})
                      }} –
                      {{
                        new Date(reservation.reserved_end_time).toLocaleString('en-US', {
                          hour: '2-digit',
                          minute: '2-digit',
                          hour12: true})
                      }}
                    </p>
                    <button class="btn btn-sm btn-outline-danger mt-2 w-100"
                      @click="cancelReservation(reservation.id)">
                      <i class="bi bi-x-circle me-1"></i> Cancel
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<style scoped>
@import "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css";

.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 1rem 1.5rem rgba(0, 0, 0, 0.05);
}

button.btn-sm {
  min-width: 100px;
}

.bg-light {
  background-color: #f8f9fa !important;
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