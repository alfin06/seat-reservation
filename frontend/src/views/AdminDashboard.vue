<template>
  <div class="admin-dashboard">
    <!-- Header -->
    <div class="admin-header">
      <h1>{{ $t('adminTitle') }}</h1>
    </div>

    <!-- Urgent Alert -->
    <el-alert 
      type="warning" 
      :title="$t('urgentAlertTitle')" 
      show-icon
      style="margin-bottom: 20px;"
    >
      <span>{{ $t('cleaningNotice') }}</span>
      <el-button type="warning" size="mini" style="margin-left: 10px;">
        {{ $t('markAsCleaned') }}
      </el-button>
    </el-alert>

    <!-- Stats Cards -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <h3>8</h3>
            <p>{{ $t('totalRooms') }}</p>
            <el-tag type="success" effect="dark">{{ $t('newRoomsTag') }}</el-tag>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <h3>24</h3>
            <p>{{ $t('activeBookings') }}</p>
            <el-tag type="warning" effect="dark">{{ $t('endingSoonTag') }}</el-tag>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-content">
            <h3>2</h3>
            <p>{{ $t('todaysNoShows') }}</p>
            <el-tag type="danger" effect="dark">{{ $t('noShowDropTag') }}</el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Main Tabs -->
    <el-tabs v-model="activeTab">
      <el-tab-pane :label="$t('tabRooms')" name="rooms">
        <room-management />
      </el-tab-pane>
      <el-tab-pane :label="$t('tabUsers')" name="users">
        <user-management />
      </el-tab-pane>
      <el-tab-pane :label="$t('tabSettings')" name="settings">
        <system-settings />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import RoomManagement from '../components/admin/RoomManagement.vue'
import UserManagement from '../components/admin/UserManagement.vue'
import SystemSettings from '../components/admin/SystemSettings.vue'

export default {
  components: {
    RoomManagement,
    UserManagement,
    SystemSettings
  },
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
  max-width: 1200px;
  margin: 0 auto;
}
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
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
