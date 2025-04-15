<template>
  <div class="system-settings">
    <el-card shadow="never">
      <div slot="header">
        <span>{{ $t('systemControls') }}</span>
      </div>

      <el-form label-width="200px">
        <el-form-item :label="$t('systemStatus')">
          <el-switch
            v-model="isSystemOnline"
            :active-text="$t('online')"
            :inactive-text="$t('maintenance')"
            @change="handleSystemToggle"
          />
        </el-form-item>

        <el-form-item :label="$t('maxBookingHours')">
          <el-input-number 
            v-model="maxBookingHours" 
            :min="1" 
            :max="8" 
            @change="saveSettings"
          />
        </el-form-item>

        <el-form-item :label="$t('noShowPolicy')">
          <el-input-number
            v-model="noShowLimit"
            :min="1"
            :max="10"
            @change="saveSettings"
          />
          <span style="margin-left: 10px; color: #666;">
            {{ $t('noShowStrikesHint') }}
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
        `${this.$t('switchSystemTo')} ${this.$t(this.isSystemOnline ? 'online' : 'maintenance')} ${this.$t('mode')}?`,
        this.$t('warning'),
        { confirmButtonText: this.$t('confirm') }
      ).then(() => {
        this.saveSettings()
      }).catch(() => {
        this.isSystemOnline = !this.isSystemOnline
      })
    },
    saveSettings() {
      this.$message.success(this.$t('settingsSaved'))
      // TODO: API call here
    }
  }
}
</script>

<style scoped>
.system-settings {
  padding: 20px;
}
</style>
