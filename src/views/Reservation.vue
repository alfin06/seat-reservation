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
        reservationForm: {
          room: '',
          seat: '',
          duration: 1
        },
        rooms: [
          { value: 'RoomA', label: 'Room A' },
          { value: 'RoomB', label: 'Room B' },
          { value: 'RoomC', label: 'Room C' }
        ],
        seats: [
          { value: 'Seat1', label: 'Seat 1' },
          { value: 'Seat2', label: 'Seat 2' },
          { value: 'Seat3', label: 'Seat 3' }
        ]
      }
    },
    methods: {
      onSubmit() {
        console.log('Reservation Form Submitted:', this.reservationForm)
        // TODO: Connect with your API to process the reservation
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
  