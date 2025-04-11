<template>
    <div class="system-settings">
      <el-card shadow="never">
        <div slot="header">
          <span>System Controls</span>
        </div>
  
        <el-form label-width="200px">
          <el-form-item label="System Status">
            <el-switch
              v-model="isSystemOnline"
              active-text="Online"
              inactive-text="Maintenance"
              @change="handleSystemToggle"
            />
          </el-form-item>
  
          <el-form-item label="Max Booking Hours">
            <el-input-number 
              v-model="maxBookingHours" 
              :min="1" 
              :max="8" 
              @change="saveSettings"
            />
          </el-form-item>
  
          <el-form-item label="No-Show Policy">
            <el-input-number
              v-model="noShowLimit"
              :min="1"
              :max="10"
              @change="saveSettings"
            />
            <span style="margin-left: 10px; color: #666;">
              strikes before penalty
            </span>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        isSystemOnline: true,
        maxBookingHours: 4,
        noShowLimit: 3
      }
    },
    methods: {
      handleSystemToggle() {
        this.$confirm(
          `Switch system to ${this.isSystemOnline ? 'ONLINE' : 'MAINTENANCE'} mode?`,
          'Warning',
          { confirmButtonText: 'Confirm' }
        ).then(() => {
          this.saveSettings()
        }).catch(() => {
          this.isSystemOnline = !this.isSystemOnline // Revert if canceled
        })
      },
      saveSettings() {
        this.$message.success('Settings saved successfully')
        // Add API call here later
      }
    }
  }
  </script>
  
  <style scoped>
  .system-settings {
    padding: 20px;
  }
  </style>