<template>
  <div class="user-management">
    <el-input
      v-model="searchQuery"
      :placeholder="$t('searchUsersPlaceholder')"
      prefix-icon="el-icon-search"
      clearable
      style="width: 400px; margin-bottom: 20px;"
    />

    <el-card shadow="never">
      <div slot="header">
        <span>{{ $t('userStats') }}</span>
        <el-button 
          type="text" 
          @click="refreshUsers" 
          style="float: right;"
          :loading="loading"
        >
          <i class="el-icon-refresh"></i> {{ $t('refresh') }}
        </el-button>
      </div>

      <el-row :gutter="20">
        <el-col :span="8">
          <div class="stat-item">
            <h3>{{ userStats.activeUsers || 0 }}</h3>
            <p>{{ $t('activeUsers') }}</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <h3>{{ userStats.administrators || 0 }}</h3>
            <p>{{ $t('administrators') }}</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <h3>{{ userStats.newToday || 0 }}</h3>
            <p>{{ $t('newToday') }}</p>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-table 
      :data="filteredUsers" 
      border 
      style="margin-top: 20px;"
      v-loading="loading"
    >
      <el-table-column prop="name" :label="$t('name')" sortable></el-table-column>
      <el-table-column prop="email" :label="$t('email')"></el-table-column>
      <el-table-column :label="$t('role')" width="120">
        <template #default="{row}">
          <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">
            {{ row.role }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column :label="$t('status')" width="120">
        <template #default="{row}">
          <el-tag :type="row.status === 'active' ? 'success' : 'warning'">
            {{ row.status }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import adminApi from '@/services/adminApi'

export default {
  data() {
    return {
      searchQuery: '',
      userStats: {
        activeUsers: 0,
        administrators: 0,
        newToday: 0
      },
      users: [],
      loading: false
    }
  },
  async created() {
    await this.fetchUserData()
  },
  computed: {
    filteredUsers() {
      return this.users.filter(user => 
        user.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        user.email.toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    }
  },
  methods: {
    async fetchUserData() {
      this.loading = true
      try {
        const response = await adminApi.getUsers()
        this.users = response.data.users || []
        this.userStats = response.data.stats || {
          activeUsers: 0,
          administrators: 0,
          newToday: 0
        }
      } catch (error) {
        this.$message.error(this.$t('fetchError'))
        console.error(error)
      } finally {
        this.loading = false
      }
    },
    async refreshUsers() {
      await this.fetchUserData()
      this.$message.success(this.$t('usersRefreshed'))
    }
  }
}
</script>

<style scoped>
.user-management {
  padding: 20px;
}
.stat-item {
  text-align: center;
  padding: 15px;
}
.stat-item h3 {
  font-size: 24px;
  margin: 0;
  color: #409EFF;
}
.stat-item p {
  margin: 5px 0 0;
  color: #666;
}
</style>