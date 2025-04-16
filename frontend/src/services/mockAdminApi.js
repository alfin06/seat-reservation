export default {
  // Room Management
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

  // Keep all existing mocks
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
  }
}