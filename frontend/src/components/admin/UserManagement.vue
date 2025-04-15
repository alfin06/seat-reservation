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
        <el-button type="text" @click="refreshUsers" style="float: right;">
          <i class="el-icon-refresh"></i> {{ $t('refresh') }}
        </el-button>
      </div>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="stat-item">
            <h3>24</h3>
            <p>{{ $t('activeUsers') }}</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <h3>3</h3>
            <p>{{ $t('administrators') }}</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-item">
            <h3>2</h3>
            <p>{{ $t('newToday') }}</p>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: ''
    }
  },
  methods: {
    refreshUsers() {
      this.$message.success(this.$t('usersRefreshed'))
    }
  }
}
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
