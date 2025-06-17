<template>
  <div class="user-management">
    <el-card shadow="never">
      <div slot="header">
        <span>User Statistics</span>
        <el-button type="text" @click="refreshUsers" style="float: right;">
          <i class="el-icon-refresh"></i> Refresh
        </el-button>
      </div>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="stat-item">
            <h3>{{ stats.active_users }}</h3>
            <p>Active Users</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <h3>{{ stats.administrators }}</h3>
            <p>Administrators</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <h3>{{ stats.new_today }}</h3>
            <p>New Today</p>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-card shadow="never" style="margin-top: 30px;">
      <el-input
        v-model="searchQuery"
        placeholder="Search users by name or email..."
        prefix-icon="el-icon-search"
        clearable
        style="width: 400px; margin-bottom: 20px;" />
      <el-table :data="filteredUsers" style="width: 100%; margin-top: 20px;">
        <el-table-column label="#" width="60">
          <template #default="scope">
            {{ scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="name" label="Name" />
        <el-table-column prop="email" label="Email" />
        <el-table-column prop="role" label="Role" />
        <el-table-column prop="is_active" label="Active" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'">
              {{ row.is_active ? 'Yes' : 'No' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchQuery: '',
      stats: {
        active_users: 0,
        administrators: 0,
        new_today: 0
      },
      users: []
    };
  },
  computed: {
    filteredUsers() {
      const q = this.searchQuery.toLowerCase();
      return this.users.filter(user =>
        user.name.toLowerCase().includes(q) ||
        user.email.toLowerCase().includes(q)
      );
    }
  },
  created() {
    this.fetchUserStats();
    this.fetchAllUsers();
  },
  methods: {
    async fetchUserStats() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/users/api/statistics/', {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
          }
        });
        this.stats = response.data;
      } catch (error) {
        this.$message.error('Failed to fetch user statistics');
      }
    },
    async fetchAllUsers() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/users/api/all/', {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
          }
        });
        console.log("User data:", response.data);
        this.users = response.data;
      } catch (error) {
        this.$message.error('Failed to fetch user list');
      }
    },
    refreshUsers() {
      this.fetchUserStats();
      this.fetchAllUsers();
      this.$message.success('User data refreshed');
    }
  }
};
</script>

<style scoped>
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
