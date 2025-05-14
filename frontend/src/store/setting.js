import { defineStore } from 'pinia';
import { useAuthStore, getCSRFToken } from './auth.js';
import axios from 'axios'; 

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    // Default values, will be overwritten by fetched values
    maxBookingDuration: 4,
    resetHour: '23:00',
    isLoading: false,
    error: null,
  }),
  getters: {
    getMaxBookingDuration: (state) => state.maxBookingDuration,
    getResetHour: (state) => state.resetHour,
  },
  actions: {
    async fetchSettings() {
      this.isLoading = true;
      this.error = null;
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:8000/dashboard/admin/setting/', {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
            'X-CSRFToken': getCSRFToken()
          },
        });
        if (response.data) {
          if (response.data.data[0].max_booking_duration !== undefined && response.data.data[0].max_booking_duration !== null) {
            this.maxBookingDuration = parseInt(response.data.data[0].max_booking_duration, 10);
          }
          if (response.data.data[0].reset_time !== undefined && response.data.data[0].reset_time !== null) {
            this.resetHour = response.data.data[0].reset_time.substring(0, 5); // "HH:mm"
          }
        }
                console.log('Settings fetched:', { maxBookingDuration: this.maxBookingDuration, resetHour: this.resetHour });
      } catch (err) {
        console.error('Failed to fetch system settings:', err);
        this.error = 'Failed to load system settings.';
      } finally {
        this.isLoading = false;
      }
    },
    async updateSetting(payload) {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('Authentication token not found.');
        return { success: false, message: 'Not authenticated for updating settings.' };
      }
      try {
        await axios.put('http://127.0.0.1:8000/dashboard/admin/setting-update/', 
          payload, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
            'X-CSRFToken': getCSRFToken()
          },
        });

        if (payload.max_booking_duration !== undefined) {
          this.maxBookingDuration = parseInt(payload.max_booking_duration, 10);
        }
        if (payload.reset_time !== undefined) {
          this.openingHour = payload.reset_time;
        }
        return { success: true, message: 'Setting updated successfully.' };
      } catch (error) {
        console.error('Failed to update setting:', error.response?.data || error.message, 'Payload:', payload);
        return { success: false, message: error.response?.data?.detail || 'Failed to update setting.' };
      }
    }
  }
});