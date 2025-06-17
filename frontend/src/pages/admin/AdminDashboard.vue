<template>
  <div class="admin-dashboard container-fluid">
    <div class="row flex-nowrap">
      <main class="col py-4">
        <!-- Welcome -->
        <section class="card shadow-sm mb-4 p-4 welcome-section">
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

        <!-- Stats Overview -->
        <section class="card shadow-sm mb-4 p-4">
          <h2 class="h5 fw-semibold mb-4">{{ $t('adminTitle') }}</h2>
          <el-row :gutter="20">
            <el-col :span="6">
              <el-card class="stat-card">
                <h3>{{ dashboardStats.total_classrooms }}</h3>
                <p>Total Rooms</p>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <h3>{{ dashboardStats.available_classroom_count }}</h3>
                <p>Available Rooms</p>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <h3>{{ dashboardStats.available_seats_count }}</h3>
                <p>Available Seats</p>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <h3>{{ dashboardStats.empty_seats_count }}</h3>
                <p>Reserved Seats</p>
              </el-card>
            </el-col>
          </el-row>
        </section>

        <!-- Charts Section -->
        <section class="card shadow-sm mb-4 p-4">
          <h2 class="h5 fw-semibold mb-4">Analytics</h2>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card>
                <line-chart :chart-data="reservationChartData" />
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <bar-chart :chart-data="seatChartData" />
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
import LineChart from '@/components/charts/LineChart.vue'
import BarChart from '@/components/charts/BarChart.vue'

export default {
  name: "AdminDashboard",
  components: {
    RoomManagement,
    UserManagement,
    SystemSettings,
    SeatManagement,
    LineChart,
    BarChart,
  },
  setup() {
    const authStore = useAuthStore();
    const stats = ref({
      users: 0,
      classrooms: 0,
      reservations: 0,
      checkInsToday: 0,
    });

    onMounted(async () => {
      await authStore.fetchUser();
    });

    return {
      authStore
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
      },
       reservationChartData: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
          label: 'Reservations',
          data: [10, 12, 14, 8, 7, 5, 3],
          borderColor: '#42b983',
          fill: false
        }]
      },
      seatChartData: {
        labels: ['Room A', 'Room B', 'Room C'],
        datasets: [{
          label: 'Available Seats',
          data: [12, 9, 15],
          backgroundColor: ['#409EFF', '#67C23A', '#E6A23C']
        }]
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
          const data = response.data;
          this.dashboardStats = response.data;

          // Update Reservation Line Chart
          const labels = Object.keys(data.reservations_last_week || {});
          const values = Object.values(data.reservations_last_week || {});
          this.reservationChartData = {
            labels: labels,
            datasets: [{
              label: 'Reservations',
              data: values,
              borderColor: '#42b983',
              fill: false
            }]
          };

          // Update Seat Availability Bar Chart
          const roomLabels = Object.keys(data.available_seats_per_room || {});
          const seatValues = Object.values(data.available_seats_per_room || {});
          this.seatChartData = {
            labels: roomLabels,
            datasets: [{
              label: 'Available Seats',
              data: seatValues,
              backgroundColor: ['#409EFF', '#67C23A', '#E6A23C']
            }]
          };
        }
      } catch (error) {
        console.error('Error fetching dashboard stats: ', error);
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
.stat-card {
  text-align: center;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
}
.stat-card h3 {
  font-size: 28px;
  margin-bottom: 5px;
  color: #409EFF;
}
.stat-card p {
  color: #666;
}
.welcome-section {
  background: linear-gradient(to right, #f0f9ff, #e0f7fa);
  border-left: 5px solid #409EFF;
}

</style>