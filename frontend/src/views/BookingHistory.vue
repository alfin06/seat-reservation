<template>
    <div class="booking-history">
      <h2>Booking History</h2>
      
      <!-- Filter Bar -->
      <div class="filter-bar">
        <select v-model="filters.room" class="filter-select">
          <option value="all">All Rooms</option>
          <option v-for="room in uniqueRooms" :key="room" :value="room">{{ room }}</option>
        </select>
        
        <select v-model="filters.date" class="filter-select">
          <option value="all">All Dates</option>
          <option v-for="date in uniqueDates" :key="date" :value="date">{{ date }}</option>
        </select>
        
        <select v-model="filters.status" class="filter-select">
          <option value="all">All Statuses</option>
          <option value="ACTIVE">Active</option>
          <option value="COMPLETED">Completed</option>
          <option value="CANCELLED">Cancelled</option>
        </select>
        
        <button @click="resetFilters" class="reset-btn">Reset</button>
      </div>
  
      <!-- Bookings Table -->
      <table class="bookings-table">
        <thead>
          <tr>
            <th>Room</th>
            <th>Seat</th>
            <th>Date</th>
            <th class="time-column">Time</th>
            <th>Status</th>
            <th>Action</th>
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
                {{ booking.status }}
              </span>
            </td>
            <td>
              <button 
                v-if="booking.status === 'ACTIVE'" 
                @click="showCancelModal(booking)"
                class="cancel-btn"
              >
                Cancel
              </button>
              <span v-else class="muted">-</span>
            </td>
          </tr>
        </tbody>
      </table>
  
      <div class="table-footer">
        Showing {{ filteredBookings.length }} bookings
      </div>
  
      <!-- Confirmation Modal -->
      <div v-if="cancelModal" class="modal-overlay">
        <div class="modal">
          <h3>Cancel this booking?</h3>
          <div class="modal-actions">
            <button @click="cancelModal = null" class="keep-btn">Keep Booking</button>
            <button @click="confirmCancel" class="confirm-btn">Yes, Cancel</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'BookingHistory',
    data() {
      return {
        bookings: [
          {
            id: 1,
            room: "Room A",
            seat: "Seat 1",
            startTime: "2025-05-02T09:00:00",
            endTime: "2025-05-02T11:00:00",
            status: "ACTIVE"
          },
          {
            id: 2,
            room: "Room A",
            seat: "Seat 3",
            startTime: "2025-05-01T14:00:00",
            endTime: "2025-05-01T16:00:00",
            status: "ACTIVE"
          },
          {
            id: 3,
            room: "Room C",
            seat: "Seat 2",
            startTime: "2025-04-30T13:00:00",
            endTime: "2025-04-30T15:00:00",
            status: "CANCELLED"
          },
          {
            id: 4,
            room: "Room B",
            seat: "Seat 4",
            startTime: "2025-04-29T16:00:00",
            endTime: "2025-04-29T18:00:00",
            status: "COMPLETED"
          },
          {
            id: 5,
            room: "Room B",
            seat: "Seat 5",
            startTime: "2025-04-28T10:00:00",
            endTime: "2025-04-28T12:00:00",
            status: "COMPLETED"
          }
        ],
        filters: {
          room: 'all',
          date: 'all',
          status: 'all'
        },
        cancelModal: null
      }
    },
    computed: {
      uniqueRooms() {
        return [...new Set(this.bookings.map(b => b.room))].sort()
      },
      uniqueDates() {
        return [...new Set(this.bookings.map(b => this.formatDate(b.startTime)))].sort().reverse()
      },
      filteredBookings() {
        return this.bookings.filter(booking => {
          const roomMatch = this.filters.room === 'all' || booking.room === this.filters.room
          const dateMatch = this.filters.date === 'all' || 
            this.formatDate(booking.startTime) === this.filters.date
          const statusMatch = this.filters.status === 'all' || 
            booking.status === this.filters.status
          
          return roomMatch && dateMatch && statusMatch
        })
      }
    },
    methods: {
      formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('en-US', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        })
      },
      formatTime(dateString) {
        return new Date(dateString).toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit'
        }).replace(/^0/, '')
      },
      resetFilters() {
        this.filters = {
          room: 'all',
          date: 'all',
          status: 'all'
        }
      },
      showCancelModal(booking) {
        this.cancelModal = booking
      },
      confirmCancel() {
        if (this.cancelModal) {
          const index = this.bookings.findIndex(b => b.id === this.cancelModal.id)
          if (index !== -1) {
            this.bookings[index].status = 'CANCELLED'
          }
          this.cancelModal = null
        }
      }
    }
  }
  </script>
  
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
    
    .filter-select, .reset-btn {
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
  
  /* ===== LOADING STATE ===== */
  .loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255,255,255,0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1001;
  }
  
  .loading-spinner {
    border: 3px solid #f3f3f3;
    border-top: 3px solid #3498db;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    animation: spin 1s linear infinite;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  </style>

