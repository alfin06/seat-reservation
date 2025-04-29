<template>
    <el-card class="box-card">
      <h2>{{ $t('reservationTitle') }}</h2>
      <el-form
        :model="reservationForm"
        ref="reservationForm"
        label-width="150px"
        @submit.prevent="onSubmit"
      >
        <el-form-item :label="$t('selectStudyRoom')" prop="room">
          <el-select v-model="reservationForm.room" :placeholder="$t('selectRoomPlaceholder')">
            <el-option
              v-for="room in rooms"
              :key="room.value"
              :label="room.label"
              :value="room.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('selectSeat')" prop="seat">
          <el-select v-model="reservationForm.seat" :placeholder="$t('selectSeatPlaceholder')">
            <el-option
              v-for="seat in seats"
              :key="seat.value"
              :label="seat.label"
              :value="seat.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('reservationDuration')" prop="duration">
          <el-input-number v-model="reservationForm.duration" :min="1" :max="4" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">{{ $t('reserveSeatButton') }}</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </template>
  
  
  <script>
  export default {
    name: 'Reservation',
    data() {
      return {
        classrooms: [],
        seats: [],
        form: {
          classroom: '',
          seat: '',
          duration: 1
        },
        error: '',
        success: ''
      }
    },
    watch: {
      'form.classroom'(val) {
        this.fetchSeats(val);
      }
    },
    mounted() {
      this.fetchClassrooms();
    },
    methods: {
      async fetchClassrooms() {
        const res = await fetch('http://127.0.0.1:8000/dashboard/api/available/');
        const data = await res.json();
        // Adjust according to your API response
        this.classrooms = data.classrooms || data.data || [];
      },
      async fetchSeats(classroomId) {
        // Fetch all seats and filter by classroom
        const res = await fetch('http://127.0.0.1:8000/dashboard/api/available/');
        const data = await res.json();
        let allSeats = [];
        if (data.seats) {
          allSeats = data.seats;
        } else if (data.data) {
          allSeats = data.data.flatMap(room => room.seats || []);
        }
        this.seats = allSeats.filter(s => s.classroom === classroomId);
      },
      async onSubmit() {
        this.error = '';
        this.success = '';
        const token = localStorage.getItem('token');
        if (!token) {
          this.error = 'Not authenticated';
          return;
        }
        const res = await fetch('http://127.0.0.1:8000/dashboard/api/reservations/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Token ${token}`
          },
          body: JSON.stringify({
            classroom: this.form.classroom,
            seat: this.form.seat,
            duration: this.form.duration
          })
        });
        const data = await res.json();
        if (res.status === 201) {
          this.success = 'Reservation successful!';
        } else {
          this.error = data.detail || JSON.stringify(data);
        }
      }
    }
  }
  </script>

  
  <style scoped>
  .box-card {
    max-width: 600px;
    margin: 20px auto;
    padding: 20px;
  }
  </style>
  