export default {
  // ========================
  // Original Room Management
  // ========================
  fetchRoomData() {
    return Promise.resolve({
      data: [
        { id: 1, name: "Room A", capacity: 20, status: "active" },
        { id: 2, name: "Room B", capacity: 15, status: "inactive" }
      ]
    })
  },
  insertClassroom(roomData) {
    console.log("[MOCK] Saving room:", roomData)
    return Promise.resolve({
      data: { ...roomData }
    })
  },
  removeClassroom(roomId) {
    console.log("[MOCK] Deleting room:", roomId)
    return Promise.resolve({ success: true })
  },

  // ======================
  // Original Seat Handling
  // ======================
  getSeatAvailability() {
    return new Promise((resolve) => {
      setTimeout(() => resolve({
        data: [
          { id: 1, room: "Room A", seat: "Seat 1", status: "available" },
          { id: 2, room: "Room A", seat: "Seat 2", status: "booked" },
          { id: 3, room: "Room B", seat: "Seat 1", status: "available" }
        ]
      }), 500)
    })
  },
  bookSeat(seatId) {
    console.log("[MOCK] Booking seat:", seatId)
    return Promise.resolve({ 
      data: { success: true, bookedSeat: seatId } 
    })
  },
  markCleaned(seats) {
    console.log("[MOCK] Cleaning seats:", seats)
    return Promise.resolve({ success: true })
  },

  // ===================
  // Original User Admin
  // ===================
  getUsers() {
    return Promise.resolve({
      data: {
        users: [
          { name: "Test Student", email: "student@uni.edu", role: "student", status: "active" },
          { name: "Test Admin", email: "admin@uni.edu", role: "admin", status: "active" }
        ],
        stats: {
          activeUsers: 2,
          administrators: 1,
          newToday: 1
        }
      }
    })
  },

  // ======================
  // Booking Management
  // ======================
  getBookings() {
    return Promise.resolve({
      data: [
        {
          id: 1,
          room_name: "Room A",
          seat_number: "Seat 3",
          start_time: new Date(Date.now() + 86400000).toISOString(), // Tomorrow
          end_time: new Date(Date.now() + 86760000).toISOString(), // +1 hour
          status: "ACTIVE"
        },
        {
          id: 2,
          room_name: "Room B",
          seat_number: "Seat 5",
          start_time: new Date(Date.now() - 86400000).toISOString(), // Yesterday
          end_time: new Date(Date.now() - 82800000).toISOString(), // -1 hour
          status: "COMPLETED"
        },
        {
          id: 3,
          room_name: "Room C",
          seat_number: "Seat 2",
          start_time: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
          end_time: new Date(Date.now() - 169200000).toISOString(),
          status: "CANCELLED"
        }
      ]
    })
  },
  cancelBooking(bookingId) {
    console.log("[MOCK] Cancelled booking ID:", bookingId)
    return new Promise((resolve) => {
      setTimeout(() => resolve({ 
        data: { 
          success: true,
          cancelledId: bookingId 
        } 
      }), 300)
    })
  },

  // ======================
  // NEW System Settings
  // ======================
  getSystemSettings() {
    return new Promise((resolve) => {
      setTimeout(() => resolve({
        data: {
          status: "online",
          max_hours: 4,
          no_show_strikes: 3,
          maintenance_message: "System under scheduled maintenance",
          last_updated: new Date().toISOString()
        }
      }), 200)
    })
  },
  updateSystemSettings(settings) {
    console.log("[MOCK] Updating system settings:", settings)
    return new Promise((resolve) => {
      setTimeout(() => resolve({
        data: {
          ...settings,
          last_updated: new Date().toISOString(),
          updated_by: "mock-admin@uni.edu"
        }
      }), 400)
    })
  }
}