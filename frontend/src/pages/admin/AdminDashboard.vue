<template>
  <div class="admin-dashboard">
    <!-- Header with Language Toggle -->
    <!-- <div class="admin-header">
      <h1>Admin dashboard</h1>
    </div> -->

    <!-- Urgent Alert -->
    <el-alert 
      type="warning" 
      title="Immediate Action Needed" 
      show-icon
      style="margin-bottom: 20px;"
    >
      <span>3 seats need cleaning in Room B</span>
      <el-button type="warning" size="mini" style="margin-left: 10px;">
        Mark as Cleaned
      </el-button>
    </el-alert>

    <!-- Stats Cards -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <h3>{{ dashboardStats.total_classrooms }}</h3>
            <p>Total Rooms</p>
            <el-tag type="success" effect="dark">{{ dashboardStats.available_classroom_count }} Available</el-tag>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <h3>{{ dashboardStats.available_seats_count }}</h3>
            <p>Available Seats</p>
            <el-tag type="warning" effect="dark">{{ dashboardStats.empty_seats_count }} Reserved</el-tag>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <h3>{{ dashboardStats.available_classroom_count }}</h3>
            <p>Available Rooms</p>
            <el-tag type="warning" effect="dark">{{ dashboardStats.empty_classroom_count }} Reserved</el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Main Tabs -->
    <el-tabs v-model="activeTab">
      <el-tab-pane label="Rooms" name="rooms">
        <room-management @room-status-changed="handleRoomStatusUpdate" />
      </el-tab-pane>
      <el-tab-pane label="Seats" name="seats">
        <seat-management ref="seatManagement" @seat-status-changed="handleSeatStatusUpdate" />
      </el-tab-pane>
      <el-tab-pane label="Users" name="users">
        <user-management />
      </el-tab-pane>
      <el-tab-pane label="Settings" name="settings">
        <system-settings />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import RoomManagement from '../../components/admin/RoomManagement.vue'
import UserManagement from '../../components/admin/UserManagement.vue'
import SystemSettings from '../../components/admin/SystemSettings.vue'
import SeatManagement from '@/components/admin/SeatManagement.vue'
import axios from 'axios'

export default {
  components: {
    RoomManagement,
    UserManagement,
    SystemSettings,
    SeatManagement
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
    }
  },
  methods: {
    changeLanguage(lang) {
      this.currentLanguage = lang
      this.$message.success(`Language changed to ${lang === 'en' ? 'English' : 'Chinese'}`)
    },

    handleRoomStatusUpdate() {
      const seatManagementComponent = this.$refs.seatManagement;
      if (seatManagementComponent) {
        seatManagementComponent.fetchSeats();
        this.$message.info('Seat list refreshed due to room status change.');
      }
      // Refresh dashboard stats when room status changes
      this.fetchDashboardStats();
    },
    
    handleSeatStatusUpdate() {
      // Refresh dashboard stats when seat status changes
      this.fetchDashboardStats();
    },
    
    async fetchDashboardStats() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/dashboard/admin/status/');
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
}
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.language-toggle {
  cursor: pointer;
  color: #666;
  font-size: 14px;
}
.language-toggle:hover {
  color: #409EFF;
}
.stats-row {
  margin-bottom: 20px;
}
.stat-card {
  text-align: center;
  padding: 15px 0;
  border-top: 3px solid #409EFF;
}
.stat-card h3 {
  font-size: 32px;
  margin: 0;
  color: #409EFF;
}
.stat-card p {
  margin: 5px 0;
  font-weight: bold;
}
</style>