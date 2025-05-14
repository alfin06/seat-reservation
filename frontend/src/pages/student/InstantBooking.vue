<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';
import { BrowserQRCodeReader } from '@zxing/browser';
import { useRouter, onBeforeRouteLeave } from 'vue-router';
import { useAuthStore, getCSRFToken } from "../../store/auth.js";
import { notify } from "@kyvg/vue3-notification";
import axios from 'axios';
import { Tooltip } from 'bootstrap';

const router = useRouter();
const authStore = useAuthStore();
const video = ref(null);
const scannedSeat = ref(null);
const duration = ref(1);
const error = ref('');
const success = ref('');
const booking = ref(false);
const cameraReady = ref(false);
const scannedValue = ref('');
const scanningStopped = ref(false);
let codeReader = null;

const stopCamera = async () => {
  if (codeReader && typeof codeReader.reset === 'function') {
    codeReader.reset();
    codeReader = null;
  }

  if (video.value && video.value.srcObject) {
    const stream = video.value.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach(track => track.stop());
    video.value.srcObject = null;
  }
};

async function callApi(decodedString) {
  if (!decodedString || scannedSeat.value || scanningStopped.value) return;

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
    scanningStopped.value = true;
    notify({ type: 'success', title: 'SUCCESS', duration: 3000, text: 'Seat found and ready to book!' });
    await stopCamera();
    await nextTick();
  } catch (err) {
    // if (!scanningStopped.value) {
    //   notify({ type: 'error', title: 'ERROR', duration: 3000, text: err.response?.data?.error });
    //   scanningStopped.value = true;
    //   await stopScanning();
    // }
    notify({ type: 'error', title: 'ERROR', duration: 3000, text: err.response?.data?.error });
  }
};

const bookSeat = async () => {
  if (!scannedSeat.value) return;
  booking.value = true;
  error.value = '';
  success.value = '';

  try {
    const response = await axios.post('http://localhost:8000/dashboard/api/instant-booking/', {
      seat_id: scannedSeat.value.seat_id,
      duration: duration.value
    }, {
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`,
        'X-CSRFToken': getCSRFToken()
      }
    });

    success.value = 'Seat booked and checked in!';
    notify({ type: 'success', title: 'SUCCESS', duration: 10000, text: success.value });
    router.push('/home');
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to book seat';
    notify({ type: 'error', title: 'ERROR', duration: 10000, text: error.value });
  } finally {
    booking.value = false;
  }
};

function navigate(route) {
  router.push(route);
}

onMounted(async () => {
  codeReader = new BrowserQRCodeReader();
  const previewVideoElement = video.value;

  try {
    const devices = await BrowserQRCodeReader.listVideoInputDevices();
    if (devices.length > 0) {
      await codeReader.decodeFromVideoDevice(devices[0].deviceId, previewVideoElement, (result, error, controls) => {
        cameraReady.value = true;
        setTimeout(() => {
          scannedValue.value = "";
        }, 5000); // 5 seconds cooldown
        if (result && scannedValue.value !== result.getText()) {
          scannedValue.value = result.getText();
          callApi(scannedValue.value);
        }
      });
    } else {
      notify({ type: 'error', text: 'No camera found!' });
    }
  } catch (error) {
    notify({ type: 'error', text: 'Error starting QR scanner!' });
    console.error('QR Error:', error);
  }

  // Initialize all tooltips
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipTriggerList.forEach(el => new Tooltip(el));
});

onBeforeUnmount(() => {
  stopCamera();
});
</script>


<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col py-4 px-3 px-md-5 d-flex justify-content-center">
        <div class="card shadow-sm border-0 rounded-4 w-100" style="max-width: 800px;">
          <div class="card-body d-flex flex-column">

            <!-- Back Button -->
            <button class="btn btn-outline-primary mb-3 align-self-start" @click="$router.push('/home')">
              <i class="bi bi-arrow-left me-2"></i> {{ $t('backToHome') }}
            </button>

            <!-- Title with Tooltip -->
            <div class="d-flex align-items-center mb-2 gap-2">
              <h2 class="h5 text-primary fw-bold m-0">{{ $t('instantBooking') }}</h2>
              <i class="bi bi-question-circle-fill text-secondary" data-bs-toggle="tooltip" data-bs-placement="right"
                title="Align your QR code within the camera frame. The scanner will detect it automatically."
                style="cursor: pointer;"></i>
            </div>
            <p class="text-muted mb-4">{{ $t('scanInstruction2') }}</p>

            <!-- QR Scanner -->
            <div v-if="!scannedSeat" class="mb-4 w-100" style="height: 250px; border-radius: 1rem; box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.1); position: relative;">
              <video ref="video" class="w-100 h-100" :class="{ 'd-none': !cameraReady }"></video>
              <div class="scanner-overlay"></div>
              <div v-if="!cameraReady" class="d-flex justify-content-center align-items-center h-100 bg-light">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading camera...</span>
                </div>
              </div>
            </div>

            <!-- Booking Form -->
            <div v-if="scannedSeat">
              <h2 class="h6 text-primary fw-bold mb-3">{{ $t('bookYourSeat') }}</h2>
              <div class="seat-info mb-3">
                <div class="row mb-2">
                  <div class="col-4 fw-semibold">Room:</div>
                  <div class="col-8">{{ (scannedSeat.classroom.split("-"))[0] }}</div>
                </div>
                <div class="row mb-2">
                  <div class="col-4 fw-semibold">Location:</div>
                  <div class="col-8">{{ scannedSeat.location }}</div>
                </div>
                <div class="row">
                  <div class="col-4 fw-semibold">Duration:</div>
                  <div class="col-8">
                    <select v-model="duration" class="form-select">
                      <option value="1">1 hour</option>
                      <option value="2">2 hours</option>
                      <option value="3">3 hours</option>
                      <option value="4">4 hours</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Actions -->
              <div class="actions text-center">
                <button @click="bookSeat" class="btn btn-success" :disabled="booking">
                  <i class="bi bi-calendar-check"></i>&nbsp;{{ booking ? 'Booking...' : 'Book Now' }}
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

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

.scanner-section {
  margin-bottom: 2rem;
}

.scanner-section h3 {
  margin-bottom: 1rem;
  font-weight: 600;
}

.scanner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

@keyframes scan {
  0% { transform: translateY(-50%); }
  50% { transform: translateY(50%); }
  100% { transform: translateY(-50%); }
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

video {
  object-fit: cover;
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

.actions {
  margin: 25px;
  text-align: center;
  padding: 10px;
}
</style> 