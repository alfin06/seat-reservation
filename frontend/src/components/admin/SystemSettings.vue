<template>
  <el-card class="system-settings">
    <h3>System Controls</h3>
    <el-form>
      <el-form-item label="System Status">
        <el-switch
          v-model="isSystemOnline"
          active-text="Online"
          inactive-text="Maintenance"
        />
      </el-form-item>
      <el-form-item label="Max Booking Hours">
        <el-input-number v-model="maxHours" :min="1" :max="24" />
      </el-form-item>
      <el-form-item label="No-Show Policy">
        <el-input-number v-model="noShowLimit" :min="1" :max="10" />
        <span style="margin-left: 10px; color: #666;">strikes before penalty</span>
      </el-form-item>
      <el-button type="primary" @click="saveSettings">Save Settings</el-button>
    </el-form>
  </el-card>
</template>

<script>
export default {
  data() {
    return {
      isSystemOnline: true,
      maxHours: 4,
      noShowLimit: 3
    }
  },
  methods: {
    saveSettings() {
      this.$message.success('Settings saved successfully');
    }
  }
}
</script>

<style scoped>
.system-settings {
  padding: 20px;
}
</style>