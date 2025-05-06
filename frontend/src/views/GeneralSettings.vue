<template>
    <div class="settings-container">
      <h2>{{ $t('generalSettingsTitle') }}</h2>
      <form @submit.prevent="saveSettings" class="settings-form">
        <div class="form-group">
          <label for="maxHours">{{ $t('maxHoursPerBooking') }}</label>
          <input
            id="maxHours"
            type="number"
            v-model.number="settings.maxHoursPerBooking"
            min="1"
            class="form-input"
          />
        </div>
  
        <div class="form-group">
          <label for="maxBookings">{{ $t('maxBookingsPerAccount') }}</label>
          <input
            id="maxBookings"
            type="number"
            v-model.number="settings.maxBookingsPerAccount"
            min="1"
            class="form-input"
          />
        </div>
  
        <div class="form-group">
          <label>{{ $t('openingHours') }}</label>
          <div class="opening-hours">
            <div class="time-range" v-for="(range, index) in settings.openingHours" :key="index">
              <input
                type="time"
                v-model="range.from"
                class="form-input time-input"
              />
              <span class="time-separator">-</span>
              <input
                type="time"
                v-model="range.to"
                class="form-input time-input"
              />
              <button type="button" class="remove-button" @click="removeRange(index)">×</button>
            </div>
            <button type="button" class="add-button" @click="addRange">+ {{ $t('addTimeRange') }}</button>
          </div>
        </div>
  
        <div class="form-group">
          <label for="others">{{ $t('otherSettings') }}</label>
          <textarea
            id="others"
            v-model="settings.others"
            class="form-textarea"
            rows="4"
          ></textarea>
        </div>
  
        <button type="submit" class="save-button">{{ $t('saveSettings') }}</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'GeneralSettings',
    data() {
      return {
        settings: {
          maxHoursPerBooking: 4,
          maxBookingsPerAccount: 5,
          openingHours: [
            { from: '09:00', to: '17:00' }
          ],
          others: ''
        }
      };
    },
    methods: {
      addRange() {
        this.settings.openingHours.push({ from: '09:00', to: '17:00' });
      },
      removeRange(index) {
        this.settings.openingHours.splice(index, 1);
      },
      saveSettings() {
        // Placeholder: emit or call API to save settings
        console.log('Settings saved:', this.settings);
        this.$toast.success(this.$t('settingsSavedMessage'));
      }
    }
  };
  </script>
  
  <style scoped>
  .settings-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .settings-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
  }
  
  .form-input,
  .form-textarea {
    padding: 8px;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .opening-hours {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .time-range {
    display: flex;
    align-items: center;
    gap: 5px;
  }
  
  .time-input {
    width: 120px;
  }
  
  .time-separator {
    margin: 0 5px;
  }
  
  .add-button,
  .remove-button,
  .save-button {
    background-color: #409eff;
    color: white;
    border: none;
    padding: 8px 12px;
    font-size: 0.9rem;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .remove-button {
    background-color: #ff4d4f;
  }
  
  .add-button {
    align-self: flex-start;
    background-color: #67c23a;
  }
  
  .save-button {
    align-self: flex-end;
  }
  </style>
  