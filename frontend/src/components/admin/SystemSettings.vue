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
import { useSettingsStore } from "@/store/setting.js";
import { mapState, mapActions } from 'pinia';

export default {
  name: 'SystemSettings',
  data() {
    return {
      editableMaxBookingDuration: 4,
      editableResetHour: '23:00',
      
      isLoadingInitial: true,
      initialError: null,
      isUpdating: false,
    };
  },
  computed: {
    ...mapState(useSettingsStore, ['maxBookingDuration', 'resetHour', 'error']),
  },
  watch: {
    maxBookingDuration(newValue) {
      this.editableMaxBookingDuration = newValue;
    },
    resetHour(newValue) {
      this.editableResetHour = newValue;
    }
  },
  async mounted() {
    this.isLoadingInitial = true;
    this.initialError = null; // Reset error on mount

    try {
      await this.fetchSettingsStore(); 
      this.editableMaxBookingDuration = this.maxBookingDuration;
      this.editableResetHour = this.resetHour;

    } catch (e) {
     
        console.error("Error during fetchSettingsStore dispatch:", e);
        this.initialError = "Failed to dispatch fetch settings.";
    } finally {
        if (this.error) {
            this.initialError = this.error;
        }
        this.isLoadingInitial = false;
        
        console.log('SystemSettings mounted. Store values:', {
            hours: this.maxBookingDuration,
            time: this.resetHour
        });
        console.log('SystemSettings mounted. Editable values set to:', {
            hours: this.editableMaxBookingDuration,
            time: this.editableResetHour
        });
    }
  },
  methods: {
    // Map actions from Pinia store
    ...mapActions(useSettingsStore, {
        fetchSettingsStore: 'fetchSettings', 
        updateSettingInStore: 'updateSetting'
    }),

    getTimestampFromTime(timeStr) {
      const match = timeStr.match(/(\d{2})(\d{2})/)
      if (match) {
        const hours = match[1];
        const minutes = match[2];
        timeStr = `${hours}:${minutes}` + ':00';
      }

      return timeStr; // e.g. "2025-05-14T20:25:00"
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
};
</script>

<style scoped>
.system-settings {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.loading-state, .error-state {
  text-align: center;
  padding: 20px;
  color: grey;
}
.error-state {
  color: red;
}
</style>