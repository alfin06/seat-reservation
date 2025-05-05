<template>
  <div class="instant-booking">
    <h2>Instant Booking</h2>
    <div class="booking-methods">
      <button class="active">
        <span>📷</span> Scan QR Code
      </button>
    </div>

    <!-- QR Scanner -->
    <div v-if="!scannedSeat" class="scanner-section">
      
      <div class="scanner-container">
        <video ref="videoElement" class="scanner-video" :class="{ 'd-none': !cameraReady }"></video>
        <div class="scanner-overlay">
          
        </div>
        <div v-if="!cameraReady" class="d-flex justify-content-center align-items-center h-100 bg-light">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading camera...</span>
          </div>
        </div>
      </div>
      <p class="scanner-hint">Point your camera at the seat's QR code</p>
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

    <!-- Back to Home Button -->
    <div class="text-center mt-4">
      <button class="btn btn-primary w-100 py-3 rounded-3" @click="goHome">
        🏠 Back to Home
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { BrowserQRCodeReader } from '@zxing/browser'
import { useRouter } from 'vue-router'
import { useAuthStore, getCSRFToken } from "../../store/auth.js"
import { notify } from "@kyvg/vue3-notification"
import axios from 'axios'

const router = useRouter()
const authStore = useAuthStore()
const videoElement = ref(null)
const scannedSeat = ref(null)
const duration = ref(1)
const error = ref('')
const success = ref('')
const booking = ref(false)
const cameraReady = ref(false)
const scannedValue = ref('')
const scanningStopped = ref(false)
let codeReader = null

const startScanning = async () => {
  if (!videoElement.value) return
  
  cameraReady.value = false
  error.value = ''
  scannedValue.value = ''
  
  try {
    codeReader = new BrowserQRCodeReader()
    const devices = await BrowserQRCodeReader.listVideoInputDevices()
    if (devices.length > 0) {
      await codeReader.decodeFromVideoDevice(
        devices[0].deviceId,
        videoElement.value,
        (result, error, controls) => {
          cameraReady.value = true;
          if (result && scannedValue.value !== result.getText()) {
            scannedValue.value = result.getText();
            onDecode(scannedValue.value);
          }
        }
      )
    } else {
      notify({ type: 'error', title: '<em>ERROR</em>', duration: 10000, text: 'No camera found!' })
    }
  } catch (err) {
    error.value = 'Failed to initialize camera'
    console.error('Camera initialization failed:', err)
  }
}

const stopScanning = () => {
  cameraReady.value = false
  scannedValue.value = ''
  if (codeReader) {
    codeReader.reset()
    codeReader = null
  }

  // Stop the video stream if it's running
  if (videoElement.value && videoElement.value.srcObject) {
    const stream = videoElement.value.srcObject
    const tracks = stream.getTracks()
    tracks.forEach(track => track.stop())
    videoElement.value.srcObject = null
  }
}

const onDecode = async (decodedString) => {
  if (!decodedString || scannedSeat.value || scanningStopped.value) return; // Prevent multiple scans
  error.value = '';
  success.value = '';
  try {
    const response = await axios.post('http://localhost:8000/dashboard/api/qr-check/', {
      seat_id: decodedString
    }, {
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`,
        'X-CSRFToken': getCSRFToken()
      }
    });
    scannedSeat.value = response.data;
    error.value = '';
    scanningStopped.value = true;
    notify({ type: 'success', title: '<em>SUCCESS</em>', duration: 10000, text: 'Seat found and ready to book!' });
    stopScanning();
  } catch (err) {
    if (!scanningStopped.value) {
      error.value = err.response?.data?.error || 'Failed to scan or find seat';
      notify({ type: 'error', title: '<em>ERROR</em>', duration: 10000, text: error.value });
      scanningStopped.value = true;
      stopScanning();
    }
  }
};

const cancelScan = () => {
  scannedSeat.value = null
  error.value = ''
  success.value = ''
  startScanning()
}

const bookSeat = async () => {
  if (!scannedSeat.value) return
  booking.value = true
  error.value = ''
  success.value = ''
  try {
    const response = await axios.post('http://localhost:8000/dashboard/api/instant-booking/', {
      seat_id: scannedSeat.value.seat_id,
      duration: duration.value
    }, {
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`,
        'X-CSRFToken': getCSRFToken()
      }
    })
    success.value = 'Seat booked and checked in! Reservation ID: ' + response.data.reservation_id
    notify({ type: 'success', title: '<em>SUCCESS</em>', duration: 10000, text: success.value })
    setTimeout(() => {
      router.push('/checkin')
    }, 1500)
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to book seat'
    notify({ type: 'error', title: '<em>ERROR</em>', duration: 10000, text: error.value })
  } finally {
    booking.value = false
  }
}

const goHome = () => {
  router.push('/home')
}

watch(videoElement, async (newVal) => {
  if (newVal) {
    await nextTick();
    startScanning();
  } else {
    stopScanning();
  }
});

onMounted(async () => {
  if (videoElement.value) {
    await nextTick();
    startScanning();
  }
});

onBeforeUnmount(() => {
  stopScanning()
})
</script>

<style scoped>
.instant-booking {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.booking-methods {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.booking-methods button {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  background: #f8f9fa;
  color: #495057;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.booking-methods button.active {
  background: #007bff;
  color: white;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

.scanner-section {
  margin-bottom: 2rem;
}

.scanner-section h3 {
  margin-bottom: 1rem;
  color: #343a40;
  font-weight: 600;
}

.scanner-container {
  position: relative;
  width: 100%;
  height: 300px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.scanner-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.scanner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.scanner-line {
  width: 80%;
  height: 2px;
  background: #007bff;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.5);
  animation: scan 2s linear infinite;
}

@keyframes scan {
  0% { transform: translateY(-50%); }
  50% { transform: translateY(50%); }
  100% { transform: translateY(-50%); }
}

.scanner-hint {
  margin-top: 1rem;
  color: #6c757d;
  font-size: 0.9rem;
  text-align: center;
}

.seat-details {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.seat-details h3 {
  margin-bottom: 1rem;
  color: #343a40;
  font-weight: 600;
}

.seat-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.seat-info p {
  margin: 0;
  color: #495057;
}

.seat-info p strong {
  color: #343a40;
}

.booking-actions {
  display: flex;
  gap: 1rem;
}

.booking-actions button {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.booking-actions button:first-child {
  background: #dc3545;
  color: white;
}

.booking-actions button:last-child {
  background: #28a745;
  color: white;
}

.booking-actions button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.error-message {
  background: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.success-message {
  background: #d4edda;
  color: #155724;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
</style> 