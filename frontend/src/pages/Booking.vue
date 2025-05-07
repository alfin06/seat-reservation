<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import {getCSRFToken} from '../store/auth'

const router = useRouter();
const available = ref([]);
const selectedClassroom = ref('');
const selectedSeat = ref('');
const duration = ref(1);
const message = ref('');
const loading = ref(false);
const token = localStorage.getItem('token');

const fetchAvailable = async () => {
  loading.value = true;
  try {
    const res = await axios.get('http://127.0.0.1:8000/dashboard/api/available/', {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
    });
    // Transform backend response to expected structure
    available.value = (res.data.rooms || []).map(item => ({
      id: item.room.id,
      name: item.room.name,
      seats: item.seats
    }));
  } catch (err) {
    message.value = 'Failed to fetch available seats.';
  } finally {
    loading.value = false;
  }
};

const makeReservation = async () => {
  if (!selectedClassroom.value || !selectedSeat.value) {
    message.value = 'Please select a classroom and seat.';
    return;
  }
  loading.value = true;
  try {
    const res = await axios.post('http://127.0.0.1:8000/dashboard/api/reservations/', {
      classroom: selectedClassroom.value,
      seat: selectedSeat.value,
      duration: duration.value
    }, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
    });
    // Redirect to success landing page
    router.push({ name: 'booking-success' });
  } catch (err) {
    message.value = err.response?.data?.detail || 'Reservation failed.';
  } finally {
    loading.value = false;
  }
};

onMounted(fetchAvailable);
</script>

<template>
  <div class="container py-5">
    <h1 class="mb-4">Book a Seat</h1>
    <div v-if="message" class="alert" :class="{'alert-success': message === 'Reservation successful!', 'alert-danger': message !== 'Reservation successful!'}">{{ message }}</div>
    <form @submit.prevent="makeReservation" class="card p-4 mb-4 shadow-sm">
      <div class="mb-3">
        <label class="form-label">Classroom</label>
        <select v-model="selectedClassroom" class="form-select" required>
          <option value="" disabled>Select classroom</option>
          <option v-for="room in available" :key="room.id" :value="room.id">{{ room.name }}</option>
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label">Seat</label>
        <select v-model="selectedSeat" class="form-select" required>
          <option value="" disabled>Select seat</option>
          <option v-for="seat in (available.find(room => room.id === selectedClassroom)?.seats || [])":key="seat.id":value="seat.id">{{ seat.name }}</option>
        </select>
      </div>
      <div class="mb-3">
        <label class="form-label">Duration (hours)</label>
        <input v-model.number="duration" type="number" min="1" max="8" class="form-control" required />
      </div>
      <button type="submit" class="btn btn-primary" :disabled="loading">Reserve</button>
    </form>
    <button class="btn btn-secondary" @click="router.back()">Back</button>
  </div>
</template>

<style scoped>
.container { max-width: 500px; }
.alert { margin-bottom: 1rem; }
</style>
