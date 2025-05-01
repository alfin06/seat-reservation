<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { BrowserQRCodeReader } from '@zxing/browser';
import { useRouter } from 'vue-router';
import { useAuthStore, getCSRFToken } from "../../store/auth.js";
  
const video = ref(null);
const scannedValue = ref('');
const apiResult = ref('');
const router = useRouter();
const authStore = useAuthStore();
let codeReader;
//await this.authStore.setCsrfToken();
  
function navigate(route) {
    router.push(route);
}
  
async function callApi(qrValue) {
    try {
        const response = await fetch('http://localhost:8000/dashboard/api/check-qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(),
            },
            body: JSON.stringify({ qrCode: qrValue }),
        });
        const data = await response.json();
        apiResult.value = JSON.stringify(data);
    } catch (error) {
        apiResult.value = 'API Error: ' + error.message;
    }
}
  
onMounted(async () => {
    codeReader = new BrowserQRCodeReader();
    const previewVideoElement = video.value;
  
    try {
        const devices = await BrowserQRCodeReader.listVideoInputDevices();
        if (devices.length > 0) {
            await codeReader.decodeFromVideoDevice(devices[0].deviceId, previewVideoElement, (result, error, controls) => {
                if (result) {
                    if (scannedValue.value !== result.getText()) {
                        scannedValue.value = result.getText();
                        callApi(scannedValue.value);
                        controls.stop();
                    }
                }
            });
        } else {
            console.error('No camera found.');
        }
    } catch (error) {
        console.error('Error starting QR scanner:', error);
    }
});
  
onBeforeUnmount(() => {
    if (codeReader && typeof codeReader.reset === 'function') {
        codeReader.reset();
        codeReader = null;
    }

    // Stop the video stream if it's running
    if (video.value && video.value.srcObject) {
        const stream = video.value.srcObject;
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop()); // Stop all tracks (video)
        video.value.srcObject = null; // Clear the stream from the video element
    }
});
</script>

<template>
    <div class="container py-4 d-flex flex-column min-vh-100">
        <!-- Scanner Section -->
        <div class="flex-grow-1 mb-4">
            <h1 class="h4 fw-bold mb-3 text-center">QR Code Scanner</h1>
  
            <!-- Smaller Camera Box -->
            <div class="mx-auto mb-3" style="width: 300px; height: 225px; overflow: hidden; border-radius: 12px; box-shadow: 0 0 10px rgba(0,0,0,0.2);">
                <video ref="video" class="w-100 h-100 object-fit-cover"></video>
            </div>
  
            <!-- Status Messages -->
            <div v-if="scannedValue" class="alert alert-success text-center">
                Scanned QR: {{ scannedValue }}
            </div>
            <div v-if="apiResult" class="alert alert-info text-center">
                API Response: {{ apiResult }}
            </div>
        </div>
  
        <!-- Back Button -->
        <div class="mt-auto">
            <router-link to="/home" class="btn btn-secondary w-100 rounded-3 py-3">
             ← Back to Home
            </router-link>
        </div>
    </div>
</template>
  
<style scoped>
video {
    object-fit: cover;
}
</style>
  