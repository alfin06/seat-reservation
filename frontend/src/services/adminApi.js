import axios from 'axios'
import mockApi from './mockAdminApi'

const API_BASE_URL = 'http://127.0.0.1:8000/dashboard/admin/'

const realApi = {
  fetchRoomData() {
    return axios.get(`${API_BASE_URL}status/room/`)
  },
  insertClassroom(roomData) {
    return axios.post(`${API_BASE_URL}classroom/insert/`, roomData)
  },
  removeClassroom(roomId) {
    return axios.post(`${API_BASE_URL}classroom/remove/`, { room_id: roomId })
  },
  getSeatAvailability() {
    return axios.get(`${API_BASE_URL}seats/availability`)
  },
  bookSeat(seatId) {
    return axios.post(`${API_BASE_URL}seats/book`, { seat_id: seatId })
  },
  markCleaned(seats) {
    return axios.post(`${API_BASE_URL}seats/clean`, { seats })
  },
  getUsers() {
    return axios.get(`${API_BASE_URL}status/user/`)
  },
  getBookings() {
    return axios.get(`${API_BASE_URL}bookings/user`)
  },
  cancelBooking(bookingId) {
    return axios.delete(`${API_BASE_URL}bookings/${bookingId}`)
  },
  getSystemSettings() {
    return axios.get(`${API_BASE_URL}system/settings`)
  },
  updateSystemSettings(settings) {
    return axios.post(`${API_BASE_URL}system/settings/update`, settings)
  }
}

export default new Proxy(realApi, {
  get(target, prop) {
    return async (...args) => {
      try {
        return await target[prop](...args)
      } catch (err) {
        console.error(`API Error - Using mock for ${prop}:`, err)
        return mockApi[prop](...args)
      }
    }
  }
})