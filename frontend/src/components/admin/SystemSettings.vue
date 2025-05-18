<template>
  <el-card class="system-settings" shadow="never">
    <div slot="header">
      <span>{{ $t('systemControls') }}</span>
    </div>

    <el-form label-width="200px">
      <!-- System Status -->
      <el-form-item :label="$t('systemStatus')">
        <el-switch
          v-model="isSystemOnline"
          :active-text="$t('online')"
          :inactive-text="$t('maintenance')"
          @change="handleSystemToggle"
        />
      </el-form-item>

      <!-- Max Booking Hours -->
      <el-form-item :label="$t('maxBookingHours')">
        <el-input-number 
          v-model="maxHours" 
          :min="1" 
          :max="24" 
        />
      </el-form-item>

      <!-- No-Show Policy -->
      <el-form-item :label="$t('noShowPolicy')">
        <el-input-number
          v-model="noShowLimit"
          :min="1"
          :max="10"
        />
        <span class="hint-text">{{ $t('noShowStrikesHint') }}</span>
      </el-form-item>

      <el-form-item>
        <el-button 
          type="primary" 
          @click="saveSettings"
          :loading="saving"
        >
          {{ $t('saveSettings') }}
        </el-button>
      </el-form-item>
    </el-form>
  </el-card>
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
    async handleSystemToggle() {
      try {
        await this.$confirm(
          `${this.$t('switchSystemTo')} ${this.$t(this.isSystemOnline ? 'online' : 'maintenance')} ${this.$t('mode')}?`,
          this.$t('warning'),
          { confirmButtonText: this.$t('confirm') }
        )
        await this.saveSettings()
      } catch {
        this.isSystemOnline = !this.isSystemOnline
      }
    },
    async saveSettings() {
      this.saving = true
      try {
        await adminApi.updateSystemSettings({
          status: this.isSystemOnline ? 'online' : 'maintenance',
          max_hours: this.maxHours,
          no_show_strikes: this.noShowLimit
        })
        this.$message.success(this.$t('settingsSavedMessage'))
      } catch (error) {
        console.error("Save failed:", error)
        this.$message.error(this.$t('saveError'))
      } finally {
        this.saving = false
      }
    }
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