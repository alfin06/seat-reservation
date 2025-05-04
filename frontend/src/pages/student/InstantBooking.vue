<template>
  <div class="instant-booking">
    <h2>Instant Booking</h2>
    <div class="booking-methods">
      <button :class="{active: method === 'qr'}" @click="method = 'qr'">
        <span>📷</span> Scan QR Code
      </button>
      <button :class="{active: method === 'manual'}" @click="method = 'manual'">
        <span>🔢</span> Enter Seat ID
      </button>
    </div>

    <!-- QR Scanner -->
    <div v-if="method === 'qr' && !scannedSeat" class="scanner-section">
      <h3>Scan QR Code</h3>
      <div v-if="loadingCamera" class="loading-spinner">
        <span class="spinner"></span>
        <p>Initializing camera...</p>
      </div>
      <div v-else class="scanner-container">
        <qrcode-stream @decode="onDecode" @init="onInit">
          <div class="scanner-overlay">
            <div class="scanner-line"></div>
          </div>
        </qrcode-stream>
      </div>
      <p class="scanner-hint">Point your camera at the seat's QR code</p>
    </div>

    <!-- Manual Entry -->
    <div v-if="method === 'manual' && !scannedSeat" class="manual-section">
      <h3>Enter Seat ID</h3>
      <input v-model="manualSeatId" placeholder="Enter seat ID" />
      <button @click="onDecode(manualSeatId)" class="btn-primary">Book with Seat ID</button>
    </div>

    <!-- Booking Form -->
    <div v-if="scannedSeat" class="booking-form">
      <h3>Book Seat</h3>
      <div class="seat-info">
        <p><strong>Seat:</strong> {{ scannedSeat.seat_name }}</p>
        <p><strong>Room:</strong> {{ scannedSeat.classroom }}</p>
        <p><strong>Location:</strong> {{ scannedSeat.location }}</p>
      </div>

      <div class="duration-selector">
        <label for="duration">Duration (hours):</label>
        <select v-model="duration" id="duration">
          <option value="1">1 hour</option>
          <option value="2">2 hours</option>
          <option value="3">3 hours</option>
          <option value="4">4 hours</option>
        </select>
      </div>

      <div class="actions">
        <button @click="cancelScan" class="btn-secondary">Cancel</button>
        <button @click="bookSeat" class="btn-primary" :disabled="booking">
          {{ booking ? 'Booking...' : 'Book Now' }}
        </button>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="error-message">
      <span>❌</span> {{ error }}
    </div>
    <!-- Success Message -->
    <div v-if="success" class="success-message">
      <span>✅</span> {{ success }}
    </div>
    <button class="back-home-bottom" @click="goHome">🏠 Back to Home</button>
  </div>
</template>

<script>
//import { QrcodeStream } from 'vue-qrcode-reader'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'InstantBooking',
  components: {
    //QrcodeStream
  },
  setup() {
    const router = useRouter()
    const scannedSeat = ref(null)
    const duration = ref(1)
    const error = ref('')
    const success = ref('')
    const booking = ref(false)
    const manualSeatId = ref('')
    const method = ref('qr')
    const loadingCamera = ref(false)

    const onDecode = async (decodedString) => {
      error.value = ''
      success.value = ''
      if (!decodedString) return
      try {
        const response = await axios.post('/dashboard/api/qr-check/', {
          seat_id: decodedString
        })
        scannedSeat.value = response.data
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to scan or find seat'
      }
    }

    const onInit = (promise) => {
      loadingCamera.value = true
      promise.then(() => {
        loadingCamera.value = false
      }).catch(errorObj => {
        loadingCamera.value = false
        error.value = 'Failed to initialize camera'
        console.error('Camera initialization failed:', errorObj)
      })
    }

    const cancelScan = () => {
      scannedSeat.value = null
      error.value = ''
      success.value = ''
      manualSeatId.value = ''
      method.value = 'qr'
    }

    const bookSeat = async () => {
      if (!scannedSeat.value) return
      booking.value = true
      error.value = ''
      success.value = ''
      try {
        const response = await axios.post('/dashboard/api/instant-booking/', {
          seat_id: scannedSeat.value.seat_id,
          duration: duration.value
        })
        success.value = 'Seat booked and checked in! Reservation ID: ' + response.data.reservation_id
        setTimeout(() => {
          router.push('/checkin')
        }, 1500)
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to book seat'
      } finally {
        booking.value = false
      }
    }

    const goHome = () => {
      router.push('/home')
    }

    return {
      scannedSeat,
      duration,
      error,
      success,
      booking,
      manualSeatId,
      method,
      loadingCamera,
      onDecode,
      onInit,
      cancelScan,
      bookSeat,
      goHome
    }
  }
}
</script>

<style scoped>
.instant-booking {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  position: relative;
}
.back-home-bottom {
  display: block;
  margin: 40px auto 0 auto;
  background: #f5f5f5;
  color: #333;
  border: none;
  border-radius: 4px;
  padding: 12px 28px;
  font-size: 18px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  z-index: 10;
}
.back-home-bottom:hover {
  background: #4CAF50;
  color: white;
}
.booking-methods {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}
.booking-methods button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background: #f5f5f5;
  color: #333;
  cursor: pointer;
  font-size: 16px;
  transition: background 0.2s, color 0.2s;
}
.booking-methods button.active {
  background: #4CAF50;
  color: white;
}
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 30px 0;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #4CAF50;
  border-top: 4px solid #eee;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.scanner-section {
  text-align: center;
}
.scanner-container {
  width: 100%;
  max-width: 400px;
  margin: 20px auto;
  position: relative;
  aspect-ratio: 1;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
}
.scanner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 2px solid #4CAF50;
  border-radius: 8px;
}
.scanner-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: #4CAF50;
  animation: scan 2s linear infinite;
}
@keyframes scan {
  0% { top: 0; }
  50% { top: 100%; }
  100% { top: 0; }
}
.scanner-hint {
  color: #666;
  margin-top: 10px;
}
.manual-section {
  text-align: center;
  margin: 30px 0;
}
.manual-section input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 200px;
  margin-right: 10px;
}
.booking-form {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-top: 30px;
}
.seat-info {
  margin: 20px 0;
  padding: 15px;
  background: #f5f5f5;
  border-radius: 4px;
}
.duration-selector {
  margin: 20px 0;
}
.duration-selector select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-top: 5px;
}
.actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}
.btn-primary, .btn-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  flex: 1;
}
.btn-primary {
  background: #4CAF50;
  color: white;
}
.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.btn-secondary {
  background: #f5f5f5;
  color: #333;
}
.error-message {
  color: #f44336;
  margin-top: 10px;
  text-align: center;
  font-size: 16px;
}
.success-message {
  color: #4CAF50;
  margin-top: 10px;
  text-align: center;
  font-size: 16px;
}
</style> 