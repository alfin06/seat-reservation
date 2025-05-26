<template>
  <div class="booking-history">
    <h2>{{ $t('bookingHistory.title') }}</h2>

    <!-- Filter Bar -->
    <div class="filter-bar">
      <select v-model="filters.room" class="filter-select">
        <option value="all">{{ $t('bookingHistory.filters.allRooms') }}</option>
        <option v-for="room in uniqueRooms" :key="room" :value="room">{{ room }}</option>
      </select>

      <div class="date-filter-container">
        <button @click="toggleDatePicker" class="date-filter-btn">
          {{ dateFilterDisplay }}
          <span class="calendar-icon">📅</span>
        </button>
        <div v-if="showDatePicker" class="calendar-popup">
          <VDatePicker 
            v-model="selectedDate" 
            mode="date"
            is-range
            @update:modelValue="handleDateSelection"
          />
        </div>
      </div>

      <select v-model="filters.status" class="filter-select">
        <option value="all">{{ $t('bookingHistory.filters.allStatuses') }}</option>
        <option value="ACTIVE">{{ $t('bookingHistory.statuses.active') }}</option>
        <option value="COMPLETED">{{ $t('bookingHistory.statuses.completed') }}</option>
        <option value="CANCELLED">{{ $t('bookingHistory.statuses.cancelled') }}</option>
      </select>

      <button @click="resetFilters" class="reset-btn">{{ $t('bookingHistory.filters.reset') }}</button>
    </div>

    <!-- Bookings Table -->
    <table class="bookings-table">
      <thead>
        <tr>
          <th>{{ $t('bookingHistory.table.room') }}</th>
          <th>{{ $t('bookingHistory.table.seat') }}</th>
          <th>{{ $t('bookingHistory.table.date') }}</th>
          <th class="time-column">{{ $t('bookingHistory.table.time') }}</th>
          <th>{{ $t('bookingHistory.table.status') }}</th>
          <th>{{ $t('bookingHistory.table.action') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="booking in filteredBookings" :key="booking.id">
          <td><strong>{{ booking.room }}</strong></td>
          <td>{{ booking.seat }}</td>
          <td>{{ formatDate(booking.startTime) }}</td>
          <td class="time-column">{{ formatTime(booking.startTime) }} - {{ formatTime(booking.endTime) }}</td>
          <td>
            <span :class="['status-badge', booking.status.toLowerCase()]">
              {{ $t(`bookingHistory.statuses.${booking.status.toLowerCase()}`) }}
            </span>
          </td>
          <td>
            <button 
              v-if="booking.status === 'ACTIVE'" 
              @click="showCancelModal(booking)"
              class="cancel-btn"
            >
              {{ $t('bookingHistory.cancel') }}
            </button>
            <span v-else class="muted">{{ $t('bookingHistory.noAction') }}</span>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="table-footer">
      {{ $t('bookingHistory.showingBookings', { count: filteredBookings.length }) }}
    </div>

    <!-- Confirmation Modal -->
    <div v-if="cancelModal" class="modal-overlay">
      <div class="modal">
        <h3>{{ $t('bookingHistory.modal.title') }}</h3>
        <div class="modal-actions">
          <button @click="cancelModal = null" class="keep-btn">{{ $t('bookingHistory.modal.keep') }}</button>
          <button @click="confirmCancel" class="confirm-btn">{{ $t('bookingHistory.modal.confirm') }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { DatePicker as VDatePicker } from 'v-calendar';
import 'v-calendar/dist/style.css';

export default {
  name: 'BookingHistory',
  components: {
    VDatePicker
  },
  data() {
    return {
      bookings: [],
      filters: {
        room: 'all',
        date: 'all',
        status: 'all'
      },
      cancelModal: null,
      showDatePicker: false,
      selectedDate: null
    }
  },
  computed: {
    uniqueRooms() {
      return [...new Set(this.bookings.map(b => b.room))].sort();
    },
    dateFilterDisplay() {
      if (this.filters.date === 'all') return this.$t('bookingHistory.filters.allDates');
      if (this.selectedDate?.start && this.selectedDate?.end) {
        const start = this.formatDate(this.selectedDate.start);
        const end = this.formatDate(this.selectedDate.end);
        return start === end ? start : `${start} - ${end}`;
      }
      return this.$t('bookingHistory.filters.selectDate');
    },
    filteredBookings() {
      return this.bookings.filter(booking => {
        const roomMatch = this.filters.room === 'all' || booking.room === this.filters.room;
        const dateMatch = this.checkDateMatch(booking.startTime);
        const statusMatch = this.filters.status === 'all' || booking.status === this.filters.status;
        return roomMatch && dateMatch && statusMatch;
      });
    }
  },
  methods: {
    async fetchBookingHistory() {
  console.log('[BookingHistory] fetchBookingHistory called');

  try {
    const token = localStorage.getItem('token');
    if (!token) {
      console.warn('[BookingHistory] No auth token found. Skipping API call.');
      return;
    }

    const response = await fetch('http://localhost:8000/api/reservations/history/', {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Fetch failed: ${response.status}`);
    }

    const data = await response.json();
    console.log('[BookingHistory] Data fetched:', data);

    this.bookings = data.map(entry => ({
      id: entry.id,
      room: entry.classroom,
      seat: entry.seat_name,
      startTime: entry.reserved_at,
      endTime: entry.reserved_end,
      status: this.mapStatus(entry.status)
    }));
  } catch (error) {
    console.error('[BookingHistory] Failed to fetch booking history:', error);
  }
},
    mapStatus(code) {
      switch (code) {
        case '0': return 'ACTIVE';
        case '1': return 'COMPLETED';
        case '2': return 'CANCELLED';
        default: return 'UNKNOWN';
      }
    },
    checkDateMatch(bookingDate) {
      if (this.filters.date === 'all') return true;
      if (!this.selectedDate?.start || !this.selectedDate?.end) return true;

      const bookingDateTime = new Date(bookingDate).getTime();
      const startDateTime = new Date(this.selectedDate.start).setHours(0, 0, 0, 0);
      const endDateTime = new Date(this.selectedDate.end).setHours(23, 59, 59, 999);

      return bookingDateTime >= startDateTime && bookingDateTime <= endDateTime;
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}/${String(date.getMonth() + 1).padStart(2, '0')}/${String(date.getDate()).padStart(2, '0')}`;
    },
    formatTime(dateString) {
      return new Date(dateString).toLocaleTimeString(this.$i18n.locale, {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      }).replace(/^0/, '');
    },
    resetFilters() {
      this.filters = {
        room: 'all',
        date: 'all',
        status: 'all'
      };
      this.selectedDate = null;
      this.showDatePicker = false;
    },
    showCancelModal(booking) {
      this.cancelModal = booking;
    },
    confirmCancel() {
      if (this.cancelModal) {
        const index = this.bookings.findIndex(b => b.id === this.cancelModal.id);
        if (index !== -1) {
          this.bookings[index].status = 'CANCELLED';
        }
        this.cancelModal = null;
      }
    },
    toggleDatePicker() {
      this.showDatePicker = !this.showDatePicker;
    },
    handleDateSelection(dateRange) {
      if (dateRange) {
        this.filters.date = 'selected';
        this.selectedDate = dateRange;
      }
      this.showDatePicker = false;
    }
  },
  mounted() {
    this.fetchBookingHistory();
  }
}
</script>

<style scoped>
/* keep your existing style unchanged */
</style>
<style scoped>
/* ===== BASE STYLES ===== */
.booking-history {
  max-width: 1000px;
  margin: 0 auto;
  padding: 15px;
  font-family: 'Segoe UI', system-ui, sans-serif;
}

/* ===== FILTER BAR ===== */
.filter-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-select {
  padding: 10px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  background-color: white;
  font-size: 14px;
  flex-grow: 1;
  min-width: 120px;
  appearance: none;
  background-image: 
    linear-gradient(45deg, transparent 50%, #555 50%),
    linear-gradient(135deg, #555 50%, transparent 50%);
  background-position:
    calc(100% - 15px) center,
    calc(100% - 10px) center;
  background-size: 5px 5px, 5px 5px;
  background-repeat: no-repeat;
}

.date-filter-container {
  position: relative;
  flex-grow: 1;
  min-width: 120px;
}

.date-filter-btn {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  background-color: white;
  font-size: 14px;
  text-align: left;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.calendar-icon {
  font-size: 16px;
}

.calendar-popup {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 100;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  margin-top: 5px;
}

.reset-btn {
  padding: 10px 15px;
  background: #f5f5f5;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.reset-btn:hover {
  background: #e0e0e0;
}

/* ===== TABLE STYLES ===== */
.bookings-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 15px;
  font-size: 15px;
}

.bookings-table th, 
.bookings-table td {
  padding: 12px 10px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.bookings-table th {
  background-color: #f8f8f8;
  font-weight: 600;
  color: #333;
  position: sticky;
  top: 0;
}

/* ===== ENHANCED STATUS BADGES ===== */
.status-badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
  display: inline-block;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.active {
  background-color: rgba(46, 125, 50, 0.1);
  color: #2e7d32;
  border-left: 3px solid #2e7d32;
}

.completed {
  background-color: rgba(97, 97, 97, 0.1);
  color: #616161;
  border-left: 3px solid #616161;
}

.cancelled {
  background-color: rgba(198, 40, 40, 0.1);
  color: #c62828;
  border-left: 3px solid #c62828;
}

/* ===== INTERACTIVE ELEMENTS ===== */
.cancel-btn {
  background: none;
  border: none;
  color: #e74c3c;
  cursor: pointer;
  padding: 5px 0;
  font-size: 14px;
  text-decoration: underline;
  transition: color 0.2s;
}

.cancel-btn:hover {
  color: #c0392b;
  text-decoration: none;
}

.bookings-table tbody tr {
  transition: background-color 0.2s;
}

.bookings-table tbody tr:hover {
  background-color: #f8f9fa;
}

/* ===== TIME COLUMN ===== */
.time-column {
  font-feature-settings: "tnum";
  white-space: nowrap;
}

/* ===== FOOTER ===== */
.table-footer {
  text-align: right;
  color: #666;
  font-size: 14px;
  padding: 10px 5px;
}

/* ===== MODAL ===== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  padding: 25px;
  border-radius: 10px;
  width: 90%;
  max-width: 350px;
  text-align: center;
  box-shadow: 0 5px 20px rgba(0,0,0,0.15);
}

.modal h3 {
  margin: 0 0 20px;
  color: #2c3e50;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.modal-btn {
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
  flex: 1;
}

.keep-btn {
  background: #f5f5f5;
  border: 1px solid #ddd;
  color: #333;
}

.keep-btn:hover {
  background: #e0e0e0;
}

.confirm-btn {
  background: #e74c3c;
  color: white;
  border: none;
}

.confirm-btn:hover {
  background: #c0392b;
}

/* ===== MOBILE STYLES ===== */
@media (max-width: 768px) {
  .booking-history {
    padding: 10px;
  }
  
  .filter-bar {
    flex-direction: column;
    gap: 8px;
  }
  
  .filter-select, .reset-btn, .date-filter-btn {
    width: 100%;
  }
  
  .bookings-table {
    font-size: 14px;
  }
  
  .bookings-table th, 
  .bookings-table td {
    padding: 8px 6px;
  }
  
  .modal-actions {
    flex-direction: column;
  }
  
  .modal-btn {
    width: 100%;
  }
  
  /* Stack time on small screens */
  @media (max-width: 480px) {
    .time-column {
      display: block;
      text-align: left;
      padding-left: 10px;
    }
  }
}
</style>