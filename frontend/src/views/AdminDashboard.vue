<template>
  <div class="admin-dashboard">
    <h1>{{ $t('adminTitle') }}</h1>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card total-rooms">
        <h3>8</h3>
        <p>{{ $t('adminDashboard.totalRooms') }}</p>
        <el-tag type="success" size="small">+3 New</el-tag>
      </div>
      <div class="stat-card active-bookings">
        <h3>24</h3>
        <p>{{ $t('adminDashboard.activeBookings') }}</p>
        <el-tag type="warning" size="small">1 Ending Soon</el-tag>
      </div>
      <div class="stat-card no-shows">
        <h3>2</h3>
        <p>{{ $t('adminDashboard.todayNoShows') }}</p>
        <el-tag type="danger" size="small">10% from avg</el-tag>
      </div>
    </div>

    <!-- Tabs -->
    <el-tabs v-model="activeTab" class="dashboard-tabs">
      <el-tab-pane :label="$t('adminRoomManagement')" name="rooms">
        <RoomManagement />
      </el-tab-pane>
      <el-tab-pane :label="$t('adminUserManagement')" name="users">
        <UserManagement />
      </el-tab-pane>
      <el-tab-pane :label="$t('systemControls')" name="settings">
        <SystemSettings />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import RoomManagement from '@/components/admin/RoomManagement.vue'
import UserManagement from '@/components/admin/UserManagement.vue'
import SystemSettings from '@/components/admin/SystemSettings.vue'

export default {
  components: { RoomManagement, UserManagement, SystemSettings },
  data() {
    return {
      activeTab: 'rooms'
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.stats-grid {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  flex: 1;
  text-align: center;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.15);
}

.stat-card h3 {
  font-size: 28px;
  margin: 0 0 8px 0;
  font-weight: 600;
}

.stat-card p {
  margin: 0 0 10px 0;
  font-weight: 500;
  color: #606266;
}

.total-rooms h3 {
  color: #409EFF;
}

.active-bookings h3 {
  color: #E6A23C;
}

.no-shows h3 {
  color: #F56C6C;
}

.dashboard-tabs {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>