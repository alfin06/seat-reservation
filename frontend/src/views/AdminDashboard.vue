<template>
  <div class="admin-dashboard">
    <!-- Header -->
    <div class="admin-header">
      <h1>{{ $t('adminTitle') }}</h1>
    </div>

    <!-- Urgent Alert -->
    <el-alert 
      v-if="showCleaningAlert"
      type="warning" 
      :title="$t('urgentAlertTitle')" 
      show-icon
      style="margin-bottom: 20px;"
    >
      <span>{{ $t('cleaningNotice') }}</span>
      <el-button 
        type="warning" 
        size="mini" 
        style="margin-left: 10px;"
        @click="dismissCleaningAlert"
      >
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
    <el-tabs v-model="activeTab" class="dashboard-tabs">
      <el-tab-pane :label="$t('tabRooms')" name="rooms">
        <RoomManagement />
      </el-tab-pane>
      <el-tab-pane :label="$t('tabUsers')" name="users">
        <UserManagement />
      </el-tab-pane>
      <el-tab-pane :label="$t('tabSettings')" name="settings">
        <SystemSettings />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import RoomManagement from '../components/admin/RoomManagement.vue'
import UserManagement from '../components/admin/UserManagement.vue'
import SystemSettings from '../components/admin/SystemSettings.vue'

export default {
  components: { RoomManagement, UserManagement, SystemSettings },
  data() {
    return {
      activeTab: 'rooms',
      showCleaningAlert: true
    }
  },
  methods: {
    dismissCleaningAlert() {
      this.showCleaningAlert = false
      this.$message.success(this.$t('cleaningMarkedComplete'))
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

.admin-header {
  margin-bottom: 20px;
}

.admin-header h1 {
  color: #303133;
  font-size: 24px;
  margin: 0;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  height: 100%;
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-content {
  padding: 15px;
  text-align: center;
}

.stat-content h3 {
  font-size: 28px;
  margin: 0 0 8px 0;
  font-weight: 600;
}

.stat-content p {
  margin: 0 0 10px 0;
  font-weight: 500;
  color: #606266;
}

.dashboard-tabs {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>