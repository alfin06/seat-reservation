<script>
import { useAuthStore, getCSRFToken } from "../../store/auth.js";

export default {
  name: 'Reservation',
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  data() {
    return {
      rooms: [],
      seats: [],
      reservationForm: {
        room: '',
        seat: '',
        duration: 1,
        date: '',      // ✅ new field
        time: ''       // ✅ new field
      },
      error: '',
      success: ''
    };
  },
  watch: {
    'reservationForm.room'(roomId) {
      const selectedRoom = this.rooms.find(r => r.id === roomId);
      this.seats = selectedRoom
        ? selectedRoom.seats.map(seat => ({
            label: seat.name || `Seat ${seat.id}`,
            value: seat.id
          }))
        : [];
      this.reservationForm.seat = '';
    }
  },
  mounted() {
    this.fetchRooms();
  },
  methods: {
    async fetchRooms() {
      try {
        const res = await fetch('http://127.0.0.1:8000/dashboard/api/available/');
        const data = await res.json();
        this.rooms = data.rooms || [];
      } catch (err) {
        this.error = 'Failed to fetch rooms ' + err;
      }
    },
    async onSubmit() {
      this.error = '';
      this.success = '';
      const token = localStorage.getItem('token');
      // 1. Combine user input into a datetime string
      const localTimeStr = `${this.reservationForm.date}T${this.reservationForm.time}`; // e.g., "2025-05-01T14:00"
      const shanghaiTime = new Date(localTimeStr); // This is in the browser's local time

      // 2. Convert to UTC explicitly
      const utcTimeStr = new Date(
        shanghaiTime.getTime() - (shanghaiTime.getTimezoneOffset() * 60000)
      ).toISOString(); // Will send as UTC

      // 3. Compute reserved_end
      const reservedEnd = new Date(shanghaiTime.getTime() + this.reservationForm.duration * 60 * 60 * 1000);
      const utcReservedEnd = new Date(
        reservedEnd.getTime() - (reservedEnd.getTimezoneOffset() * 60000)
      ).toISOString();

      if (!token) {
        this.error = 'Not authenticated';
        return;
      }
      try {
        const res = await fetch('http://127.0.0.1:8000/dashboard/api/reservations/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`,
          },
          credentials: 'include',
          body: JSON.stringify({
            user_id: this.authStore.user,
            classroom: this.reservationForm.room,
            seat: this.reservationForm.seat,
            duration: this.reservationForm.duration,
            reserved_at: utcTimeStr,
            reserved_end: utcReservedEnd
          })
        });

        const data = await res.json();
        if (res.status === 201) {
          this.$router.push({ name: 'booking-success' });
          return;
        } else {
          this.$notify({type:"error", text:"Reservation failed!"});
          console.log(data.detail || JSON.stringify(data));
        }
      } catch (err) {
        this.$notify({type:"error", text:"Reservation failed!"});
        console.log('Reservation failed ' + err);
      }
    },

    async mounted() {
      await this.authStore.fetchUser();
    },
  }
};
</script>

<template>
  <el-card class="box-card">
    <h2>{{ $t('reservationTitle') }}</h2>
    <br />
    <el-form :model="reservationForm" ref="reservationForm" label-width="150px" @submit.prevent="onSubmit">
      
      <!-- Room -->
      <el-form-item :label="$t('selectStudyRoom')" prop="room">
        <el-select v-model="reservationForm.room" :placeholder="$t('selectRoomPlaceholder')">
          <el-option
            v-for="room in rooms"
            :key="room.id"
            :label="room.name"
            :value="room.id" />
        </el-select>
      </el-form-item>

      <!-- Seat -->
      <el-form-item :label="$t('selectSeat')" prop="seat">
        <el-select v-model="reservationForm.seat" :placeholder="$t('selectSeatPlaceholder')">
          <el-option
            v-for="seat in seats"
            :key="seat.value"
            :label="seat.label"
            :value="seat.value" />
        </el-select>
      </el-form-item>

      <!-- Date Picker -->
      <el-form-item label="Date" prop="date">
        <el-date-picker
          v-model="reservationForm.date"
          type="date"
          placeholder="Pick a date"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>

      <!-- Time Picker -->
      <el-form-item label="Time" prop="time">
        <el-time-picker
          v-model="reservationForm.time"
          placeholder="Pick a time"
          format="HH:mm"
          value-format="HH:mm"
        />
      </el-form-item>

      <!-- Duration -->
      <el-form-item :label="$t('reservationDuration')" prop="duration">
        <el-input-number v-model="reservationForm.duration" :min="1" :max="4" /> 
        &nbsp;&nbsp;<label>{{ $t('hour') }}</label>
      </el-form-item>

      <br/>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">
          {{ $t('reserveSeatButton') }}
        </el-button>
      </el-form-item>

      <p v-if="success" style="color: green;">{{ success }}</p>
      <p v-if="error" style="color: red;">{{ error }}</p>
    </el-form>
  </el-card>
</template>

<style scoped>
.box-card {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
}
</style>
