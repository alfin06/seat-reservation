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
            <h3>8</h3>
            <p>Total Rooms</p>
            <el-tag type="success" effect="dark">+2 New</el-tag>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <h3>24</h3>
            <p>Active Bookings</p>
            <el-tag type="warning" effect="dark">3 Ending Soon</el-tag>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <h3>2</h3>
            <p>Today's No-Shows</p>
            <el-tag type="danger" effect="dark">-10% from avg</el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Main Tabs -->
    <el-tabs v-model="activeTab">
      <el-tab-pane label="Rooms" name="rooms">
        <room-management />
      </el-tab-pane>
      <el-tab-pane label="Seats" name="seats">
        <seat-management />
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
import RoomManagement from '../components/admin/RoomManagement.vue'
import UserManagement from '../components/admin/UserManagement.vue'
import SystemSettings from '../components/admin/SystemSettings.vue'
import SeatManagement from '@/components/admin/SeatManagement.vue'

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
      currentLanguage: 'en'
    }
  },
  methods: {
    changeLanguage(lang) {
      this.currentLanguage = lang
      this.$message.success(`Language changed to ${lang === 'en' ? 'English' : 'Chinese'}`)
    }
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