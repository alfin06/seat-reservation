<template>

  <div class="">
    <el-card shadow="never">
      <div v-if="isLoadingInitial" class="loading-state">
        <span>Please wait...</span>
      </div>
      <div v-else-if="initialError" class="error-state">
        Error loading settings: {{ initialError }}. Displaying default values.
      </div>

      <el-form v-else label-width="200px" @submit.prevent>
        <el-form-item label="Max Booking Hours">
          <el-input-number v-model="editableMaxBookingDuration"
            :min="1"
            :max="24"
            placeholder="Hours"
            @change="handleMaxBookingDurationUpdate"
            :disabled="isUpdating" />
        </el-form-item>

      </el-form>
    </el-card>
  </div>
</template>

<script>
import adminApi from '@/services/adminApi'

export default {
  data() {
    return {
      isSystemOnline: true,
      maxHours: 4,
      noShowLimit: 3,
      saving: false
    }
  },
  async created() {
    await this.loadSettings()
  },
  methods: {
    async loadSettings() {
      try {
        const response = await adminApi.getSystemSettings()
        this.isSystemOnline = response.data.status === 'online'
        this.maxHours = response.data.max_hours
        this.noShowLimit = response.data.no_show_strikes
      } catch (error) {
        console.error("Failed to load settings:", error)
      }
    },

    async handleMaxBookingDurationUpdate(currentValue) {
      if (currentValue === null || currentValue === undefined) {
        this.$message.warning('Max booking hours cannot be empty. Reverting.');
        this.editableMaxBookingDuration = this.maxBookingDuration; // Revert to store's value
        return;
      }
      
      this.isUpdating = true;
      const result = await this.updateSettingInStore({ max_booking_duration: currentValue});
      this.isUpdating = false;

      if (result.success) {
        this.$message.success(result.message);
      } else {
        this.$message.error(result.message + " Reverting to previous value.");
        this.editableMaxBookingDuration = this.maxBookingDuration; // Revert on failure
      }
    },
  }
}
</script>

<style scoped>
.system-settings {
  padding: 20px;
}
.hint-text {
  margin-left: 10px;
  color: #666;
  font-size: 0.9em;
}
</style>