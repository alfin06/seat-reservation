<template>
  <div class="container-fluid">
    <div class="row flex-nowrap">
      <main class="col py-4">

        <!-- Welcome Section -->
        <section class="card shadow-sm mb-4 p-4">
          <h2 class="h5 fw-semibold text-dark">
            {{ $t('welcome') }}, {{ authStore.user?.name || authStore.user?.username }}!
            <span class="badge bg-primary-subtle text-dark ms-2 text-uppercase">
              {{ authStore.user?.role || 'ADMIN' }}
            </span>
          </h2>
          <p class="small text-muted">
            {{ $t('lastLogin') }}: {{ new Date(authStore.user?.last_login).toLocaleString() }}
          </p>
        </section>

        <!-- Dashboard Content Section -->
        <section class="card shadow-sm mb-4 p-4">
          <h2 class="h5 fw-semibold mb-4">{{ $t('adminStats') }}</h2>

          <!-- <div class="row text-center mb-4">
            <div class="col-6 col-md-3" v-for="(stat, label) in stats" :key="label">
              <div class="p-3 bg-light rounded">
                <div class="fs-4 fw-bold">{{ stat }}</div>
                <div class="small text-muted text-capitalize"><strong>{{ label }}</strong></div>
              </div>
            </div>
          </div> -->

          <!-- Add more admin controls/sections below as needed -->
          <!-- Urgent Alert -->
          <!-- <el-alert 
            type="warning" 
            title="Immediate Action Needed" 
            show-icon
            class="mb-4"
          >
            <span>3 seats need cleaning in Room B</span>
            <el-button type="warning" size="mini" class="ml-2">
              Mark as Cleaned
            </el-button>
          </el-alert> -->

          <!-- Stats Cards -->
          <el-row :gutter="20" class="mb-6">
            <el-col :span="8">
              <el-card class="stat-card" shadow="hover">
                <h3>{{ dashboardStats.total_classrooms }}</h3>
                <p>Total Rooms</p>
                <el-tag type="success">{{ dashboardStats.available_classroom_count }} Available</el-tag>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="stat-card" shadow="hover">
                <h3>{{ dashboardStats.available_seats_count }}</h3>
                <p>Available Seats</p>
                <el-tag type="warning">{{ dashboardStats.empty_seats_count }} Reserved</el-tag>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="stat-card" shadow="hover">
                <h3>{{ dashboardStats.available_classroom_count }}</h3>
                <p>Available Rooms</p>
                <el-tag type="warning">{{ dashboardStats.empty_classroom_count }} Reserved</el-tag>
              </el-card>
            </el-col>
          </el-row>
        </section>
      </main>
    </div>
  </div>
</template>

<script>
import RoomManagement from '../../components/admin/RoomManagement.vue'
import UserManagement from '../../components/admin/UserManagement.vue'
import SystemSettings from '../../components/admin/SystemSettings.vue'
import SeatManagement from '@/components/admin/SeatManagement.vue'
import axios from 'axios'
import { useAuthStore } from '../../store/auth.js'
import { onMounted, ref } from 'vue'

export default {
  name: "AdminDashboard",
  components: {
    RoomManagement,
    UserManagement,
    SystemSettings,
    SeatManagement
  },
  setup() {
    const authStore = useAuthStore();
    const stats = ref({
      users: 0,
      classrooms: 0,
      reservations: 0,
      checkInsToday: 0,
    });

    const fetchAdminStats = async () => {
      const token = localStorage.getItem('token');
      try {
        const res = await fetch('http://localhost:8000/dashboard/api/admin/stats/', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
          },
        });
        if (!res.ok) throw new Error("Failed to fetch admin stats");

        const data = await res.json();
        stats.value = {
          users: data.total_users,
          classrooms: data.total_classrooms,
          reservations: data.total_reservations,
          checkInsToday: data.check_ins_today,
        };
      } catch (err) {
        console.error("Error fetching admin stats:", err);
      }
    };

    onMounted(async () => {
      await authStore.fetchUser();
      await fetchAdminStats();
    });

    return {
      authStore,
      stats,
    };
  },
  data() {
    return {
      activeTab: 'rooms',
      currentLanguage: 'en',
      dashboardStats: {
        total_classrooms: 0,
        available_classroom_count: 0,
        available_seats_count: 0,
        empty_seats_count: 0,
        empty_classroom_count: 0,
        total_seats: 0,
        number_of_user: 0
      }
    };
  },
  methods: {
    changeLanguage(lang) {
      this.currentLanguage = lang;
      this.$message.success(`Language changed to ${lang === 'en' ? 'English' : 'Chinese'}`);
    },

    goToHome() {
      this.$router.push({ name: 'home' });
    },

    handleRoomStatusUpdate() {
      const seatManagementComponent = this.$refs.seatManagement;
      if (seatManagementComponent) {
        seatManagementComponent.fetchSeats();
        this.$message.info('Seat list refreshed due to room status change.');
      }
      this.fetchDashboardStats();
    },

    handleSeatStatusUpdate() {
      this.fetchDashboardStats();
    },

    async fetchDashboardStats() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/dashboard/admin/status/', {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
          },
          withCredentials: true
        });
        if (response.data) {
          this.dashboardStats = response.data;
        }
      } catch (error) {
        console.error('Error fetching dashboard stats:', error);
        this.$message.error('Failed to load dashboard statistics');
      }
    }
  },
  mounted() {
    this.fetchDashboardStats();
  }
};
</script>

<style scoped>
.page-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.stat-card {
  text-align: center;
  padding: 20px;
  border-top: 4px solid #409EFF;
}
.stat-card h3 {
  font-size: 30px;
  margin: 0;
  color: #409EFF;
}
.stat-card p {
  font-weight: 600;
  margin: 5px 0 10px;
}

.mb-4 {
  margin-bottom: 20px;
}
.mb-6 {
  margin-bottom: 30px;
}
.ml-2 {
  margin-left: 10px;
}
.d-flex {
  display: flex;
}
.justify-between {
  justify-content: space-between;
}
.items-center {
  align-items: center;
}


</style>