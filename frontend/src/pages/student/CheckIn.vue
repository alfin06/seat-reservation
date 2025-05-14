<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { BrowserQRCodeReader } from '@zxing/browser';
import { useRouter } from 'vue-router';
import { useAuthStore, getCSRFToken } from "../../store/auth.js";
import { notify } from "@kyvg/vue3-notification";
import { Tooltip } from 'bootstrap';

const video = ref(null);
const scannedValue = ref('');
const apiResult = ref('');
const router = useRouter();
const authStore = useAuthStore();
let codeReader;

const cameraReady = ref(false);

function navigate(route) {
  router.push(route);
}

async function callApi(qrValue) {
  const token = localStorage.getItem('token');

  try {
    const response = await fetch('http://localhost:8000/dashboard/api/check-qr/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${token}`,
        'X-CSRFToken': getCSRFToken()
      },
      credentials: 'include',
      body: JSON.stringify({
        user_id: authStore.user.id,
        qrCode: qrValue
      }),
    });

    const data = await response.json();
    if (response.status === 201) {
      notify({ type: "success", title: 'SUCCESS', duration: 3000, text: "Check-in successful!" });
    } else {
      notify({ type: "error", title: 'ERROR', duration: 3000, text: "No valid reservation for check-in found." });
    }
  } catch (error) {
    notify({ type: "error", title: 'ERROR', duration: 3000, text: "No valid reservation for check-in found." });
    console.log('API Error: ' + error);
  }
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
});
</script>

<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col py-4 px-3 px-md-5 d-flex justify-content-center">
        <div class="card shadow-sm border-0 rounded-4 w-100 w-md-75 w-lg-50 animate__animated animate__fadeIn" style="max-width: 800px;">
          <div class="card-body d-flex flex-column">

            <!-- Back Button -->
            <button class="btn btn-outline-primary mb-3 align-self-start" @click="$router.push('/home')">
              <i class="bi bi-arrow-left me-2"></i> {{ $t('backToHome') }}
            </button>

            <!-- Title and Tooltip -->
            <div class="d-flex justify-content-start align-items-center mb-2 gap-2">
              <h2 class="h5 text-primary fw-semibold m-0">{{ $t('qrCodeScanner') }}</h2>
              <i
                class="bi bi-question-circle-fill text-secondary"
                data-bs-toggle="tooltip"
                data-bs-placement="right"
                title="Align your QR code within the camera frame. The scanner will detect it automatically."
                style="cursor: pointer;"
              ></i>
            </div>

            <p class="text-muted mb-4">{{ $t('scanInstruction') }}</p>

            <!-- Scanner Area -->
            <div
              class="mb-4 w-100"
              style="
                height: 250px;
                overflow: hidden;
                border-radius: 1rem;
                box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.1);
                position: relative;">
              <video ref="video" class="w-100 h-100" :class="{ 'd-none': !cameraReady }"></video>

              <!-- Spinner -->
              <div v-if="!cameraReady" class="d-flex justify-content-center align-items-center h-100 bg-light">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading camera...</span>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
video {
  object-fit: cover;
}

.card {
  max-width: 600px;
  margin: 0 auto;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 0.75rem 1.5rem rgba(0, 0, 0, 0.05);
}
</style>
